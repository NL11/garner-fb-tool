import time
import random
import groups
import datetime
import request_check
import user_info
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dateutil.parser import parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def friend_by_group(driver, quota):
    time.sleep(random.uniform(2.0, 4.0))
    user_groups_array = groups.get_user_groups(driver)
    error_data = ''
    friends_added = []
    for group_data in user_groups_array:
        if (quota != 0):
            if (group_data[0] != ''):
                time.sleep(random.uniform(2.0, 4.0))
                run_data = groups.members_near_me(driver, group_data[1], quota)
                if (run_data[1] == 'people_you_may_know' or run_data[1] == 'account_blocked'):
                    error_data = run_data[1]
                    if (len(run_data[0]) != 0):
                        for friend in run_data[0]:
                            friends_added.append(friend)
                    quota = 0
                else:
                    quota = quota - len(run_data[0])
                    error_data = ''
                    if (len(run_data[0]) != 0):
                        for friend in run_data[0]:
                            friends_added.append(friend)
    return [friends_added, error_data, user_groups_array]


def friend_by_friend(user, driver, quota):
    friends = get_recent_friends(driver, user)
    random.shuffle(friends)
    error_data = ''
    friends_added = []
    for friend in friends:
        if (request_check.is_from_fountn(friend[1], user) and quota > 0):
            time.sleep(random.uniform(2.0, 4.0))
            run_data = groups.current_city(user, driver, friend[1], quota)
            if (run_data[1] == 'people_you_may_know' or run_data[1] == 'account_blocked'):
                error_data = run_data[1]
                if (len(run_data[0]) != 0):
                    for friend in run_data[0]:
                        friends_added.append(friend)
                quota = 0
            else:
                quota = quota - len(run_data[0])
                error_data = ''
                if (len(run_data[0]) != 0):
                    for friend in run_data[0]:
                        friends_added.append(friend)
    return [friends_added, error_data]


def escape_string_for_xpath(s):
    if '"' in s and "'" in s:
        return 'concat(%s)' % ", '\"',".join('"%s"' % x for x in s.split('"'))
    elif '"' in s:
        return "'%s'" % s
    return '"%s"' % s

def get_new_friends(driver, user):
    time.sleep(random.uniform(1.0, 2.5))
    new_friends = []
    driver.get("https://www.facebook.com/me/allactivity/?category_key=FRIENDS&filter_hidden=ALL&filter_privacy=NONE")
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Activity Log')]]")))
    time.sleep(0.5)
    """
    try:
        load_elements_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-visualcompletion='loading-state' and aria-valuetext='Loading...' and role='progressbar' and aria-busy='true' and aria-valuemax='100' and style='animation-delay: 1100ms;']")))
        todays_friends_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()[contains(., 'Today')]]"))).find_element_by_xpath(
            '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_xpath('..').find_element_by_xpath('..')
        todays_friends = todays_friends_div.find_elements_by_xpath(".//*[text()[contains(., 'became friends with')]]")
        todays_friends_len = len(todays_friends)
    except:
        scroll = False
    while scroll:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", load_elements_div)
            load_elements_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                "[data-visualcompletion='loading-state' and aria-valuetext='Loading...' and role='progressbar' and aria-busy='true' and aria-valuemax='100' and style='animation-delay: 1100ms;']")))
            todays_friends_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[text()[contains(., 'Today')]]"))).find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..')
            todays_friends = todays_friends_div.find_elements_by_xpath(
                ".//*[text()[contains(., 'became friends with')]]")
            time.sleep(random.uniform(1.0, 2.0))
            if (todays_friends_len == len(todays_friends)):
                scroll = False
            else:
                todays_friends_len = len(todays_friends_div)
        except:
            scroll = False
    """
    try:
        todays_friends_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()[contains(., 'Today')]]"))).find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        todays_friends = todays_friends_div.find_elements_by_xpath(".//*[text()[contains(., 'became friends with')]]")
        for friend in todays_friends:
            try:
                name = friend.text.split('became friends with ')[1].split('.')[0]
                fb_id = friend.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('href').split('https://www.facebook.com/')[1]
                new_friends.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                time.sleep(random.uniform(1.5, 2.5))
            except Exception as e:
                ''
    except Exception as e:
        ''
    try:
        yesterdays_friends_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()[contains(., 'Yesterday')]]"))).find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        yesterdays_friends = yesterdays_friends_div.find_elements_by_xpath(".//*[text()[contains(., 'became friends with')]]")
        for friend in yesterdays_friends:
            try:
                name = friend.text.split('became friends with ')[1].split('.')[0]
                fb_id = friend.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('href').split('https://www.facebook.com/')[1]
                new_friends.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                time.sleep(random.uniform(1.5, 2.5))
            except Exception as e:
                ''
    except Exception as e:
        ''
    return(new_friends)

