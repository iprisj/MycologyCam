from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import string
import cv2
import time, threading

cam = cv2.VideoCapture(0)
def screenshot():
    if cam.isOpened():
        suc, content = cam.read()
        name = "screenshots/" + ''.join(random.choices(string.ascii_uppercase, k=8)) + ".png"
        cv2.imwrite(name, content)
        return suc, name
    else:
        return False

async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.from_user.id == 2128522398:
        return update.message.reply_text('Who are you bruv?')
    res, frame = screenshot()
    if res:
        await update.message.reply_photo(open(frame, "rb"))
    else:
        await update.message.reply_text('Error getting Camera')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.from_user.id)

app = ApplicationBuilder().token("5778310826:AAEhVKOGVYvO2YfUH3KwS8fM0Kv2ukLZzzU").build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("screenshot", upload_image))
app.add_handler(CommandHandler("whoami", whoami))
app.run_polling()

def periodically_take_screenshot():
    screenshot()
    threading.Timer(60 * 60, periodically_take_screenshot).start()
periodically_take_screenshot()