#!/usr/bin/env python3
import user_info
import save_data
import login
import user_status_options
import concurrent.futures
import datetime
from func_timeout import func_timeout, FunctionTimedOut
import random
import time
from settings import MyGlobals


def shuffle_under_seed(ls, seed):
  random.seed(seed)
  random.shuffle(ls)
  return ls

def unshuffle_list(shuffled_ls, seed):
  n = len(shuffled_ls)
  perm = [i for i in range(1, n + 1)]
  shuffled_perm = shuffle_under_seed(perm, seed)
  zipped_ls = list(zip(shuffled_ls, shuffled_perm))
  zipped_ls.sort(key=lambda x: x[1])
  return [a for (a, b) in zipped_ls]


def init_test():
    print("test mode")
    logs = open("runs.txt", "a")
    logs.write("start:" + datetime.datetime.today().strftime("%Y-%m-%d") + " " + datetime.datetime.today().strftime(
        '%H:%M:%S') + '\n')
    logs.write("  Test Run\n")
    user_data = MyGlobals.user_data
    seed = random.randint(0, 2000)
    user_data = shuffle_under_seed(user_data, seed)
    print('Run type: ' + "Test Run")
    print('{0} users retrieved.'.format(len(user_data)))
    print('User order: ')
    for num, name in enumerate(user_data, start=1):
        print("User {}: {}".format(num, name[1]))
    print('\n')
    user_report = []
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for user in user_data:
            futures.append(executor.submit(user_loop, user))
        for future in concurrent.futures.as_completed(futures):
            try:
                user_future = future.result()
                user_report.append(user_future)
            except Exception as e:
                print(e)
    user_data = unshuffle_list(user_data, seed)
    print("User Report: \n")
    print(user_report)
    print("\n")
    logs = open("runs.txt", "a")
    logs.write("end:" + datetime.datetime.today().strftime("%Y-%m-%d") + " " + datetime.datetime.today().strftime(
        '%H:%M:%S') + "\n")
    logs.write("--------------------------\n")
    logs.close()


def init():
    logs = open("runs.txt", "a")
    logs.write("start:" + datetime.datetime.today().strftime("%Y-%m-%d") + " " + datetime.datetime.today().strftime(
        '%H:%M:%S') + '\n')
    status = save_data.check_master_csv()
    logs.write("  " + str(status) + "\n")
    logs.close()
    user_data = user_info.get_user_info()
    current_missionaries = user_info.get_blacklist()
    seed = random.randint(0,2000)
    user_data = shuffle_under_seed(user_data, seed)
    if (int(status) == 0):
        run_type = "full"
    else:
        run_type = "message"
    print('Run type: ' + status + " - " + run_type)
    print('{0} users retrieved.'.format(len(user_data)))
    print('User order: ')
    for num, name in enumerate(user_data, start=1):
        print("User {}: {}".format(num, name[1]))
    print('\n')
    user_report = []
    futures = []
    time.sleep(random.uniform(0.0, 1800.0))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        if (int(status) == 0):
            for user in user_data:
                futures.append(executor.submit(user_loop, user))
        else:
            for user in user_data:
                futures.append(executor.submit(message_only_loop, user))
        for future in concurrent.futures.as_completed(futures):
            try:
                user_future = future.result()
                user_report.append(user_future)
            except:
                ''
    user_data = unshuffle_list(user_data, seed)
    updated_missionaires = save_data.get_missionary_blacklist()
    user_info.set_user_info(user_data)
    user_info.upload_missionary_blacklist(updated_missionaires)
    save_data.generate_daily_report(user_report)
    user_info.upload_daily_report()
    user_info.upload_screen_shots()
    logs = open("runs.txt", "a")
    logs.write("end:" + datetime.datetime.today().strftime("%Y-%m-%d") + " " + datetime.datetime.today().strftime(
        '%H:%M:%S') + "\n")
    logs.write("--------------------------\n")
    logs.close()