def get_new_friends_old(driver, user):
    time.sleep(random.uniform(1.0, 2.5))
    new_friends = []
    driver.get('https://m.facebook.com/me/allactivity/?category_key=friends&entry_point=settings_yfi')
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Activity Log')]]")))
    time.sleep(0.5)
    try:
        todays_friends_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Today')]]"))).find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        todays_friends = todays_friends_div.find_elements_by_xpath(".//a[contains(@href, '/story.php')]")
        new_friends_thing = []
        for friend in todays_friends:
            new_friends_thing.append([friend.get_attribute('href'), friend.text])
        for friend in new_friends_thing:
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to_window(driver.window_handles[1])
            try:
                link = friend[0]
                name = friend[1]
                if (name != ''):
                    name = name.split('with ')[1].replace('.', '')
                    driver.get(link)
                    escaped_name = escape_string_for_xpath(name)
                    link_alt = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//a[text() = " + escaped_name + "]")))
                    # link_alt = driver.find_element_by_xpath("//a[text() = " + escaped_name + "]")
                    fb_id = link_alt.get_attribute('href').split('/')[3].split('?refid=')[0].split('&refid=')[0]
                    new_friends.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                    time.sleep(random.uniform(1.5, 2.5))
            except Exception as e:
                ''
                # print(e)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        # print(e)
        ''
    try:
        yesterdays_friends_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Yesterday')]]"))).find_element_by_xpath('..')
        yesterdays_friends = yesterdays_friends_div.find_elements_by_xpath(".//a[contains(@href, '/story.php')]")
        new_friends_thing = []
        for friend in yesterdays_friends:
            new_friends_thing.append([friend.get_attribute('href'), friend.text])
        for friend in new_friends_thing:
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to_window(driver.window_handles[1])
            try:
                link = friend[0]
                name = friend[1]
                if (name != ''):
                    name = name.split('with ')[1].replace('.', '')
                    driver.get(link)
                    escaped_name = escape_string_for_xpath(name)
                    link_alt = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//a[text() = " + escaped_name + "]")))
                    # link_alt = driver.find_element_by_xpath("//a[text() = " + escaped_name + "]")
                    fb_id = link_alt.get_attribute('href').split('/')[3].split('?refid=')[0].split('&refid=')[0]
                    new_friends.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                    time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                ''
                # print(e)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        ''
    return new_friends


def get_recent_friends(driver, user):
    time.sleep(random.uniform(1.0, 2.0))

    driver.get('https://facebook.com/me/friends_recent')
    new_friends = []
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Recently Added')]]")))
    time.sleep(1.0)
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_members_len = 0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(2.0, 4.0))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        new_members_len = len(driver.find_elements_by_css_selector("[aria-label='Friends']"))
        if new_members_len == last_members_len:
            break
        last_members_len = new_members_len

    members = driver.find_elements_by_css_selector("[aria-label='Friends']")
    for member in members:
        try:
            container = member.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..')
            href = container.find_elements_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")[1]
            name_obj = href.find_element_by_xpath("./span")
            name = name_obj.get_attribute('innerHTML')
            link = href.get_attribute('href')
            fb_id = link.split('/')[3]
            new_friends.append([name, fb_id])
        except Exception as e:
            ''
            # driver.save_screenshot("error_screenshots/" + user[1].split('@')[0] + " - " + 'logging_friends-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
    return new_friends


