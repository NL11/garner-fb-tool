import csv
import math
import datetime
import time
import random
import save_data
from dateutil.parser import parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def generate_quota(user, user_data, driver):
    pending = 0
    friended = 0
    penalty_quota = 0
    with open('friend_info/' + user[1].split('@')[0] + '.csv', "r") as infile:
        reader = csv.DictReader(infile)
        start_date = datetime.datetime.today() + datetime.timedelta(-20)
        end_date = datetime.datetime.today() + datetime.timedelta(-10)
        alt_start_date = datetime.datetime.today() + datetime.timedelta(-5)
        alt_end_date = datetime.datetime.today()
        for row in reader:
            try:
                date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
            except:
                ''
            if (date > start_date and date < end_date):
                if (str(row['status']) == 'pending'):
                    pending += 1
                elif (str(row['status']) == 'friended'):
                    friended += 1
            if (date > alt_start_date and date < alt_end_date):
                penalty_quota += 1
    try:
        if (friended + pending > 20):
            accepted_ratio = friended / (friended + pending)
        else:
            accepted_ratio = .15
    except:
        accepted_ratio = .15
    last_post = user_data[3]
    post_date = ''
    if 'h' in last_post:
        todays_date = datetime.date.today()
        post_date = datetime.date.today()
    elif 'd' in last_post:
        todays_date = datetime.date.today()
        try:
            post_date = datetime.date.today() + datetime.timedelta(-1 * int(last_post[:-1]))
        except:
            post_date = datetime.date.today() + datetime.timedelta(-60)
    else:
        try:
            todays_date = datetime.datetime.today()
            post_date = parse(last_post)
        except:
            post_date = datetime.datetime.today() + datetime.timedelta(-60)

    last_post_days = (todays_date - post_date).days

    driver.execute_script("window.open('', '_blank');")
    driver.switch_to_window(driver.window_handles[1])
    time.sleep(random.uniform(1.0, 2.2))
    driver.get('https://m.facebook.com/messages/?folder=unread')
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'New Message')]]")))
    while True:
        try:
            get_more = driver.find_element_by_xpath("//*[text()[contains(., 'See Older Messages…')]]")
            get_more.click()
            time.sleep(random.uniform(3.0, 5.0))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            break
    unread_message_elements = driver.find_elements_by_xpath(".//a[contains(@href, '/messages/read/')]")
    unreads = []
    for unread in unread_message_elements:
        message_class = unread.get_attribute('class')
        if (message_class != 'touchable' and message_class != 'touchable primary'):
            unreads.append(unread.get_attribute('innerHTML'))

    unread_messages = len(unreads)
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

    button_reversions = 0
    with open('reversion_info/' + user[1].split('@')[0] + '.csv', "r") as infile:
        reader = csv.DictReader(infile)
        start_date = datetime.datetime.today() + datetime.timedelta(-20)
        for row in reader:
            date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
            if (date > start_date):
                button_reversions += 1

    friending_blocks = 0
    with open('block_info/' + user[1].split('@')[0] + '.csv', "r") as infile:
        reader = csv.DictReader(infile)
        start_date = datetime.datetime.today() + datetime.timedelta(-20)
        for row in reader:
            date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
            if (date > start_date):
                friending_blocks += 1

    quota = calculate_quota(accepted_ratio, last_post_days, unread_messages, button_reversions, friending_blocks,
                            penalty_quota)

    return [round(quota[0]), last_post_days, unread_messages, accepted_ratio, button_reversions, friending_blocks,
            quota[1]]


def check_user(id):
    input_file = csv.DictReader(open("local_master.csv"))
    start_date = datetime.datetime.today() + datetime.timedelta(-90)
    for row in input_file:
        date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
        if (str(row['fb_id']) == id and date > start_date):
            return True
    if (not (save_data.on_blacklist(id))):
        return False
    else:
        return True


def check_age(id, user):
    input_file = csv.DictReader(open('friend_info/' + user[1].split('@')[0] + '.csv'))
    start_date = datetime.datetime.today() + datetime.timedelta(-5)
    for row in input_file:
        date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
        if (str(row['fb_id']) == id and date < start_date):
            return True
    return False


def check_recent_friend(id, recent_friends_added):
    for friend in recent_friends_added:
        if (friend[1] == id):
            return True
    return False


def is_from_fountn(fb_id, user):
    input_file = csv.DictReader(open('friend_info/' + user[1].split('@')[0] + '.csv'))
    for row in input_file:
        if (str(row['fb_id']) == fb_id):
            return True
    return False


def has_requests_to_clear(user):
    input_file = csv.DictReader(open('friend_info/' + user[1].split('@')[0] + '.csv'))
    start_date = datetime.datetime.today() + datetime.timedelta(-5)
    for row in input_file:
        date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
        if (str(row['status']) == 'pending' and date < start_date):
            return True
    return False


def calculate_quota(accepted_ratio, last_post_days, unread_messages, button_reversions, friending_blocks,
                    penalty_quota):
    accepted_ratio_multiplier = (1 / (1 + math.exp(-(12 * (accepted_ratio) - 3.5)))) * .90 + .10
    last_post_days_multiplier = (1 / (1 + math.exp(0.30 * (last_post_days) - 10))) * .5 + .5
    unread_messages_multiplier = (1 / (1 + math.exp(0.35 * (unread_messages) - 10))) * .5 + .5
    button_reversions_multiplier = (1 / (1 + math.exp(0.40 * (button_reversions) - 5))) * .90 + .10
    friending_blocks_multiplier = (1 / (1 + math.exp(2 * (friending_blocks) - 5))) * .90 + .10
    if (penalty_quota < 100):
        penalty = (1 / (1 + math.exp(-(.08 * penalty_quota - 3)))) * .5 + .5
    else:
        penalty = 1
    return [round(
        120 * accepted_ratio_multiplier * last_post_days_multiplier * unread_messages_multiplier * button_reversions_multiplier * friending_blocks_multiplier * penalty),
            penalty]


def check_user_page(user, id, fb_date):
    input_file = csv.DictReader(open('friend_info/' + user[1].split('@')[0] + '.csv'))
    start_date = datetime.datetime.today() + datetime.timedelta(-90)
    todays_date = datetime.date.today()
    other_date = datetime.datetime.strptime(fb_date, '%m/%d/%y').date()
    if (other_date == todays_date):
        for row in input_file:
            date = datetime.datetime.strptime(str(row['date']), '%d/%m/%Y')
            if (str(row['fb_id']) == id and date > start_date):
                return False
        return True
    if (not (save_data.on_blacklist(id))):
        return False
    else:
        return True
