import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config.telegram_bot_token)
dp = Dispatcher(bot)

def get_weather_samara():
    city = 'Самара'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.openweather_token}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = requests.get(url)
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather_desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']

        return (
            f"Погода в {city_name}, {country}: \n"
            f"Описание: {weather_desc} ℃ (ощущается как {feels_like}) \n"
            f"Влажность: {humidity}% \n"
            f"Скорость ветра: {wind_speed} м/c"
        )
    else:
        return 'Не удалось получить данные о погоде'

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет, Я бот, который может показывать погоду в Самаре \n'
                        'Чтобы узнать погоду воспользуйтесь командой Start')

@dp.message_handler(commands = ['help'])
async def send_help(message: types.Message):
    help_text = ('Список доступных комманд: ')
    await message.reply(help_text)

@dp.message_handler(commands = ['weather'])
async def send_weather(message: types.Message):
    weather_info = get_weather_samara()
    await message.reply(weather_info, Parse_Mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)