def send_messages_new_friends(user, driver, friends):
    friends_messaged = []
    if (user[4] == '{voice_message}'):
        user_info.download_audio(user)
    for friend in friends:
        if(str(friend[3]) != "page_friended"):
            time.sleep(random.uniform(3.0, 5.0))
            friend_fixed = friend[1].replace('profile.php?id=', '')
            driver.get('https://www.facebook.com/messages/t/' + friend_fixed)
            message_friend = True
            try:
                text_box = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='outgoing_group']")))
                    friends_messaged.append(friend)
                    message_friend = False
                except:
                    ''
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='incoming_group']")))
                    friends_messaged.append(friend)
                    message_friend = False
                except:
                    ''
                if(message_friend == True):
                    if (user[4] != '{voice_message}'):
                        message = user[4].replace('{first_name}', friend[0].split(' ')[0])
                        message = message.replace('{First_name}', friend[0].split(' ')[0])
                        message = message.replace('{first_Name}', friend[0].split(' ')[0])
                        message = message.replace('{First_Name}', friend[0].split(' ')[0])
                        message = message.replace('{first name}', friend[0].split(' ')[0])
                        message = message.replace('{First name}', friend[0].split(' ')[0])
                        message = message.replace('{first Name}', friend[0].split(' ')[0])
                        message = message.replace('{First Name}', friend[0].split(' ')[0])
                        message = message.replace('{full_name}', friend[0])
                        message = message.replace('{Full_name}', friend[0])
                        message = message.replace('{full_Name}', friend[0])
                        message = message.replace('{Full_Name}', friend[0])
                        message = message.replace('{full name}', friend[0])
                        message = message.replace('{Full name}', friend[0])
                        message = message.replace('{full Name}', friend[0])
                        message = message.replace('{Full Name}', friend[0])
                        text_box.send_keys(message)
                        text_box.send_keys(Keys.RETURN)
                        friends_messaged.append(friend)
                        delivery = WebDriverWait(driver, 40).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@data-testid='messenger_delivery_status']")))
                        try:
                            WebDriverWait(delivery, 5).until(
                                EC.presence_of_element_located((By.XPATH, ".//*[contains(@alt, 'Error']")))
                            return friends_messaged
                        except:
                            try:
                                WebDriverWait(delivery, 25).until(EC.presence_of_element_located(
                                    (By.XPATH, ".//*[contains(@alt, 'Seen') or @alt='Delivered' or @alt='Sent']")))
                                time.sleep(random.uniform(2.0, 3.5))
                            except:
                                ""
                    else:
                        open_more = driver.find_element_by_css_selector("[aria-label='Open more actions']")
                        open_more.click()
                        time.sleep(random.uniform(1.5, 2.5))
                        send_file = driver.find_element_by_xpath("//input[@type='file']")
                        send_file.send_keys('/home/fountn/garner_python/' + user[1].split('@')[0].replace(".", "_") + ".m4a")
                        text_box.send_keys(Keys.RETURN)
                        friends_messaged.append(friend)
                        WebDriverWait(driver, 40).until(
                            EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Play')]]")))
                        time.sleep(0.5)
            except Exception as e:
                ''
        else:
            try:
                text_box = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='outgoing_group']")))
                    friends_messaged.append(friend)
                    message_friend = False
                except:
                    ''
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='incoming_group']")))
                    friends_messaged.append(friend)
                    message_friend = False
                except:
                    ''
                if(message_friend == True):
                    message = user[4].replace('{first_name}', friend[0].split(' ')[0])
                    message = message.replace('{First_name}', friend[0].split(' ')[0])
                    message = message.replace('{first_Name}', friend[0].split(' ')[0])
                    message = message.replace('{First_Name}', friend[0].split(' ')[0])
                    message = message.replace('{first name}', friend[0].split(' ')[0])
                    message = message.replace('{First name}', friend[0].split(' ')[0])
                    message = message.replace('{first Name}', friend[0].split(' ')[0])
                    message = message.replace('{First Name}', friend[0].split(' ')[0])
                    message = message.replace('{full_name}', friend[0])
                    message = message.replace('{Full_name}', friend[0])
                    message = message.replace('{full_Name}', friend[0])
                    message = message.replace('{Full_Name}', friend[0])
                    message = message.replace('{full name}', friend[0])
                    message = message.replace('{Full name}', friend[0])
                    message = message.replace('{full Name}', friend[0])
                    message = message.replace('{Full Name}', friend[0])
                    text_box.send_keys(message)
                    text_box.send_keys(Keys.RETURN)
                    friends_messaged.append(friend)
                    delivery = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@data-testid='messenger_delivery_status']")))
                    try:
                        WebDriverWait(delivery, 5).until(
                            EC.presence_of_element_located((By.XPATH, ".//*[contains(@alt, 'Error']")))
                        return friends_messaged
                    except:
                        try:
                            WebDriverWait(delivery, 25).until(EC.presence_of_element_located(
                                (By.XPATH, ".//*[contains(@alt, 'Seen') or @alt='Delivered' or @alt='Sent']")))
                            time.sleep(random.uniform(2.0, 3.5))
                        except:
                            ""
            except Exception as e:
                ''
    if (user[4] == '{voice_message}'):
        try:
            os.remove(r'' + user[1].split('@')[0].replace(".", "_") + ".m4a")
        except:
            ''
    time.sleep(2)
    return friends_messaged


