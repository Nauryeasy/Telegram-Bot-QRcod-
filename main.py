from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.tranlete_qr_code import get_link_qr_code
from src.check_url import check_link
from utils import TestStates

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    start_button_1, start_button_2 = 'Отправить URL 👀', 'Загрузить QR_code 🖥'  # , 'Отмена ❌'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    # keyboard.add(start_button_3)

    await message.reply("Привет!\nТебя приветствует бот для проверки ссылок и QR_Cods!\n(Да, да, эт я)",
                        reply_markup=keyboard)


@dp.message_handler(Text(equals='Отправить URL 👀'))
async def processing_url(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[1])
    await bot.send_message(message.from_user.id, "Напиши url, который хочешь проверить:")


@dp.message_handler(Text(equals='Загрузить QR_code 🖥'))
async def processing_qr_code(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, "Отправь qr_code, который хочешь проверить:")


@dp.message_handler(Text(equals='Отмена ❌'))
async def processing_url(message: types.Message, state: FSMContext):
    await state.reset_state()


@dp.message_handler(state=TestStates.URL_STATE[0])
async def solution_url(message: types.Message, state: FSMContext):
    url = message.text
    await message.reply("Подождите пожалуйста, идет проверка ссылки...", reply=False)
    try:
        result = check_link(url)
        galochka, krestik = '✅', '❌'
        card = f'Перенаправления: {galochka if result["redirect"] == True else krestik}\n' \
               f'Поддержка https: {galochka if result["https"] == True else krestik}\n' \
               f'Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
               f'Пародирование известных доменов: {galochka if result["suspicious"] == True else krestik}\n' \
               f'Подозрительный JS код: {galochka if result["suspicious_js"] == True else krestik}\n' \
               f'Чрезмерно длинных домен: {galochka if result["Long level"] == True else krestik}\n' \
               f'Нечитаемый домен: {galochka if result["Unreadability"] == True else krestik}\n'
        await message.reply(card, reply=False)
        await state.reset_state()
    except:
        await message.reply("Некорректная ссылка, попробуйте снова😵", reply=False)
        await state.reset_state()


@dp.message_handler(state=TestStates.QR_STATE[0], content_types=['photo'])
async def solution_QRcode(message: types.Message, state: FSMContext):
    await message.reply("Изображение скачивается...", reply=False)
    await message.photo[-1].download('src/img.png')
    try:
        url = get_link_qr_code()
        await message.reply("Подождите пожалуйста, идет проверка ссылки...", reply=False)
        try:
            result = check_link(url)
            galochka, krestik = '✅', '❌'
            card = f'Перенаправления: {galochka if result["redirect"] == True else krestik}\n' \
                   f'Поддержка https: {galochka if result["https"] == True else krestik}\n' \
                   f'Наличие SSL сертификата: {galochka if result["ssl"] == True else krestik}\n' \
                   f'Пародирование известных доменов: {galochka if result["suspicious"] == True else krestik}\n' \
                   f'Подозрительный JS код: {galochka if result["suspicious_js"] == True else krestik}\n' \
                   f'Чрезмерно длинных домен: {galochka if result["Long level"] == True else krestik}\n' \
                   f'Нечитаемый домен: {galochka if result["Unreadability"] == True else krestik}\n'
            await message.reply(card, reply=False)
            await state.reset_state()
        except:
            await message.reply("Некорректная ссылка, попробуйте снова😵", reply=False)
            await state.reset_state()
    except:
        await message.reply("Простите, не удалось прочитать qr_code, попробуйте снова😵", reply=False)
        await state.reset_state()


if __name__ == '__main__':
    executor.start_polling(dp)
