from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
import requests
from pyowm import OWM

TELEGRAM_TOKEN = '6611113927:AAHxW5DPtPnv2LiBjsdxtmh_gZ0Be7bsXsc'
WEBEX_ACCESS_TOKEN = 'NmZlZGJkMDktZGE0Ny00OWQxLWI4YmEtMGQxMjZiMmM2ZDE2NmQwMzMxMTktMTk3_PE93_64bb227d-594d-4030-a56f-373e324be165'
WEBEX_SITE_URL = 'webexapis.com'
OPENWEATHERMAP_API_KEY = '3fdb2d7a03757ca1b310cd4a245c9355'


async def send_link_to_mentioned_users(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                       meeting_link: str) -> None:
    chat_id = update.message.chat_id

    mentioned_users = [
        user.username for user in update.message.entities
        if user.type == 'mention' and user.user.username
    ]


def get_weather():
    owm = OWM(OPENWEATHERMAP_API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place("Almaty,Kazakhstan")
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    weather_status = w.status
    return f'Текущая температура: {temperature}°C\nСостояние погоды: {weather_status}'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Отправь мне команду /newmeeting, чтобы создать новую видеоконференцию Webex.')


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

        # Получаем информацию о погоде
        weather_info = get_weather()

        # Отправляем сообщение с ссылкой на видеоконференцию и информацией о погоде
        await update.message.reply_text(
            f'Ссылка на вашу видеоконференцию: {meeting_link}\n\n{weather_info}')
    else:
        await update.message.reply_text('Произошла ошибка при создании видеоконференции.')


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newmeeting", new_meeting))

    app.run_polling()


if __name__ == 'main':
    main()