def clear_all_pending_requests(driver, user):
    driver.get('https://www.facebook.com/friends/requests')
    removed_friends = []
    view_all_button = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'View Sent Requests')]]")))
    time.sleep(2.0)
    view_all_button.click()
    scroll = True
    time.sleep(1.0)
    try:
        load_elements_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-visualcompletion='loading-state' and aria-valuetext='Loading...' and role='progressbar' and aria-busy='true' and aria-valuemax='100' and style='animation-delay: 1100ms;']")))
    except:
        scroll = False
    while scroll:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", load_elements_div)
            time.sleep(random.uniform(1.0, 2.0))
            if (len(driver.find_elements_by_css_selector("[aria-label='Cancel Request']")) == 0):
                scroll = False
        except:
            scroll = False
    cancel_buttons = driver.find_elements_by_css_selector("[aria-label='Cancel Request']")
    random.shuffle(cancel_buttons)
    for button in cancel_buttons:
        try:
            OK_button = driver.find_element_by_css_selector("[aria-label='OK']")
            OK_button.click()
            time.sleep(random.uniform(5.0, 7.0))
        except:
            ''
        try:
            person = button.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")
            name = person.find_element_by_xpath(".//*[@role='img']").get_attribute('aria-label')
            fb_id = person.get_attribute('href').split('/')[3]
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(random.uniform(0.7, 1.3))
            button.click()
            removed_friends.append([name, fb_id])
            time.sleep(random.uniform(2.5, 3.0))
        except:
            ''
            # driver.save_screenshot("error_screenshots/" + user[1].split('@')[0] + " - " + 'delete_pending_old-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
    return removed_friends


def clear_old_pending_requests(driver, user):
    driver.get('https://www.facebook.com/friends/requests')
    removed_friends = []
    view_all_button = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'View Sent Requests')]]")))
    time.sleep(2.0)
    view_all_button.click()
    scroll = True
    time.sleep(1.0)
    try:
        load_elements_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-visualcompletion='loading-state']")))
        time.sleep(random.uniform(1.0, 2.0))
        if (len(driver.find_elements_by_css_selector("[aria-label='Cancel Request']")) == 0):
            scroll = False
    except:
        scroll = False
    while scroll:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", load_elements_div)
            time.sleep(random.uniform(1.0, 2.0))
        except Exception as e:
            scroll = False
    cancel_buttons = driver.find_elements_by_css_selector("[aria-label='Cancel Request']")
    random.shuffle(cancel_buttons)
    for button in cancel_buttons:
        try:
            OK_button = driver.find_element_by_css_selector("[aria-label='OK']")
            OK_button.click()
            time.sleep(random.uniform(5.0, 7.0))
        except:
            ''
        try:
            person = button.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")
            name = person.find_element_by_xpath(".//*[@role='img']").get_attribute('aria-label')
            fb_id = person.get_attribute('href').split('/')[3]
            if (request_check.check_age(fb_id, user)):
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(random.uniform(0.7, 1.3))
                button.click()
                removed_friends.append([name, fb_id])
                time.sleep(random.uniform(2.5, 3.0))
        except:
            ''
    return removed_friends


