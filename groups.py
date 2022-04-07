import time
import datetime
import random
import request_check
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_user_groups(driver):
    driver.get('https://m.facebook.com/groups_browse/your_groups/')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Groups')]]")))
    time.sleep(random.uniform(1.0, 2.0))

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(random.uniform(2.0, 4.5))

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    groups = driver.find_elements_by_xpath("//a[contains(@href, '/groups/')]")
    user_groups_array = []
    for group in groups:
        text = ''
        try:
            text = group.text.split('\n')[0]
        except:
            text = group.text
        user_groups_array.append([text, group.get_attribute('href').replace('m.facebook.com', 'www.facebook.com').replace('?ref=group_browse', '')])
    #print('User Groups: ' + str(user_groups_array))
    random.shuffle(user_groups_array)
    return user_groups_array

def members_near_me(driver, group_url, quota):
    driver.get(group_url + 'members/near_you')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Members')]]")))
    time.sleep(random.uniform(1.0, 2.0))

    # Get scroll height
    error_data = ''
    last_height = driver.execute_script("return document.body.scrollHeight")
    added_member_info = []
    requests_sent = 0
    time.sleep(random.uniform(3.0, 5.0))
    continue_scroll = True
    while continue_scroll:
        members = driver.find_elements_by_css_selector("[aria-label='Add Friend']")
        random.shuffle(members)
        for member in members:
            if (requests_sent < quota):
                try:
                    container = member.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
                    href = ''
                    name = ''
                    link = ''
                    fb_id = ''
                    try:
                        href = container.find_element_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")
                        name = href.text
                        link = href.get_attribute('href')
                        fb_id = link.split('/')[3]
                    except:
                        href = container.find_element_by_xpath(".//a[contains(@href, '/user/')]")
                        name = href.text
                        link = href.get_attribute('href')
                        fb_id = link.split('/')[6]
                        driver.execute_script("window.open('', '_blank');")
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(random.uniform(1.0, 2.2))
                        driver.get('https://www.facebook.com/' + fb_id + '/')
                        fb_id = driver.current_url.split('/')[3]
                        time.sleep(random.uniform(0.1, 0.7))
                        driver.close()
                        driver.switch_to_window(driver.window_handles[0])
                    button = member
                    if (not(request_check.check_user(fb_id))):
                        button.click()
                        time.sleep(0.2)
                        try:
                            reverted_button = driver.find_element_by_css_selector("[aria-label='OK']")
                            try:
                                message = driver.find_element_by_xpath("""//*[contains(text(), 'What is "People You May Know"?')]""")
                                if (error_data == ''):
                                    error_data = '1'
                                    #print('First Warning')
                                if (error_data == '1'):
                                    error_data = 'people_you_may_know'
                                    #print('Final Warning')
                                    continue_scroll = False
                                time.sleep(random.uniform(3.0,3.5))
                                reverted_button.click()
                            except:
                                error_data = 'account_blocked'
                                time.sleep(3.0)
                                reverted_button.click()
                                continue_scroll = False
                        except:
                            added_member_info.append([name, fb_id, datetime.date.today().strftime('%d/%m/%Y')])
                            requests_sent += 1
                            time.sleep(random.uniform(3.0, 3.5))
                    else:
                        continue_scroll = False
                        break
                except Exception as e:
                    ''
            else:
                continue_scroll = False
                break

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(3.0, 5.0))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(3)
    return [added_member_info, error_data]

def current_city(user, driver, fb_id, quota):
    driver.get('https://www.facebook.com/' + fb_id + '/friends_current_city')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Friends')]]")))
    time.sleep(random.uniform(3.0, 5.0))
    # Get scroll height
    error_data = ''
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_members_len = len(driver.find_elements_by_css_selector("[aria-label='Friends']"))
    last_members_len = 0
    added_member_info = []
    requests_sent = 0
    time.sleep(random.uniform(3.0, 5.0))
    continue_scroll = True
    while continue_scroll:
        members = driver.find_elements_by_css_selector("[aria-label='Add Friend']")
        random.shuffle(members)
        new_members = []
        for member in members:
            try:
                container = member.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')  # .find_element_by_xpath('..')
                mutual_friends = container.find_element_by_xpath(".//span[contains(text(), 'mutual')]").text
                num_mutual_friends = int(mutual_friends.split(' ')[0])
                href = container.find_elements_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")[1]#.text
                name_span = href.find_element_by_xpath(".//span")
                name = name_span.get_attribute('innerHTML')
                link = href.get_attribute('href')
                fb_id = link.split('/')[3]
                new_members.append([member, num_mutual_friends, name, fb_id])
            except Exception as e:
                ''
        new_members = sorted(new_members, key=lambda x: x[1], reverse=True)
        for member in new_members:
            try:
                button = member[0]
                if (requests_sent < quota):
                    if (not (request_check.check_user(fb_id)) and (member[2] != "")):
                        button.click()
                        time.sleep(0.2)
                        try:
                            reverted_button = driver.find_element_by_css_selector("[aria-label='OK']")
                            try:
                                message = driver.find_element_by_xpath("""//*[contains(text(), 'What is "People You May Know"?')]""")
                                if (error_data == ''):
                                    error_data = '1'
                                if (error_data == '1'):
                                    error_data = 'people_you_may_know'
                                    continue_scroll = False
                                time.sleep(2.0)
                                reverted_button.click()
                            except:
                                error_data = 'account_blocked'
                                time.sleep(3.0)
                                reverted_button.click()
                                continue_scroll = False
                        except:
                            added_member_info.append([member[2], member[3], datetime.date.today().strftime('%d/%m/%Y')])
                            requests_sent += 1
                            time.sleep(random.uniform(3.0, 3.5))
                else:
                    continue_scroll = False
                    break
            except Exception as e:
                ''
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(3.0, 5.0))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        new_members_len = len(driver.find_elements_by_css_selector("[aria-label='Friends']"))
        if new_members_len == last_members_len:
            break
        last_members_len = new_members_len

    time.sleep(3)
    return [added_member_info, error_data]