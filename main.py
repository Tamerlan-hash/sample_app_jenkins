from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
import requests

TELEGRAM_TOKEN = '6898158317:AAGW_WCZ5LoaAyxuxl5r2b0pMIfFdJ-XUOs'
WEBEX_ACCESS_TOKEN = 'OWNkMWVlMzctOTIzYy00NTQ0LTkyNTMtMjFjNWYwYmJiMTg4MWNmYmU2YzItNjNh_PE93_64bb227d-594d-4030-a56f-373e324be165'
WEBEX_SITE_URL = 'webexapis.com'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне команду /newmeeting, чтобы создать новую видеоконференцию Webex.')


async def new_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Authorization': f'Bearer {WEBEX_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    data = {
        "title": "Новая Видеоконференция",
        "start": (datetime.now() + timedelta(minutes=1)).strftime(date_format),
        "end": (datetime.now() + timedelta(minutes=60)).strftime(date_format)
    }

    response = requests.post(f'https://{WEBEX_SITE_URL}/v1/meetings', headers=headers, json=data)
    if response.status_code == 200:
        meeting_link = response.json()['webLink']
        await update.message.reply_text(f'Ссылка на вашу видеоконференцию: {meeting_link}')
    else:
        await update.message.reply_text('Произошла ошибка при создании видеоконференции.')


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newmeeting", new_meeting))

    app.run_polling()


if __name__ == '__main__':
    main()