def invite_new_friends_to_page(driver, user, recent_friends_added):
    driver.get('https://m.facebook.com/send_page_invite/?pageid=' + user[8] + '&reference=msite_friends_inviter_card')
    invited_friends = []
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Invite Friends')]]")))
    time.sleep(1.0)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(3.5, 4.5))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    invite_buttons = driver.find_elements_by_xpath("//button[@value='Invite']")
    random.shuffle(invite_buttons)
    for button in invite_buttons:
        try:
            person = button.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_xpath('..').find_element_by_xpath(".//a[contains(@href, '/')]")
            try:
                name = person.find_element_by_xpath(".//h1").get_attribute('innerHTML')
            except:
                name = person.find_element_by_xpath(".//h3").get_attribute('innerHTML')
            fb_id = person.get_attribute('href').replace('https://m.facebook.com/', '')
            if (request_check.is_from_fountn(fb_id, user)):
                button.click()
                invited_friends.append([name, fb_id])
                time.sleep(random.uniform(2.7, 3.3))
        except Exception as e:
            ''
    return invited_friends


def read_all_messages(driver, user):
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to_window(driver.window_handles[1])
    driver.get('https://m.facebook.com/messages/?folder=unread')
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'New Message')]]")))
    time.sleep(1.0)
    unread_message_elements = driver.find_elements_by_xpath(".//a[contains(@href, '/messages/read/')]")
    unreads = []
    while (len(unread_message_elements) != 0):
        for unread in unread_message_elements:
            message_class = unread.get_attribute('class')
            if (message_class != 'touchable' and message_class != 'touchable primary'):
                unreads.append(unread.get_attribute('innerHTML'))
                unread.click()
                time.sleep(random.uniform(.75, 1.25))
                driver.execute_script("window.history.go(-1)")
                driver.refresh()
                unread_message_elements = driver.find_elements_by_xpath(".//a[contains(@href, '/messages/read/')]")
                break
            del unread
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    return unreads


def get_new_page_likes(user, driver, quota):
    time.sleep(2)
    driver.get('https://www.facebook.com/' + user[8] + '/settings/?tab=people_and_other_pages')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    time.sleep(1.0)
    friends_added = []
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'People and Other Pages')]]")))
    time.sleep(1.0)
    page_likes = driver.find_elements_by_xpath(".//a[contains(@data-hovercard, '/ajax/hovercard/user.php?id=')]")
    todays_date = datetime.date.today()
    for like in page_likes:
        if (quota > 0):
            try:
                action = ActionChains(driver)
                action.move_to_element(like).perform()
                name = like.get_attribute('innerHTML')
                time.sleep(random.uniform(3.5, 4.0))
                try:
                    try:
                        fb_id = driver.find_element_by_xpath(
                            "//a[contains(@href, '?fref=hovercard&hc_location=none')]").get_attribute('href').split(
                            '/')[3].split('?fref=')[0]
                    except:
                        fb_id = driver.find_element_by_xpath(
                            "//a[contains(@href, '&fref=hovercard&hc_location=none')]").get_attribute('href').split(
                            '/')[3].split('&fref=')[0]
                    date = like.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                        '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                        '..').find_element_by_xpath(".//abbr[@class='livetimestamp']").get_attribute('innerHTML')
                    other_date = datetime.datetime.strptime(date, '%m/%d/%y').date()
                    if (todays_date > other_date):
                        break
                    if (request_check.check_user_page(user, fb_id, date)):
                        button = driver.find_element_by_css_selector("[aria-label='Add " + name + " as a friend']")
                        button.click()
                        time.sleep(.3)
                        friends_added.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                        quota = quota - 1
                except Exception as e:
                    ''
                    # print(str(e))
                    # driver.save_screenshot("error_screenshots/" + user[1].split('@')[0] + " - " + 'add_friend_page-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
                action.move_by_offset(-150, 0).perform()
            except:
                driver.execute_script("window.scrollTo(0, 800);")
                action = ActionChains(driver)
                action.move_to_element(like).perform()
                name = like.get_attribute('innerHTML')
                time.sleep(random.uniform(3.5, 4.0))
                try:
                    try:
                        fb_id = driver.find_element_by_xpath(
                            "//a[contains(@href, '?fref=hovercard&hc_location=none')]").get_attribute('href').split(
                            '/')[3].split('?fref=')[0]
                    except:
                        fb_id = driver.find_element_by_xpath(
                            "//a[contains(@href, '&fref=hovercard&hc_location=none')]").get_attribute('href').split(
                            '/')[3].split('&fref=')[0]
                    date = like.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                        '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                        '..').find_element_by_xpath(".//abbr[@class='livetimestamp']").get_attribute('innerHTML')
                    other_date = datetime.datetime.strptime(date, '%m/%d/%y').date()
                    if (todays_date > other_date):
                        break
                    if (request_check.check_user_page(user, fb_id, date)):
                        button = driver.find_element_by_css_selector("[aria-label='Add " + name + " as a friend']")
                        button.click()
                        time.sleep(.3)
                        friends_added.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                        quota = quota - 1
                except Exception as e:
                    ''
                    # driver.save_screenshot("error_screenshots/" + user[1].split('@')[0] + " - " + 'add_friend_page-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
                action.move_by_offset(-150, 0).perform()

    driver.switch_to.default_content()
    return friends_added


