import logging
from config import Config
from bot import updater, dp, browser
from telegram.ext import CommandHandler, run_async
from telegram import ChatAction
import os
import pickle
import time
from os import execl
from sys import executable
import csv
import datetime

meeting_list = list()

def convertTime(string_time):
    hour = string_time.split(':')[0]
    minute = string_time.split(':')[1]

    datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'
    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

    return datetime_object


class Meeting():
    def __init__(self, day, time, link):
        self.time = convertTime(time)
        self.link = link

def getTodayMeetings():
    try:
        with open('bot/meet.csv') as file:
            read = csv.reader(file, delimiter=',')
            meet_count = 0
            for row in read:
                meet_count += 1
                if row[0] == datetime.datetime.today().strftime('%A'):
                    meeting = Meeting(row[0], row[1], row[2])
                    meeting_list.append(meeting)
    except:
        print("Google meet schedule not found. Run schedule.py to add schedule.")

def meet(context):
    logging.info("DOING")
    userId = 451311925
    def students(context):
        number = browser.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]').text
        print(number)
        if(int(number) <10):
            context.bot.send_message(chat_id=userId, text="Your Class has ended!")
            browser.quit()
            execl(executable, executable, "chromium.py")
    try:
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
        usernameStr = Config.GUSERNAME
        passwordStr = Config.GPASSWORD
        url_meet = context.job.context
        print(url_meet)


        if os.path.exists("meet.pkl"):
            cookies = pickle.load(open("meet.pkl", "rb"))
            browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            for cookie in cookies:
                browser.add_cookie(cookie)
        else:
            browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            username = browser.find_element_by_id('identifierId')
            username.send_keys(usernameStr)
            nextButton = browser.find_element_by_id('identifierNext')
            nextButton.click()
            time.sleep(7)

            browser.save_screenshot("ss.png")
            context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
            mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
            os.remove('ss.png')

            password = browser.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
            password.send_keys(passwordStr)
            signInButton = browser.find_element_by_id('passwordNext')
            signInButton.click()
            time.sleep(7)

            if(browser.find_elements_by_xpath('//*[@id="authzenNext"]/div/button/div[2]')):
                context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
                context.bot.send_message(chat_id=userId, text="Need Verification. Please Verify")
                browser.find_element_by_xpath('//*[@id="authzenNext"]/div/button/div[2]').click()
                time.sleep(5)

                browser.save_screenshot("ss.png")
                context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
                mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
                os.remove('ss.png')
                time.sleep(20)

            browser.get('https://meet.google.com')
            time.sleep(7)   

            pickle.dump( browser.get_cookies() , open("meet.pkl","wb"))
            context.bot.send_message(chat_id=userId, text="Logged In!")

        browser.get(url_meet)
        time.sleep(3)   

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid  = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), caption="Test", timeout = 120).message_id
        os.remove('ss.png')

        if(browser.find_elements_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div')):
            browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div').click()
            time.sleep(3)

            context.bot.delete_message(chat_id=userId,message_id = mid)

            browser.save_screenshot("ss.png")
            context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
            mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
            os.remove('ss.png')
        try:
            browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]").click()
            time.sleep(10)
        except:
            browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]").click()
            time.sleep(10)

        context.bot.delete_message(chat_id=userId ,message_id = mid)

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')
        time.sleep(5)

        context.bot.delete_message(chat_id=userId ,message_id = mid)
        time.sleep(10)

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')

        context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=userId, text="Attending you lecture. You can chill :v")
        logging.info("STAAAAPH!!")
    except Exception as e:
        browser.quit()
        context.bot.send_message(chat_id=userId, text="Error occurred! Fix error and retry!")
        context.bot.send_message(chat_id=userId, text=str(e))

    j = updater.job_queue
    j.run_repeating(students, 1000, 20)
    # except:
    #     print("NICE")

def mJobQueue():
    logging.info("Adding Google Meet meetings to schedule")
    getTodayMeetings()

    j = updater.job_queue
    
    for row in meeting_list:
        secs = (row.time - datetime.datetime.now()).total_seconds()
        if(secs > 0):
            print(secs)
            j.run_once(meet, secs, context=row.link)

