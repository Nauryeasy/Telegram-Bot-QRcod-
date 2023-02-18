from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .src.check_url import check_link
from utils import TestStates

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    start_buttons = ['Отправить URL 👀', 'Загрузить QR_code 🖥']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_buttons)

    await message.reply("Привет!\nТебя приветствует бот для проверки ссылок и QR_Cods!\n(Да, да, эт я)", reply_markup=keyboard)


@dp.message_handler(Text(equals='Отправить URL 👀'))
async def processing_url(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, "Напиши url, который хочешь проверить:")


@dp.message_handler(Text(equals='Загрузить QR_code 🖥'))
async def processing_qr_code(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[1])
    await bot.send_message(message.from_user.id, "Отправь qr_code, который хочешь проверить:")


@dp.message_handler(state=TestStates.URL_STATE[0])
async def second_test_state_case_met(message: types.Message):
    url = message.text
    result = check_link(url)
    await bot.send_message(f"{result['https']}")


@dp.message_handler(state=TestStates.QR_STATE[0])
async def second_test_state_case_met(message: types.Message):
    await message.reply('Второй!', reply=False)

if __name__ == '__main__':
    executor.start_polling(dp)