def invite_new_reactions(user, driver):
    driver.get('https://m.facebook.com/notifications.php?more&targetID=' + user[8] + '&ref=bookmarks')
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Notifications')]]")))
    time.sleep(1.0)
    reactions1 = driver.find_elements_by_xpath("//span[text()[contains(., 'reacted to your')]]")
    reactions2 = driver.find_elements_by_xpath("//span[text()[contains(., 'likes your')]]")
    reactions3 = driver.find_elements_by_xpath("//span[text()[contains(., 'like your')]]")
    reactions = reactions1 + reactions2 + reactions3
    start_date = datetime.datetime.today() + datetime.timedelta(-3)
    invited_reactions = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(4.5, 5.5))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    for alert in reactions:
        link = alert.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            ".//a[@class='touchable']").get_attribute('href')
        date = alert.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            ".//abbr").get_attribute('innerHTML')
        try:
            if "seconds" in date:
                date_conv = datetime.datetime.today()
            elif "minutes" in date:
                date_conv = datetime.datetime.today()
            elif "hours" in date:
                date_conv = datetime.datetime.today()
            else:
                date_conv = parse(date)
        except:
            date_conv = datetime.datetime.today() + datetime.timedelta(-7)
        if (date_conv > start_date and len(invited_reactions) <= 30):
            try:
                invited_reactions += (invite_reactions_on_post(link, driver))
                time.sleep(random.uniform(4.0, 5.0))
            except:
                ''

    return invited_reactions


def invite_reactions_on_post(link, driver):
    driver.execute_script("window.open('', '_blank');")
    time.sleep(0.25)
    driver.switch_to_window(driver.window_handles[1])
    driver.get(link)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Comment')]]")))
    likes_link = driver.find_element_by_xpath(".//a[contains(@href, '/ufi/reaction/profile/browser/')]")
    time.sleep(random.uniform(5.0, 7.5))
    likes_link.click()
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Facebook')]]")))
    time.sleep(random.uniform(5.0, 7.5))

    invited_likes = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(4.5, 5.5))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    invite_buttons = driver.find_elements_by_xpath("//button[@value='Invite']")
    random.shuffle(invite_buttons)
    for button in invite_buttons:
        try:
            person = button.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                ".//a[contains(@href, '/')]")
            name = button.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
                ".//strong").get_attribute('innerHTML')
            fb_id = person.get_attribute('href').replace('https://m.facebook.com/', '').replace(
                '?ref=bookmarks&notif_t=page_post_reaction', '')
            button.click()
            invited_likes.append([name, fb_id])
            time.sleep(random.uniform(2.5, 3.5))
        except Exception as e:
            ''

    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    return invited_likes

def send_login_error_email(user, error):
    message = "Your Garner account failed to login because you have "
    if(error == 'two_factor'):
        message += 'two factor authentication enabled. Please either turn it off or approve it immediatley the next time Garner tries to log in. You have 3 minites from when Garner tries to log in the next time to approve the log in.'
    elif(error == 'old_pass'):
        message += 'an old password saved in Garner. Please update it on the Garner sign up at this link: https://www.englishsa.org/garner \nPlease update it soon! Your account will begin to run again as soon as you resubmit the form.'
    elif(error == 'wrong_pass'):
        message += 'the wrong password saved in Garner. Please update it on the Garner sign up at this link: https://www.englishsa.org/garner \nPlease update it soon! Your account will begin to run again as soon as you resubmit the form.'
    elif(error == 'wrong_user'):
        message += 'the wrong username saved in Garner. Please update it on the Garner sign up at this link: https://www.englishsa.org/garner \nPlease update it soon! Your account will begin to run again as soon as you resubmit the form.'
    else:
        return None
    user_info.send_message(user[1], message)
