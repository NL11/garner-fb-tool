from __future__ import print_function
import os.path
from googleapiclient import errors
from googleapiclient import discovery
import io
import os
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import datetime
import glob
import time
from oauth2client.service_account import ServiceAccountCredentials
import save_data
from settings import MyGlobals
import smtplib
import ssl
from email.message import EmailMessage
"""
from email.Utils import COMMASPACE, formatdate
from email import Encoders
"""


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

SAMPLE_MANIFEST = '''
{
  "timeZone": "America/New_York",
  "exceptionLogging": "CLOUD"
}
'''.strip()


def get_user_info():
    """Calls the Apps Script API.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Apps Script API
    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'User Info!A2:J'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        data = result.get('values', [])
        return data
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''


def set_user_info(values):
    states = []
    message_read = []
    wait_for_update = []
    for user_state in values:
        states += [[user_state[6]]]
        message_read += [[user_state[7]]]
        wait_for_update += [[user_state[9]]]

    """Calls the Apps Script API."""
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Apps Script API
    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'User Info!G2:G' + str(len(states) + 1)
        body = {
            'values': states
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        data = result.get('values', [])
        #return 'Success'
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''

    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'User Info!H2:H' + str(len(message_read) + 1)
        body = {
            'values': message_read
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        data = result.get('values', [])
        #return 'Success'
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''

    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'User Info!J2:J' + str(len(wait_for_update) + 1)
        body = {
            'values': wait_for_update
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        data = result.get('values', [])
        #return 'Success'
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''


def upload_missionary_blacklist(missionaires):
    missionaires_array = []
    for missionary in missionaires:
        missionaires_array += [[missionary]]

    """Calls the Apps Script API."""
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Apps Script API
    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'Missionary List!A1:A'
        body = {
            'values': missionaires_array
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        data = result.get('values', [])
        return 'Success'
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''


def get_blacklist():
    """Calls the Apps Script API."""
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
    service = discovery.build('sheets', 'v4', credentials=creds)
    # Call the Apps Script API
    missionaries = []
    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = 'Missionary List!A1:A'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        data = result.get('values', [])
        missionaries = data
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''
    blacklist = []
    try:
        spreadsheet_id = MyGlobals.spreadsheet_id
        range_name = "'Blacklist'!A1:A"
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        data = result.get('values', [])
        blacklist = data
    except errors.HttpError as error:
        # The API encountered a problem.
        # print(error.content)
        ''
    save_data.update_blacklist(missionaries + blacklist)
    return missionaries


def download_audio(user):
    """Calls the Apps Script API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    service = discovery.build('drive', 'v3', credentials=creds)
    # print(user[1])
    page_token = None
    while True:
        response = service.files().list(
            q="trashed = false and name='" + user[1].split('@')[0].replace(".", "_") + ".m4a'", spaces='drive',
            fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            # print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            ''
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    try:
        file_id = response.get('files', [])[0].get('id')
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(user[1].split('@')[0].replace(".", "_") + ".m4a", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
    except:
        ''


def upload_daily_report():
    """Calls the Apps Script API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    service = discovery.build('drive', 'v3', credentials=creds)

    year_folder_id = None
    month_folder_id = None
    day_folder_id = None
    # Search Year
    page_token = None
    while True:
        response = service.files().list(
            q="'" + MyGlobals.reports_folder + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
            spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        for file in response.get('files', []):
            if (file.get('name') == datetime.datetime.today().strftime("%Y")):
                year_folder_id = file.get('id')
                break
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    if (year_folder_id == None):
        # Create Year
        file_metadata = {
            'name': datetime.datetime.today().strftime("%Y"),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [MyGlobals.reports_folder]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        year_folder_id = folder.get('id')

    page_token = None
    while True:
        response = service.files().list(
            q="'" + year_folder_id + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
            spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        for file in response.get('files', []):
            if (file.get('name') == datetime.datetime.today().strftime("%B")):
                month_folder_id = file.get('id')
                break
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    if (month_folder_id == None):
        # Create Month
        file_metadata = {
            'name': datetime.datetime.today().strftime("%B"),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [year_folder_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        month_folder_id = folder.get('id')

    page_token = None
    while True:
        response = service.files().list(
            q="'" + month_folder_id + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
            spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        for file in response.get('files', []):
            if (file.get('name') == datetime.datetime.today().strftime("%Y-%m-%d")):
                day_folder_id = file.get('id')
                break
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    if (day_folder_id == None):
        # Create Month
        file_metadata = {
            'name': datetime.datetime.today().strftime("%Y-%m-%d"),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [month_folder_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        day_folder_id = folder.get('id')
    try:
        # Create Report
        file_metadata = {
            'name': datetime.datetime.today().strftime("%H:%M:%S"),
            'parents': [day_folder_id]
        }
        media = MediaFileUpload('daily_report.csv', mimetype='text/csv', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    except Exception as e:
        # print('Uploading Report Failed' + str(e))
        ''
    return None


def upload_screen_shots():
    """Calls the Apps Script API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    service = discovery.build('drive', 'v3', credentials=creds)

    files = glob.glob("error_screenshots/*.png")
    year_folder_id = None
    month_folder_id = None
    day_folder_id = None
    # Search Year
    if (len(files) > 0):
        page_token = None
        while True:
            response = service.files().list(
                q="'" + MyGlobals.errors_folder + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
                spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            for file in response.get('files', []):
                if (file.get('name') == datetime.datetime.today().strftime("%Y")):
                    year_folder_id = file.get('id')
                    break
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        if (year_folder_id == None):
            # Create Year
            file_metadata = {
                'name': datetime.datetime.today().strftime("%Y"),
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [MyGlobals.errors_folder]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            year_folder_id = folder.get('id')

        page_token = None
        while True:
            response = service.files().list(
                q="'" + year_folder_id + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
                spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            for file in response.get('files', []):
                if (file.get('name') == datetime.datetime.today().strftime("%B")):
                    month_folder_id = file.get('id')
                    break
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        if (month_folder_id == None):
            # Create Month
            file_metadata = {
                'name': datetime.datetime.today().strftime("%B"),
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [year_folder_id]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            month_folder_id = folder.get('id')

        page_token = None
        while True:
            response = service.files().list(
                q="'" + month_folder_id + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'",
                spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            for file in response.get('files', []):
                if (file.get('name') == datetime.datetime.today().strftime("%Y-%m-%d")):
                    day_folder_id = file.get('id')
                    break
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        if (day_folder_id == None):
            # Create Month
            file_metadata = {
                'name': datetime.datetime.today().strftime("%Y-%m-%d"),
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [month_folder_id]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            day_folder_id = folder.get('id')

        for file in files:
            try:
                # Create Report
                file_metadata = {
                    'name': file.replace('.png', '').replace('error_screenshots/', ''),
                    'parents': [day_folder_id]
                }
                media = MediaFileUpload(file, 'image/png', resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            except Exception as e:
                # print('Uploading Report Failed' + str(e))
                ''
        time.sleep(2)
        media = ''
        for file in files:
            os.remove(file)
    return None


def send_message(user_email, message):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "fountn.manager@gmail.com"
    receiver_email = user_email
    password = 'Fountn2020'
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Garner login error'
    msg['From'] = sender_email
    msg['To'] = user_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())