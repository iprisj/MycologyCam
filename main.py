import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import string
import cv2
import time, threading


config = json.load(open('config.json'))

telegramId = config["telegramId"]
app = ApplicationBuilder().token(config["token"]).build()

cam = cv2.VideoCapture(0)
async def screenshot():
    if cam.isOpened():
        suc, content = cam.read()
        name = "screenshots/" + ''.join(random.choices(string.ascii_uppercase, k=8)) + ".png"
        cv2.imwrite(name, content)
        return suc, name
    else:
        return False

async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.from_user.id == telegramId:
        return update.message.reply_text('Who are you bruv?')
    res, frame = await screenshot()
    if res:
        await update.message.reply_photo(open(frame, "rb"))
    else:
        await update.message.reply_text('Error getting Camera')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.from_user.id)

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("screenshot", upload_image))
app.add_handler(CommandHandler("whoami", whoami))
app.run_polling()