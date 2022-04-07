from selenium import webdriver
import time
import random
import decrypt
import pickle
import os
from os import path
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import save_data
import datetime


def login(driver, user):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Home']")))
        return 'success'
    except:
        try:
            username = decrypt.decrypt_key(user[2])
            password = decrypt.decrypt_key(user[3])
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "m_login_email")))
                email_box = driver.find_element_by_id('m_login_email')
                pass_box = driver.find_element_by_id('m_login_password')
            except:
                email_box = driver.find_element_by_id('email')
                pass_box = driver.find_element_by_id('pass')
            email_box.send_keys(username)
            time.sleep(random.uniform(2.0, 3.0))
            pass_box.send_keys(password)
            time.sleep(random.uniform(2.0, 3.0))
            login_button = driver.find_element_by_name('login')
            login_button.click()
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Home']")))
                return 'success'
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'Two-Factor Authentication Required')]""")
                time.sleep(180)
                return "two_factor"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'Old Password')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "old_pass"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'The password you’ve entered is incorrect.')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "wrong_pass"
            except:
                ''
            try:
                driver.find_element_by_xpath(
                    """//*[contains(text(), 'is not associated with any Facebook account.')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "wrong_user"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'match any account.')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "wrong_user"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'Your Account Is Temporarily Locked')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "locked_account"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'Your account has been disabled')]""")
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "disabled_account"
            except:
                ''
            try:
                driver.find_element_by_xpath("""//*[contains(text(), 'Please Confirm Your Identity')]""")
                user[6] = "-2"
                try:
                    os.remove(r'pickle_files/' + user[1].split('@')[0] + ".pkl")
                except:
                    ""
                return "ident_check"
            except:
                ''
        except:
            driver.save_screenshot("error_screenshots/" + user[1].split('@')[
                0] + " - " + 'login_error-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
            return 'no_login'
    return 'no_login'


def get_me(driver):
    driver.get('https://www.facebook.com/me')
    url = driver.current_url
    user_fb_info = []
    driver.execute_script("window.scrollTo(0, 500);")
    try:
        container = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@src = 'https://static.xx.fbcdn.net/rsrc.php/v3/yk/r/X_t0JnueVu-.png']")))
        driver.execute_script("arguments[0].scrollIntoView();", container)
        time.sleep(1.0)
        container = container.find_element_by_xpath('..').find_element_by_xpath('..')
        href = container.find_element_by_xpath(".//a[contains(@href, 'https://www.facebook.com/')]")
        name = href.find_element_by_xpath('.//span')
        city_text = name.get_attribute('innerHTML')
        city_id = href.get_attribute('href')
        user_fb_info = [url.split('/')[3], city_text, city_id.split('/')[3]]
    except Exception as e:
        user_fb_info = [url.split('/')[3], 'No city', 'No city']
        # print(e)
    time.sleep(2)
    try:
        container = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, 'https://www.facebook.com/" + url.split('/')[3] + "')]")))
        driver.execute_script("arguments[0].scrollIntoView();", container)
        time.sleep(3.0)
        container = container.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_xpath('..').find_element_by_xpath('..')
        last_post_obj = container.find_elements_by_xpath("//a[contains(@href, '#')]")[0]
        action = ActionChains(driver)
        action.move_to_element(last_post_obj).perform()
        time.sleep(0.5)
        last_post = ''
        if (last_post_obj.get_attribute("aria-label") == ''):
            last_post = last_post_obj.text
        else:
            last_post = last_post_obj.get_attribute("aria-label")
        user_fb_info.append(last_post)
    except:
        try:
            last_post_obj = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, 'https://www.facebook.com/" + url.split('/')[3] + "/posts/')]")))
            driver.execute_script("arguments[0].scrollIntoView();", last_post_obj)
            action = ActionChains(driver)
            action.move_to_element(last_post_obj).perform()
            if (last_post_obj.get_attribute("aria-label") == ''):
                last_post = last_post_obj.text
            else:
                last_post = last_post_obj.get_attribute("aria-label")
            user_fb_info.append(last_post)
        except:
            user_fb_info.append("no_last_post_retrieved")
    save_data.add_missionary_to_blacklist(user_fb_info[0])
    return user_fb_info


def load_driver(user):
    exe_path = r'/usr/bin/geckodriver'
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0')
    driver = webdriver.Firefox(executable_path=exe_path, firefox_profile=profile)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.get('https://www.facebook.com')
    try:
        cookies = pickle.load(open('pickle_files/' + user[1].split('@')[0] + ".pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    except:
        f = open('pickle_files/' + user[1].split('@')[0] + ".pkl", "w")
        f.close()
    # driver.get('https://www.facebook.com')

    return driver


def save_pickle(user, driver):
    with open('pickle_files/' + user[1].split('@')[0] + ".pkl", 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)
    return driver


def check_csv(user):
    user_found = True
    if (not (path.exists('friend_info/' + user[1].split('@')[0] + '.csv'))):
        with open('friend_info/' + user[1].split('@')[0] + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['name', 'fb_id', 'date', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            user_found = False

    if (not (path.exists('reversion_info/' + user[1].split('@')[0] + '.csv'))):
        with open('reversion_info/' + user[1].split('@')[0] + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            user_found = False

    if (not (path.exists('block_info/' + user[1].split('@')[0] + '.csv'))):
        with open('block_info/' + user[1].split('@')[0] + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            user_found = False

    return user_found
