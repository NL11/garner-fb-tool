import csv
from os import path
import os
import datetime
import time
from settings import MyGlobals

def on_blacklist(id):
    with open('blacklist.csv', "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row['fb_id'] == id):
                return True
    return False


def get_missionary_blacklist():
    missionary_array = []
    with open('missionary_blacklist.csv', "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            missionary_array.append(row['fb_id'])
    return missionary_array


def update_blacklist(blacklist_info):
    with open('blacklist.csv', 'w', newline='') as csvfile:
        fieldnames = ['fb_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for id in blacklist_info:
            try:
                writer.writerow({'fb_id': id[0]})
            except:
                ''
    with open('missionary_blacklist.csv', 'w', newline='') as csvfile:
        fieldnames = ['fb_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def add_missionary_to_blacklist(fb_id):
    with open('missionary_blacklist.csv', 'a', newline='') as csvfile:
        fieldnames = ['fb_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'fb_id': fb_id})


def add_friend_user(user, friends_added):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'fb_id', 'date', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for friend in friends_added:
            writer.writerow({'name': friend[0], 'fb_id': friend[1], 'date': friend[2], 'status': 'pending'})


def add_friend_master(user, friends_added):
    with open('local_master.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'fb_id', 'date', 'user']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for friend in friends_added:
            writer.writerow({'name': friend[0], 'fb_id': friend[1], 'date': friend[2], 'user': user[1]})

def add_friend_user_page(user, friends_added):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'fb_id', 'date', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for friend in friends_added:
            writer.writerow({'name': friend[0], 'fb_id': friend[1], 'date': friend[2], 'status': 'page'})


def check_master_csv():
    new_status = '0'
    num_cycles = MyGlobals.num_cycles
    if (not (path.exists('local_master.csv'))):
        with open('local_master.csv', 'w', newline='') as csvfile:
            fieldnames = ['name', 'fb_id', 'date', 'user']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    if (not (path.exists('status.txt'))):
        status = 0
        if(num_cycles > 1):
            new_status = '1'
        else:
            new_status = '0'
    else:
        with open('status.txt', 'r') as txtfile:
            status = txtfile.read()
            if(num_cycles == 1):
                new_status = '0'
            elif(int(status) == 0):
                new_status = '1'
            elif(int(status) >= num_cycles-1):
                new_status = '0'
            else:
                new_status = str(int(status) + 1)
    with open('status.txt', 'w') as txtfile:
        txtfile.write(new_status)
    if (not (path.exists('friend_info'))):
        os.makedirs('friend_info')
    if (not (path.exists('reversion_info'))):
        os.makedirs('reversion_info')
    if (not (path.exists('block_info'))):
        os.makedirs('block_info')
    if (not (path.exists('pickle_files'))):
        os.makedirs('pickle_files')
    if (not (path.exists('error_screenshots'))):
        os.makedirs('error_screenshots')
    return status


def update_added_friends(user, new_friends):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', "r") as infile, open('friend_info/temp.csv', "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['name', 'fb_id', 'date', 'status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        recent_friends_added = []
        for row in reader:
            found = False
            page = False
            for friend in new_friends:
                if (str(row['fb_id']) == friend[1] and str(row['status']) != 'messaged' and str(row['status']) != 'friended'):
                    if(str(row['status']) != 'page'):
                        recent_friends_added.append([row['name'], row['fb_id'], row['date'], 'friended'])
                        found = True
                        page = False
                        break
                    else:
                        recent_friends_added.append([row['name'], row['fb_id'], row['date'], 'page_friended'])
                        found = True
                        page = True
                        break
            if (found):
                if(page):
                    writer.writerow({'name': row['name'], 'fb_id': row['fb_id'], 'date': datetime.date.today().strftime('%d/%m/%Y'),'status': 'page_friended'})
                else:
                    writer.writerow({'name': row['name'], 'fb_id': row['fb_id'], 'date': datetime.date.today().strftime('%d/%m/%Y'),'status': 'friended'})
            else:
                writer.writerow(row)
    os.remove(r'friend_info/' + user[1].split('@')[0] + '.csv')
    os.rename(r'friend_info/temp.csv', r'friend_info/' + user[1].split('@')[0] + '.csv')
    return recent_friends_added


def get_unmessaged_friends(user):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', "r") as csvfile:
        reader = csv.DictReader(csvfile)
        unmessaged_friends = []
        start_date = datetime.datetime.today() + datetime.timedelta(-7)
        for row in reader:
            date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
            if (str(row['status']) == 'friended' and date > start_date):
                unmessaged_friends.append([row['name'], row['fb_id'], row['date'], 'friended'])
            elif(str(row['status']) == 'page_friended' and date > start_date):
                unmessaged_friends.append([row['name'], row['fb_id'], row['date'], 'page_friended'])
    return unmessaged_friends


def update_messaged_friends(user, messaged_friends):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', "r") as infile, open('friend_info/temp.csv', "w",
                                                                                     newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['name', 'fb_id', 'date', 'status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        recent_friends_messaged = []
        for row in reader:
            found = False
            page = False
            for friend in messaged_friends:
                if (str(row['fb_id']) == friend[1]):
                    if(str(row['status']) == "page_friended"):
                        recent_friends_messaged.append([row['name'], row['fb_id'], row['date'], 'messaged'])
                        found = True
                        page = False
                        break
                    else:
                        recent_friends_messaged.append([row['name'], row['fb_id'], row['date'], 'page_messaged'])
                        found = True
                        page = True
                        break
            if (found):
                if(page):
                    writer.writerow({'name': row['name'], 'fb_id': row['fb_id'], 'date': datetime.date.today().strftime('%d/%m/%Y'),'status': 'page_messaged'})
                else:
                    writer.writerow({'name': row['name'], 'fb_id': row['fb_id'], 'date': datetime.date.today().strftime('%d/%m/%Y'),'status': 'messaged'})
            else:
                writer.writerow(row)
    os.remove(r'friend_info/' + user[1].split('@')[0] + '.csv')
    os.rename(r'friend_info/temp.csv', r'friend_info/' + user[1].split('@')[0] + '.csv')
    return recent_friends_messaged


def add_reversion(user):
    with open('reversion_info/' + user[1].split('@')[0] + '.csv', 'a', newline='') as csvfile:
        fieldnames = ['date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'date': datetime.date.today().strftime('%d/%m/%Y')})


def add_block(user):
    with open('block_info/' + user[1].split('@')[0] + '.csv', 'a', newline='') as csvfile:
        fieldnames = ['date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'date': datetime.date.today().strftime('%d/%m/%Y')})


def update_canceled_requests(user, canceled_friend_requests):
    with open('friend_info/' + user[1].split('@')[0] + '.csv', "r") as infile, open('friend_info/temp.csv', "w",
                                                                                     newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['name', 'fb_id', 'date', 'status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        recent_friends_canceled = []
        for row in reader:
            found = False
            for friend in canceled_friend_requests:
                if (str(row['fb_id']) == friend[1]):
                    recent_friends_canceled.append([row['name'], row['fb_id'], row['date'], 'canceled'])
                    found = True
                    break
            if (found):
                writer.writerow(
                    {'name': row['name'], 'fb_id': row['fb_id'], 'date': datetime.date.today().strftime('%d/%m/%Y'),
                     'status': 'canceled'})
            else:
                writer.writerow(row)
    os.remove(r'friend_info/' + user[1].split('@')[0] + '.csv')
    os.rename(r'friend_info/temp.csv', r'friend_info/' + user[1].split('@')[0] + '.csv')
    return recent_friends_canceled


def delete_user(user):
    if (path.exists('friend_info/' + user[1].split('@')[0] + '.csv')):
        os.remove(r'friend_info/' + user[1].split('@')[0] + '.csv')
    if (path.exists('reversion_info/' + user[1].split('@')[0] + '.csv')):
        os.remove(r'reversion_info/' + user[1].split('@')[0] + '.csv')
    if (path.exists('block_info/' + user[1].split('@')[0] + '.csv')):
        os.remove(r'block_info/' + user[1].split('@')[0] + '.csv')
    return user


def generate_daily_report(user_data):
    with open('daily_report.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user', 'setting', 'status', 'page', 'message', 'login', 'city', 'new_friends',
                      'friends_messaged', 'pending_cleared', 'groups', 'friends_invited_to_like_page', 'last_post',
                      'unread_messages', 'acceptance_ratio', 'people_you_may_know_3_mon', 'block_3_mon', 'penaly_added',
                      'quota', 'sent_requests_friends', 'sent_requests_groups', 'sent_requests_page',
                      'people_you_may_know', 'block']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in user_data:
            writer.writerow(
                {'user': user[0], 'setting': user[1], 'status': user[2], 'page': user[3], 'message': user[4],
                 'login': user[5], 'city': user[6], 'new_friends': user[7], 'friends_messaged': user[8],
                 'pending_cleared': user[9], 'groups': user[10], 'friends_invited_to_like_page': user[11],
                 'last_post': user[12], 'unread_messages': user[13], 'acceptance_ratio': user[14],
                 'people_you_may_know_3_mon': user[15], 'block_3_mon': user[16], 'penaly_added': user[17],
                 'quota': user[18], 'sent_requests_friends': user[19], 'sent_requests_groups': user[20],
                 'sent_requests_page': user[21], 'people_you_may_know': user[22], 'block': user[23]})
    time.sleep(2)
