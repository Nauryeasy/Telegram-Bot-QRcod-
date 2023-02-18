from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    start_buttons = ['Отправить URL 👀', 'Загрузить QR_code 🖥']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_buttons)

    await message.reply("Привет!\nТебя приветствует бот для проверки ссылок и QR_Cods!\n(Да, да, эт я)")


@dp.message_handler(Text(equals='Отправить URL 👀'))
async def process_start_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Напиши url, который хочешь проверить:")
    current_state = await state.get_state()


@dp.message_handler(Text(equals='Загрузить QR_code 🖥'))
async def process_start_command(message: types.Message, state: FSMContext):
    pass