def message_only_loop(user):
    user_run_info = ['N/A'] * 24
    user_run_info[0] = user[1]
    user_run_info[1] = user[5]
    user_run_info[2] = user[6]
    user_run_info[3] = user[8]
    user_run_info[4] = user[4]
    if (user[5] != 'Off' and user[5] != "Home"):
        driver = login.load_driver(user)
        try:
            if(not(MyGlobals.test_mode)):
                time.sleep(random.uniform(20.0, 40.0))
            user_run_info = func_timeout(900, user_status_options.message_only, args=(user, driver))
        except FunctionTimedOut:
            print('User Timeout: ' + user[1] + '\n')
            user_run_info[5] = 'timed_out'
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
            try:
                driver.save_screenshot("error_screenshots/" + user[1].split('@')[
                    0] + " - " + 'general_error-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
            except:
                ''
    elif (user[5] == 'Off'):
        user_run_info = ['Off'] * 24
        user_run_info[0] = user[1]
        final_message = ''
        final_message += 'User Email: ' + str(user[1]) + '\n'
        final_message += 'State: Off' + '\n'
        print(final_message)
    elif (user[5] == 'Home'):
        user_run_info = ['Home'] * 24
        user_run_info[0] = user[1]
        final_message = ''
        final_message += 'User Email: ' + str(user[1]) + '\n'
        final_message += 'State: Home' + '\n'
        print(final_message)
    try:
        driver.close()
    except:
        ""
    return user_run_info


def user_loop(user):
    user_run_info = ['N/A'] * 24
    user_run_info[0] = user[1]
    user_run_info[1] = user[5]
    user_run_info[2] = user[6]
    user_run_info[3] = user[8]
    user_run_info[4] = user[4]
    if (user[5] == 'Off'):
        try:
            user_run_info = user_status_options.off(user)
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
    elif (user[5] == 'Home'):
        try:
            user_run_info = user_status_options.home(user)
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
    elif (user[5] == 'Groups'):
        driver = login.load_driver(user)
        try:
            if (not(MyGlobals.test_mode)):
                time.sleep(random.uniform(20.0, 40.0))
            user_run_info = func_timeout(900, user_status_options.groups, args=(user, driver))
        except FunctionTimedOut:
            print('User Timeout: ' + user[1] + '\n')
            user_run_info[5] = 'timed_out'
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
            try:
                driver.save_screenshot("error_screenshots/" + user[1].split('@')[
                    0] + " - " + 'general_error-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
            except:
                ''
    elif (user[5] == 'On'):
        driver = login.load_driver(user)
        try:
            if (not(MyGlobals.test_mode)):
                time.sleep(random.uniform(20.0, 40.0))
            user_run_info = func_timeout(900, user_status_options.on, args=(user, driver))
        except FunctionTimedOut:
            print('User Timeout: ' + user[1] + '\n')
            user_run_info[5] = 'timed_out'
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
            try:
                driver.save_screenshot("error_screenshots/" + user[1].split('@')[
                    0] + " - " + 'general_error-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
            except:
                ''
    elif (user[5] == 'Pages'):
        driver = login.load_driver(user)
        try:
            if (not(MyGlobals.test_mode)):
                time.sleep(random.uniform(20.0, 40.0))
            user_run_info = func_timeout(900, user_status_options.pages, args=(user, driver))
        except FunctionTimedOut:
            print('User Timeout: ' + user[1] + '\n')
            user_run_info[5] = 'timed_out'
        except Exception as e:
            print('User Failed: ' + user[1])
            print(e)
            print('\n')
            try:
                driver.save_screenshot("error_screenshots/" + user[1].split('@')[
                    0] + " - " + 'general_error-' + datetime.datetime.today().strftime('%H:%M:%S') + ".png")
            except:
                ''
    try:
        driver.close()
    except:
        ''
    return user_run_info


if __name__ == '__main__':
    if (MyGlobals.test_mode):
        init_test()
    else:
        init()

