import logging
import os
import pickle
from telegram.ext import CommandHandler, Job, run_async
from telegram import ChatAction
from config import Config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from os import execl
from sys import executable
from bot import updater, dp, browser, restricted


from bot.zoom import zoom

if Config.SCHEDULE == True:
    from bot.meet_schedule import mJobQueue, timeTable
    from bot.zoom_schedule import zJobQueue

userId = Config.USERID


@run_async
def exit(update, context):
    context.bot.send_message(chat_id=userId, text="Restarting bot, Please wait!")
    browser.quit()
    execl(executable, executable, "chromium.py")


@run_async
def status(update, context):
    browser.save_screenshot("ss.png")
    context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120)
    os.remove('ss.png')


@run_async
def start(update, context):
    userId = Config.USERID
    user_id = update.effective_user.id
    if user_id != int(userId):
        print("Unauthorized access denied for {0}. Allowed users: {1}".format(user_id, userId))
        context.bot.send_message(chat_id=user_id,
                                 text="You are not authorized to use this bot! Make your own zoom member bot contact @alpha_romeo_06")
        return
    else:
          context.bot.send_message(chat_id=user_id,
                                 text='''now you was auth by my owner welcome to zoom bot you can attend zoom meetings by this bot !
                                  join multiple zoom members by this  bot contact @alpha_romeo_06 or use /help''')

@run_async
def help(update, context):
    context.bot.send_message(chat_id=userId, text="""
/zoom <userID> <password>  
you dont have premium pack to use count mode
/count <number> now curently disabled by @alpha_romeo_06
/exit -   Exit the meeting and restart
/status -   Send screenshot
/help -   Send this help message""")


def main():
    j = updater.job_queue

    dp.add_handler(CommandHandler("zoom", zoom))
    

    if Config.SCHEDULE == True:
        mJobQueue()
        zJobQueue()
        dp.add_handler(CommandHandler("timetable", timeTable))

    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    logging.info("Bot started")

    updater.start_polling()

if __name__ == '__main__':
    main()
