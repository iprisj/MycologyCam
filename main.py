#! /usr/bin/python3
from email import message
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import random
import string
import cv2
import time


config = json.load(open('config.json'))

telegramId = config["telegramId"]
app = Updater(config["token"])
app.start_polling(poll_interval=0.1)
dispatcher = app.dispatcher

cam = cv2.VideoCapture(config["cameraIndex"])


def screenshot(sendTelegram:False):
    if cam.isOpened():
        suc, content = cam.read()
        name = "screenshots/" + ''.join(random.choices(string.ascii_uppercase, k=8)) + ".png"
        print(name)
        cv2.imwrite(name, content)
        if sendTelegram:
            app.bot.send_photo(config["updateTelegramId"], open(name, "rb"))
        return suc, name
    else:
        return False, False

def upload_image(update: Update, context: CallbackContext) -> None:
    if not update.message.from_user.id == telegramId:
        return update.message.reply_text('Who are you bruv?')
    res, frame = screenshot(False)
    if res:
        update.message.reply_photo(open(frame, "rb"))
    else:
        update.message.reply_text('Error getting Camera')

def eval_cmd(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == telegramId:
        eval(' '.join(context.args))



dispatcher.add_handler(CommandHandler("screenshot", upload_image))
dispatcher.add_handler(CommandHandler("eval", eval_cmd))

dispatcher.add_handler(CommandHandler("hello", lambda update, context: 
    update.message.reply_text(f'Hello {update.effective_user.first_name}')
))
dispatcher.add_handler(CommandHandler("whoami", lambda update, context: 
    update.message.reply_text(update.message.from_user.id)
))


while False:
    screenshot(True)
    time.sleep(60 * 60)
