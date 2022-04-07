import user_options
import login
import save_data
import random
import request_check


################################################################################################################################################################################user_report###################################################################################################################################################################################
#['user', 'setting', 'status', 'page', 'message', 'login', 'city', 'new_friends', 'friends_messaged', 'pending_cleared', 'groups', 'friends_invited_to_like_page', 'last_post', 'unread_messages', 'acceptance_ratio', 'people_you_may_know_3_mon', 'block_3_mon', 'penaly_added', 'quota', 'sent_requests_friends', 'sent_requests_groups', 'sent_requests_page', 'people_you_may_know', 'block']#
##############################################################################################################################################################################################################################################################################################################################################################################

def message_only(user, driver):
    final_message = ''
    user_report = ['N/A'] * 24
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: Message Only' + '\n'
    user_report[0] = user[1]  # user
    user_report[1] = user[5]  # setting
    user_report[2] = user[6]  # status
    user_report[3] = user[8]  # page
    user_report[4] = user[4]  # message
    if (int(user[6]) == 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Not blocked\n'
        login_error = login.login(driver, user)
        user_report[5] = login_error  # login
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if(user_found):
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                save_data.update_messaged_friends(user, friends_messaged)
                user_report[8] = friends_messaged  # friends_messaged
                invited_friends = []
                if (user[8] != 'None' and user[8] != ''):
                    final_message += 'Inviting Friends to Page: ' + str(user[8]) + '\n'
                    invited_friends = user_options.invite_new_friends_to_page(driver, user, recent_friends_added)
                    final_message += 'Friends invited to like page: ' + str(invited_friends) + '\n'
                user_report[11] = invited_friends  # friends_invited_to_like_page
                if (request_check.has_requests_to_clear(user) and random.randint(0, 5) > 3):
                    user_report[9] = 'y'  # pending_cleared
                    canceled_friend_requests = user_options.clear_old_pending_requests(driver, user)
                    final_message += str(len(canceled_friend_requests)) + " Canceled pending requests: " + str(canceled_friend_requests) + '\n'
                    save_data.update_canceled_requests(user, canceled_friend_requests)
                else:
                    user_report[10] = 'n'  # pending_cleared
                    canceled_friend_requests = []
                    final_message += 'No requests to cancel' + '\n'
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) > 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Blocked ' + str(user[6]) + ' days' + '\n'
        login_error = login.login(driver, user)
        user_report[5] = login_error
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                new_friends = user_options.get_new_friends(driver, user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                user_report[8] = friends_messaged  # friends_messaged
                save_data.update_messaged_friends(user, friends_messaged)
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif (int(user[6]) < 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Super Blocked ' + user[6] + ' days' + '\n'
    else:
        final_message += 'Wait until password/username update\n'
    print(final_message)
    return user_report

def off(user):
    final_message = ''
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: Off' + '\n'
    user_report = ['Off'] * 24
    user_report[0] = user[1]
    print(final_message)
    return user_report

def home(user):
    final_message = ''
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: Home' + '\n'
    user_report = ['Home'] * 24
    user_report[0] = user[1]
    save_data.delete_user(user)
    user[6] = 'home'
    print(final_message)
    return user_report

def groups(user, driver):
    final_message = ''
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: Groups' + '\n'
    user_report = ['N/A'] * 24
    user_report[0] = user[1]  # user
    user_report[1] = user[5]  # setting
    user_report[2] = user[6]  # status
    user_report[3] = user[8]  # page
    user_report[4] = user[4]  # message
    if(int(user[6]) == 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Not blocked' + '\n'
        login_error = login.login(driver, user)
        user_report[5] = login_error  # login
        if(login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if(user_found):
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                save_data.update_messaged_friends(user, friends_messaged)
                user_report[8] = friends_messaged # friends_messaged
                if(request_check.has_requests_to_clear(user) and random.randint(0,5) > 3):
                    user_report[9] = 'y'  # pending_cleared
                    canceled_friend_requests = user_options.clear_old_pending_requests(driver, user)
                    final_message += str(len(canceled_friend_requests)) + " Canceled pending requests: " + str(canceled_friend_requests) + '\n'
                    save_data.update_canceled_requests(user, canceled_friend_requests)
                else:
                    user_report[9] = 'n'  # pending_cleared
                    canceled_friend_requests = []
                    final_message += 'No requests to cancel' + '\n'
                invited_friends = []
                if(user[8] != 'None'):
                    final_message += 'Inviting Friends to Page: ' + str(user[8]) + '\n'
                    invited_friends = user_options.invite_new_friends_to_page(driver, user, recent_friends_added)
                    final_message += 'Friends invited to like page: ' + str(invited_friends) + '\n'
                user_report[11] = invited_friends  # friends_invited_to_like_page
                quota_data = request_check.generate_quota(user, user_fb_data, driver)
                final_message += 'last post:' +str( quota_data[1]) + ';unread messages:' + str(quota_data[2]) + ';Acceptance Ratio:' + str(quota_data[3]) + ';People you may Know:' + str(quota_data[4]) + ';Blocks:' + str(quota_data[5]) + ';Low Request Penalty:' + str(quota_data[6]) + '\n'
                user_report[12] = quota_data[1]  # last_post
                user_report[13] = quota_data[2]  # unread_messages
                user_report[14] = quota_data[3]  # acceptance_ratio
                user_report[15] = quota_data[4]  # people_you_may_know_3_mon
                user_report[16] = quota_data[5]  # block_3_mon
                user_report[17] = quota_data[6]*(2/3)  # penalty_added
                quota = quota_data[0]
                quota = round(quota*(2/3))
                user_report[18] = quota  # quota
                user_report[19] = []  # sent_requests_friends
                final_message += 'Quota: ' + str(quota) + '\n'
                group_friends = []
                blocked_info_group = ''
                if (quota > 0):
                    group_friends_info = user_options.friend_by_group(driver, quota)
                    final_message += 'Users Groups: ' + str(len(group_friends_info[2])) + '\n'
                    user_report[10] = group_friends_info[2]  # groups
                    group_friends = group_friends_info[0]
                    blocked_info_group = group_friends_info[1]
                    if(blocked_info_group != ''):
                        if(blocked_info_group == 'people_you_may_know'):
                            final_message += 'Account blocked. Info: ' + str(blocked_info_group) + '\n'
                            save_data.add_reversion(user)
                            quota = 0
                            user[6] = "1"
                            save_data.add_reversion(user)
                            user_report[22] = 1  # people_you_may_know
                            user_report[23] = 0  # block
                        else:
                            final_message += 'Account blocked Info: ' + str(blocked_info_group) + '\n'
                            save_data.add_block(user)
                            quota = 0
                            user[6] = "3"
                            save_data.add_block(user)
                            user_report[22] = 0  # people_you_may_know
                            user_report[23] = 1  # block
                    else:
                        quota = quota - len(group_friends)
                    final_message += str(len(group_friends)) + " Sent Requests: " + str(group_friends) + '\n'
                    final_message += "Requests Left: " + str(quota) + '\n'
                    save_data.add_friend_user(user, group_friends)
                    save_data.add_friend_master(user, group_friends)
                user_report[20] = group_friends  # sent_requests_groups
                user_report[21] = []  # sent_requests_page
                if(blocked_info_group == ''):
                    user_report[22] = 0  # people_you_may_know
                    user_report[23] = 0  # block
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) > 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Blocked ' + user[6] + ' days' + '\n'
        user[6] = str(int(user[6]) - 1)
        login_error = login.login(driver, user)
        user_report[5] = login_error
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                user_report[8] = friends_messaged  # friends_messaged
                save_data.update_messaged_friends(user, friends_messaged)
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) < 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Super Blocked ' + user[6] + ' days' + '\n'
        user[6] = str(int(user[6]) + 1)
    else:
        final_message += 'Wait until password/username update\n'
    print(final_message)
    return user_report

def on(user, driver):
    final_message = ''
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: On' + '\n'
    user_report = ['N/A'] * 24
    user_report[0] = user[1]  # user
    user_report[1] = user[5]  # setting
    user_report[2] = user[6]  # status
    user_report[3] = user[8]  # page
    user_report[4] = user[4]  # message
    if (int(user[6]) == 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Not blocked' + '\n'
        login_error = login.login(driver, user)
        user_report[5] = login_error  # login
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                save_data.update_messaged_friends(user, friends_messaged)
                user_report[8] = friends_messaged  # friends_messaged
                if (request_check.has_requests_to_clear(user) and random.randint(0, 5) > 3):
                    canceled_friend_requests = user_options.clear_old_pending_requests(driver, user)
                    user_report[9] = 'y'  # pending_cleared
                    final_message += str(len(canceled_friend_requests)) + " Canceled pending requests: " + str(canceled_friend_requests) + '\n'
                else:
                    canceled_friend_requests = []
                    user_report[9] = 'n'  # pending_cleared
                    final_message += 'No requests to cancel' + '\n'
                save_data.update_canceled_requests(user, canceled_friend_requests)
                invited_friends = []
                if (user[8] != 'None' and user[8] != ''):
                    final_message += 'Inviting Friends to Page: ' + str(user[8]) + '\n'
                    invited_friends = user_options.invite_new_friends_to_page(driver, user,recent_friends_added)
                    final_message += 'Friends invited to like page: ' + str(invited_friends) + '\n'
                user_report[11] = invited_friends  # friends_invited_to_like_page
                quota_data = request_check.generate_quota(user, user_fb_data, driver)
                final_message += 'last post:' +str( quota_data[1]) + ';unread messages:' + str(quota_data[2]) + ';Acceptance Ratio:' + str(quota_data[3]) + ';People you may Know:' + str(quota_data[4]) + ';Blocks:' + str(quota_data[5]) + ';Low Request Penalty:' + str(quota_data[6]) + '\n'
                user_report[12] = str(quota_data[1])  # last_post
                #final_message += 'Last Post: ' + str(quota_data[1]) + '\n'
                user_report[13] = quota_data[2]  # unread_messages
                #final_message += 'Unread Messages: ' + str(quota_data[2]) + '\n'
                user_report[14] = quota_data[3]  # acceptance_ratio
                #final_message += 'Acceptance Ratio: ' + str(quota_data[3]) + '\n'
                user_report[15] = quota_data[4]  # people_you_may_know_3_mon
                #final_message += 'People you may Know: ' + str(quota_data[4]) + '\n'
                user_report[16] = quota_data[5]  # block_3_mon
                #final_message += 'Blocks: ' + str(quota_data[5]) + '\n'
                user_report[17] = quota_data[6]  # penalty_added
                #final_message += 'Low Request Penalty: ' + str(quota_data[6]) + '\n'
                quota = quota_data[0]
                user_report[18] = quota  # quota
                final_message += 'Quota: ' + str(quota) + '\n'
                new_page_likes = []
                if (quota > 0 and user[8] != 'None' and user[8] != ''):
                    new_page_likes = user_options.get_new_page_likes(user, driver, quota)
                    final_message += str(len(new_page_likes)) + " Sent Page Requests: " + str(new_page_likes) + '\n'
                    save_data.add_friend_user_page(user, new_page_likes)
                    save_data.add_friend_master(user, new_page_likes)
                    quota = quota - len(new_page_likes)
                user_report[21] = new_page_likes  # sent_requests_page
                friend_friends = []
                blocked_info_friend = ''
                if (quota > 0):
                    friend_friends_info = user_options.friend_by_friend(user, driver, quota)
                    friend_friends = friend_friends_info[0]
                    blocked_info_friend = friend_friends_info[1]
                    if (blocked_info_friend != ''):
                        if (blocked_info_friend == 'people_you_may_know'):
                            final_message += 'Account blocked. Info: ' + str(blocked_info_friend) + '\n'
                            save_data.add_reversion(user)
                            quota = 0
                            user[6] = "1"
                            save_data.add_reversion(user)
                            user_report[22] = 1  # people_you_may_know
                            user_report[23] = 0  # block
                        else:
                            final_message += 'Account blocked Info: ' + str(blocked_info_friend) + '\n'
                            save_data.add_block(user)
                            quota = 0
                            user[6] = "3"
                            save_data.add_block(user)
                            user_report[22] = 0  # people_you_may_know
                            user_report[23] = 1  # block
                    else:
                        quota = quota - len(friend_friends)
                    final_message += str(len(friend_friends)) + " Sent Friends of Friends Requests: " + str(friend_friends) + '\n'
                    final_message += "Requests Left: " + str(quota) + '\n'
                    save_data.add_friend_user(user, friend_friends)
                    save_data.add_friend_master(user, friend_friends)
                user_report[19] = friend_friends  # sent_requests_friends
                group_friends = []
                blocked_info_group = ''
                if(quota > 0):
                    group_friends_info = user_options.friend_by_group(driver, quota)
                    final_message += 'Users Groups: ' + str(len(group_friends_info[2])) + '\n'
                    user_report[10] = group_friends_info[2]  # groups
                    group_friends = group_friends_info[0]
                    blocked_info_group = group_friends_info[1]
                    if (blocked_info_group != ''):
                        if (blocked_info_group == 'people_you_may_know'):
                            final_message += 'Account blocked. Info: ' + str(blocked_info_group) + '\n'
                            save_data.add_reversion(user)
                            quota = 0
                            user[6] = "1"
                            save_data.add_reversion(user)
                            user_report[22] = 1  # people_you_may_know
                            user_report[23] = 0  # block
                        else:
                            final_message += 'Account blocked Info: ' + str(blocked_info_group) + '\n'
                            save_data.add_block(user)
                            quota = 0
                            user[6] = "3"
                            save_data.add_block(user)
                            user_report[22] = 0  # people_you_may_know
                            user_report[23] = 1  # block
                    else:
                        quota = quota - len(group_friends)
                    final_message += str(len(group_friends)) + " Sent Group Requests: " + str(group_friends) + '\n'
                    final_message += "Requests Left: " + str(quota) + '\n'
                    save_data.add_friend_user(user, group_friends)
                    save_data.add_friend_master(user, group_friends)
                user_report[20] = group_friends  # sent_requests_groups
                user_report[21] = []  # sent_requests_page
                if (blocked_info_group == ''):
                    user_report[22] = 0  # people_you_may_know
                    user_report[23] = 0  # block
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) > 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Blocked ' + str(user[6]) + ' days' + '\n'
        user[6] = str(int(user[6]) - 1)
        login_error = login.login(driver, user)
        user_report[5] = login_error
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                user_report[8] = friends_messaged  # friends_messaged
                save_data.update_messaged_friends(user, friends_messaged)
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if (login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) < 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Super Blocked ' + user[6] + ' days' + '\n'
        user[6] = str(int(user[6]) + 1)
    else:
        final_message += 'Wait until password/username update\n'
    print(final_message)
    return user_report


def pages(user, driver):
    final_message = ''
    user_report = ['N/A'] * 24
    final_message += 'User Email: ' + str(user[1]) + '\n'
    final_message += 'State: Pages' + '\n'
    final_message += 'Page: ' + str(user[8]) + '\n'
    user_report[0] = user[1]  # user
    user_report[1] = user[5]  # setting
    user_report[2] = user[6]  # status
    user_report[3] = user[8]  # page
    user_report[4] = user[4]  # message
    user_report[10] = 'N/A'  # groups
    user_report[11] = 'N/A'  # friends_invited_to_like_page
    user_report[19] = 'N/A'  # sent_requests_friends
    user_report[20] = 'N/A'  # sent_requests_groups
    if (int(user[6]) == 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Not blocked' + '\n'
        login_error = login.login(driver, user)
        user_report[5] = login_error  # login
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                save_data.update_messaged_friends(user, friends_messaged)
                user_report[8] = friends_messaged  # friends_messaged
                if (request_check.has_requests_to_clear(user) and random.randint(0, 5) > 3):
                    canceled_friend_requests = user_options.clear_old_pending_requests(driver, user)
                    user_report[9] = 'y'  # pending_cleared
                    final_message += str(len(canceled_friend_requests)) + " Canceled pending requests: " + str(canceled_friend_requests) + '\n'
                else:
                    canceled_friend_requests = []
                    user_report[9] = 'n'  # pending_cleared
                    final_message += 'No requests to cancel' + '\n'
                save_data.update_canceled_requests(user, canceled_friend_requests)
                invited_reactions = user_options.invite_new_reactions(user, driver)
                final_message += str(len(invited_reactions)) + ' Reactions invited to like page: ' + str(invited_reactions) + '\n'
                quota_data = request_check.generate_quota(user, user_fb_data, driver)
                final_message += 'last post:' +str( quota_data[1]) + ';unread messages:' + str(quota_data[2]) + ';Acceptance Ratio:' + str(quota_data[3]) + ';People you may Know:' + str(quota_data[4]) + ';Blocks:' + str(quota_data[5]) + ';Low Request Penalty:' + str(quota_data[6]) + '\n'
                user_report[12] = quota_data[1]  # last_post
                #final_message += 'Last Post: ' + str(quota_data[1]) + '\n'
                user_report[13] = quota_data[2]  # unread_messages
                #final_message += 'Unread Messages: ' + str(quota_data[2]) + '\n'
                user_report[14] = quota_data[3]  # acceptance_ratio
                #final_message += 'Acceptance Ratio: ' + str(quota_data[3]) + '\n'
                user_report[15] = quota_data[4]  # people_you_may_know_3_mon
                #final_message += 'People you may Know: ' + str(quota_data[4]) + '\n'
                user_report[16] = quota_data[5]  # block_3_mon
                #final_message += 'Blocks: ' + str(quota_data[5]) + '\n'
                user_report[17] = quota_data[6]  # penalty_added
                #final_message += 'Low Request Penalty: ' + str(quota_data[6]) + '\n'
                quota = quota_data[0]
                user_report[18] = quota  # quota
                final_message += 'Quota: ' + str(quota) + '\n'
                new_page_likes = []
                if(quota > 0):
                    new_page_likes = user_options.get_new_page_likes(user, driver, quota)
                    final_message += str(len(new_page_likes)) + " Sent Page Requests: " + str(new_page_likes) + '\n'
                    save_data.add_friend_user_page(user, new_page_likes)
                    save_data.add_friend_master(user, new_page_likes)
                    quota = quota - len(new_page_likes)
                user_report[21] = new_page_likes  # sent_requests_page
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if(login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif(int(user[6]) > 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Blocked ' + str(user[6]) + ' days' + '\n'
        user[6] = str(int(user[6]) - 1)
        login_error = login.login(driver, user)
        user_report[5] = login_error
        if (login_error == 'success'):
            user_found = login.check_csv(user)
            login.save_pickle(user, driver)
            user_fb_data = login.get_me(driver)
            user_report[6] = user_fb_data[2]  # city
            final_message += 'User FB Info: ' + str(user_fb_data) + '\n'
            if (user_found):
                new_friends = user_options.get_new_friends(driver ,user)
                final_message += 'New friends full List: ' + str(new_friends) + '\n'
                recent_friends_added = save_data.update_added_friends(user, new_friends)
                user_report[7] = recent_friends_added  # new_friends
                final_message += str(len(recent_friends_added)) + ' New friends: ' + str(recent_friends_added) + '\n'
                unmessaged_friends = save_data.get_unmessaged_friends(user)
                friends_messaged = user_options.send_messages_new_friends(user, driver, unmessaged_friends)
                final_message += str(len(friends_messaged)) + ' friends messaged: ' + str(friends_messaged) + '\n'
                user_report[8] = friends_messaged  # friends_messaged
                save_data.update_messaged_friends(user, friends_messaged)
            else:
                removed_users = user_options.clear_all_pending_requests(driver, user)
                final_message += str(len(removed_users)) + " Pending requests cleared: " + str(removed_users) + '\n'
                user_report[5] = 'new_user_init'  # login
                if (user[7] == 'Yes'):
                    read_messages = user_options.read_all_messages(driver, user)
                    final_message += 'Messages read: ' + str(read_messages) + '\n'
                    user[7] = 'No'
                final_message += "New User Initialization Complete" + '\n'
        else:
            if(login_error != "ident_check"):
                login.save_pickle(user, driver)
            else:
                final_message += "Pickle Deleted" + '\n'
            user_options.send_login_error_email(user, login_error)
            user[9] = 'Yes'
            final_message += 'Login Error: ' + str(login_error) + '\n'
    elif (int(user[6]) < 0 and str(user[9]) != "Yes"):
        final_message += 'Status: Super Blocked ' + user[6] + ' days' + '\n'
        user[6] = str(int(user[6]) + 1)
    else:
        final_message += 'Wait until password/username update\n'
    print(final_message)
    return user_report