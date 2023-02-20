import time
from urllib.parse import urlparse

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.translate_qr_code import get_link_qr_code
from src.check_url import check_link
from utils import TestStates
from aiogram.utils.markdown import hide_link

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
@dp.message_handler(content_types=['photo'])
async def process_start_command(message: types.Message):
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Отмена ❌'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    with open('img.png', 'rb') as file:
        await message.answer_photo(photo=file)
        await message.answer("""|----------------------------------
|<b>Приветствую тебя пользователь!</b>
|----------------------------------
|<b>Чтобы пользоваться ботом, посмотрите на список команд:</b>
|----------------------------------
|
|<b>---></b> /qr_code
|
|<b>---></b> /url
|
|<b>---></b> /help
|
|----------------------------------""", parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(commands=["qr_code"])
async def cmd_qrcode(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, "Отправь qr_code, который хочешь проверить:")


@dp.message_handler(commands=["url"])
async def cmd_url(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[1])
    await bot.send_message(message.from_user.id, "Напиши url, который хочешь проверить:")


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QRcode 🖥', 'Отмена ❌'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    with open('img_1.png', 'rb') as file:
        await message.answer_photo(photo=file)
        await message.answer(
            """
            <b>ВЫ ОБРАТИЛИСЬ ПО КОМАНДЕ /help</b>
            
1️⃣ /qrcode - при указании QRcode'а в данной команде, вы получите ссылку, а затем ссылка будет проверенна на различные факторы безопасности ссылки и затем выводиться список.
            
2️⃣ /url - при указании ссылки в данной команде, выполнится проверка на различные факторы безопасности и тут же вам выводиться список
            """, parse_mode='HTML', reply_markup=keyboard)


@dp.message_handler(Text(equals='Отправить URL 👀'))
async def processing_url(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[1])
    await bot.send_message(message.from_user.id, """
Напиши url, который хочешь проверить:
-------------------------------------------->
""")


@dp.message_handler(Text(equals='Загрузить QR_code 🖥'))
async def processing_qr_code(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, """
Отправь qr_code, который хочешь проверить:
-------------------------------------------->
""")


@dp.message_handler(Text(equals='Отмена ❌'), state=TestStates.QR_STATE[0])
async def processing_url(message: types.Message, state: FSMContext):
    await state.reset_state()
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Отмена ❌'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    with open('img.png', 'rb') as file:
        await message.answer_photo(photo=file)
        await message.answer("""|----------------------------------
    |<b>Приветствую тебя пользователь!</b>
    |----------------------------------
    |<b>Чтобы пользоваться ботом, посмотрите на список команд:</b>
    |----------------------------------
    |
    |<b>---></b> /qr_code
    |
    |<b>---></b> /url
    |
    |<b>---></b> /help
    |
    |----------------------------------""", parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(Text(equals='Отмена ❌'), state=TestStates.URL_STATE[0])
async def processing_url(message: types.Message, state: FSMContext):
    await state.reset_state()
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Отмена ❌'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    with open('img.png', 'rb') as file:
        await message.answer_photo(photo=file)
        await message.answer("""|----------------------------------
    |<b>Приветствую тебя пользователь!</b>
    |----------------------------------
    |<b>Чтобы пользоваться ботом, посмотрите на список команд:</b>
    |----------------------------------
    |
    |<b>---></b> /qr_code
    |
    |<b>---></b> /url
    |
    |<b>---></b> /help
    |
    |----------------------------------""", parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(state=TestStates.URL_STATE[0])
async def solution_url(message: types.Message, state: FSMContext):
    url = message.text
    await message.reply("""
_____________________💤💤💤_________________________
Подождите пожалуйста, идет проверка ссылки...
_____________________💤💤💤_________________________
    """, reply=False)
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.scheme + '://' + parsed_url.netloc + '/'
        result = check_link(domain)
        galochka, krestik = '✅', '❌'
        with open('img_2.png', 'rb') as file:
            await message.answer_photo(photo=file)
        card = \
            f'| Отсутствие перенаправлений: {krestik if result["redirect"] == True else galochka}\n' \
            f'| Поддержка https: {galochka if result["https"] == True else krestik}\n' \
            f'| Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
            f'| Не пародирует известные домены: {krestik if result["suspicious"] == True else galochka}\n' \
            f'| Отсутствие подозрительного JS код: {krestik if result["suspicious_js"] == True else galochka}\n' \
            f'| Нормальное количество доменных уровней: {krestik if result["Long level"] == True else galochka}\n' \
            f'| Читаемый домен: {krestik if result["Unreadability"] == True else galochka}\n'
        await message.reply(card, reply=False)
        await state.reset_state()
    except:
        try:
            parsed_url = urlparse(url)
            domain = 'http://' + parsed_url.netloc + '/'
            result = check_link(domain)
            galochka, krestik = '✅', '❌'
            with open('img_2.png', 'rb') as file:
                await message.answer_photo(photo=file)
            card = \
                f'| Отсутствие перенаправлений: {krestik if result["redirect"] == True else galochka}\n' \
                f'| Поддержка https: {galochka if result["https"] == True else krestik}\n' \
                f'| Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
                f'| Не пародирует известные домены: {krestik if result["suspicious"] == True else galochka}\n' \
                f'| Отсутствие подозрительного JS код: {krestik if result["suspicious_js"] == True else galochka}\n' \
                f'| Нормальное количество доменных уровней: {krestik if result["Long level"] == True else galochka}\n' \
                f'| Читаемый домен: {krestik if result["Unreadability"] == True else galochka}\n'
            await message.reply(card, reply=False)
            await state.reset_state()
        except:
            await message.reply("Некорректная ссылка, попробуйте снова😵", reply=False)
            await state.reset_state()


@dp.message_handler(state=TestStates.QR_STATE[0], content_types=['photo'])
async def solution_QRcode(message: types.Message, state: FSMContext):
    await message.reply("📎 Изображение скачивается... 📎 ", reply=False)
    time.sleep(1)
    await message.photo[-1].download('src/img.png')
    time.sleep(1)
    try:
        url = get_link_qr_code()
        await message.reply("""
_____________________💤💤💤_________________________
Подождите пожалуйста, идет проверка ссылки...
_____________________💤💤💤_________________________
            """, reply=False)
        time.sleep(1)
        try:
            with open('img_3.png', 'rb') as file:
                await message.answer_photo(photo=file)
                time.sleep(2)
            parsed_url = urlparse(url)
            domain = parsed_url.scheme + '://' + parsed_url.netloc + '/'
            result = check_link(domain)
            galochka, krestik = '✅', '❌'
            card = f'URL: {url}\n' \
                   f'Отсутствие перенаправлений: {krestik if result["redirect"] == True else galochka}\n' \
                   f'Поддержка https: {galochka if result["https"] == True else krestik}\n' \
                   f'Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
                   f'Не пародирует известные домены: {krestik if result["suspicious"] == True else galochka}\n' \
                   f'Отсутствие подозрительного JS код: {krestik if result["suspicious_js"] == True else galochka}\n' \
                   f'Нормальное количество доменных уровней: {krestik if result["Long level"] == True else galochka}\n' \
                   f'Читаемый домен: {krestik if result["Unreadability"] == True else galochka}\n'
            await message.reply(card, reply=False)
            await state.reset_state()
        except:
            try:
                await message.reply("""🔒 ССЫЛКА ИМЕЕТ ПРОТОКОЛ https! 🔒
⚠️ Не удалось подключиться к протоколу https ⚠️
🖥 Идёт замена протокола на http, пожалуйста подождите... 🖥""", reply=False)
                time.sleep(2)
                parsed_url = urlparse(url)
                domain = 'http://' + parsed_url.netloc + parsed_url.path
                result = check_link(domain)
                galochka, krestik = '✅', '❌'
                card = f'URL: {domain}\n' \
                       f'Отсутствие перенаправлений: {krestik if result["redirect"] == True else galochka}\n' \
                       f'Поддержка https: {galochka if result["https"] == True else krestik}\n' \
                       f'Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
                       f'Не пародирует известные домены: {krestik if result["suspicious"] == True else galochka}\n' \
                       f'Отсутствие подозрительного JS код: {krestik if result["suspicious_js"] == True else galochka}\n' \
                       f'Нормальное количество доменных уровней: {krestik if result["Long level"] == True else galochka}\n' \
                       f'Читаемый домен: {krestik if result["Unreadability"] == True else galochka}\n'
                await message.reply(card, reply=False)
                await state.reset_state()
            except:
                await message.reply("⚠️ Ссылка в QR-коде некорректная... ⚠️", reply=False)
                await state.reset_state()
    except:
        await message.reply(
            """
------------------------------------

                     ⚠️⚠️⚠️
                     
<b>НЕ УДАЛОСЬ РАСПОЗНАТЬ QR-КОД</b>

<b>Причиной может быть:</b>

1️⃣ - Плохое качество картинки

2️⃣ - QR-кода недействителен

3️⃣ - Недопустимый формат шифрования QR-кода

------------------------------------
            """, parse_mode='HTML', reply=False)
        await state.reset_state()


if __name__ == '__main__':
    executor.start_polling(dp)
