from config import *
from src.translate_qr_code import get_link_qr_code
from src.check_url import check_link


@dp.message_handler(commands=['start'])
@dp.message_handler(content_types=['photo'])
async def process_start_command(message: types.Message):
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Назад ↩️'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    await message.answer('🔄 <b> БОТ Information Defender </b> - ЗАПУСКАЕТСЯ, ПОЖАЛУЙСТА, ПОДОЖДИТЕ... 🔄', parse_mode='HTML')
    with open('img.png', 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
        await message.answer(
            """
|----------------------------------
|<b>Приветствую тебя пользователь!</b>
|----------------------------------
|<b>Посмотрите на список команд:</b>
|----------------------------------
|
|<b>---> /start - Запуск бота </b> 🖥
|
|<b>---> /qr_code - Проверка QR </b> 💾
|
|<b>---> /url - Проверка url </b> 💾
|
|<b>---> /help - Помощь </b> 🔧
|
|----------------------------------
            """, parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(commands=["qr_code"])
async def cmd_qrcode(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, "💾Отправь <b>QR-код</b>, который хочешь проверить: 💾",
                           parse_mode='HTML')


@dp.message_handler(commands=["url"])
async def cmd_url(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[1])
    await bot.send_message(message.from_user.id, "💾 Напиши <b>URL</b>, который хочешь проверить: 💾", parse_mode='HTML')


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QRcode 🖥', 'Назад ↩️'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    with open('img_1.png', 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
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
💾 Напиши <b>URL</b>, который хочешь проверить: 💾
""", parse_mode='HTML')


@dp.message_handler(Text(equals='Загрузить QR_code 🖥'))
async def processing_qr_code(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.all()[0])
    await bot.send_message(message.from_user.id, """
💾Отправь <b>QR-код</b>, который хочешь проверить: 💾
""", parse_mode='HTML')


@dp.message_handler(Text(equals='Назад ↩️'), state=TestStates.QR_STATE[0])
async def processing_qr_code(message: types.Message, state: FSMContext):
    await state.reset_state()
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Назад ↩️'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    await message.answer('🔄 <b>ИДЁТ ПЕРЕНАПРАВЛЕНИЕ НА ГЛАВНОЕ ОКНО, ПОЖАЛУЙСТА, ПОДОЖДИТЕ...</b> 🔄', parse_mode='HTML')
    with open('img.png', 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
        await message.answer(
            """
|----------------------------------
|<b>Приветствую тебя пользователь!</b>
|----------------------------------
|<b>Посмотрите на список команд:</b>
|----------------------------------
|
|<b>---> /start - Запуск бота </b> 🖥
|
|<b>---> /qr_code - Проверка QR </b> 💾
|
|<b>---> /url - Проверка url </b> 💾
|
|<b>---> /help - Помощь </b> 🔧
|
|----------------------------------
            """, parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(Text(equals='Назад ↩️'), state=TestStates.URL_STATE[0])
async def processing_url(message: types.Message, state: FSMContext):
    await state.reset_state()
    start_button_1, start_button_2, start_button_3 = 'Отправить URL 👀', 'Загрузить QR_code 🖥', 'Назад ↩️'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button_1)
    keyboard.add(start_button_2)
    keyboard.add(start_button_3)
    await message.answer('🔄 <b>ИДЁТ ПЕРЕНАПРАВЛЕНИЕ НА ГЛАВНОЕ ОКНО, ПОЖАЛУЙСТА, ПОДОЖДИТЕ...</b> 🔄', parse_mode='HTML')
    with open('img.png', 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
        await message.answer(
            """
|----------------------------------
|<b>Приветствую тебя пользователь!</b>
|----------------------------------
|<b>Посмотрите на список команд:</b>
|----------------------------------
|
|<b>---> /start - Запуск бота </b> 🖥
|
|<b>---> /qr_code - Проверка QR </b> 💾
|
|<b>---> /url - Проверка url </b> 💾
|
|<b>---> /help - Помощь </b> 🔧
|
|----------------------------------
            """, parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(state=TestStates.URL_STATE[0])
async def solution_url(message: types.Message, state: FSMContext):
    url = message.text
    await message.reply("""
_________________________________________________
🔻                                           🔻                                     🔻
                                            
 Пожалуйста, подождите, идет проверка ссылки...
   
🔺                                           🔺                                     🔺                                  
_________________________________________________
    """, reply=False)
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.scheme + '://' + parsed_url.netloc + '/'
        result = check_link(domain)
        galochka, krestik = '✅', '❌'
        with open('img_2.png', 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
        card = \
            f'|-----------------------------------\n' \
            f'|\n' \
            f'|<b>----> URL:</b> {url}\n' \
            f'|\n' \
            f'|<b>----> Отсутствие перенаправлений:</b> {krestik if result["redirect"] == True else galochka}\n' \
            f'|\n' \
            f'|<b>----> Поддержка https:</b> {galochka if result["https"] == True else krestik}\n' \
            f'|\n' \
            f'|<b>----> Наличие SSL сертификата:</b> {galochka if result["ssl"] == True else krestik}\n' \
            f'|\n' \
            f'|<b>----> Не пародирует известные домены:</b> {krestik if result["suspicious"] == True else galochka}\n' \
            f'|\n' \
            f'|<b>----> Отсутствие подозрительного JS код:</b> {krestik if result["suspicious_js"] == True else galochka}\n' \
            f'|\n' \
            f'|<b>----> Нормальное количество доменных уровней:</b> {krestik if result["Long level"] == True else galochka}\n' \
            f'|\n' \
            f'|<b>----> Читаемый домен:</b> {krestik if result["Unreadability"] == True else galochka}\n' \
            f'|\n' \
            f'|----------------------------------'
        await message.reply(card, reply=False)
        await state.reset_state()
    except:
        try:
            parsed_url = urlparse(url)
            domain = 'http://' + parsed_url.netloc + '/'
            result = check_link(domain)
            galochka, krestik = '✅', '❌'
            with open('img_2.png', 'rb') as file:
                file.seek(0)
                await message.answer_photo(photo=file)
                file.close()
                await message.reply(
                    """
🔒 <b> ССЫЛКА ИМЕЕТ ПРОТОКОЛ https! </b> 🔒
⚠️ <b> Не удалось подключиться к протоколу https </b> ⚠️
🖥 <b> Идёт замена протокола на http... 🖥</b>
                    """, parse_mode='HTML', reply=False)
                time.sleep(2)
            card = \
                f'|-----------------------------------\n' \
                f'|\n' \
                f'|<b>----> URL:</b> {domain}\n' \
                f'|\n' \
                f'|<b>----> Отсутствие перенаправлений:</b> {krestik if result["redirect"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Поддержка https:</b> {galochka}\n' \
                f'|\n' \
                f'|<b>----> Наличие SSL сертификата:</b> {galochka if result["ssl"] == True else krestik}\n' \
                f'|\n' \
                f'|<b>----> Не пародирует известные домены:</b> {krestik if result["suspicious"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Отсутствие подозрительного JS код:</b> {krestik if result["suspicious_js"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Нормальное количество доменных уровней:</b> {krestik if result["Long level"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Читаемый домен:</b> {krestik if result["Unreadability"] == True else galochka}\n' \
                f'|\n' \
                f'|----------------------------------'
            await message.reply(card, parse_mode="HTML", reply=False)
            await state.reset_state()
        except:
            await message.reply(
                """
|-------------------------------------------------
|
|                                  ⚠️⚠️⚠️
|                     
|--<b>🔴НЕ УДАЛОСЬ РАСПОЗНАТЬ URL🔴</b>--
|
|          <b>◼️ Причиной может быть: ◼️</b>
|
|---> 1️⃣ - Не существующий домен
|
|---> 2️⃣ - Не указан протокол подключения
|
|---> 3️⃣ - Ссылка является локальной
|
|--------------------------------------------------
                """, parse_mode='HTML', reply=False)
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
_________________________________________________
🔻                                           🔻                                     🔻
                                            
 Пожалуйста, подождите, идет проверка ссылки...
   
🔺                                           🔺                                     🔺                                  
_________________________________________________
            """, reply=False)
        time.sleep(1)
        try:
            with open('img_3.png', 'rb') as file:
                file.seek(0)
                await message.answer_photo(photo=file)
                file.close()
                time.sleep(2)
            parsed_url = urlparse(url)
            domain = parsed_url.scheme + '://' + parsed_url.netloc + '/'
            result = check_link(domain)
            galochka, krestik = '✅', '❌'
            card = \
                f'|-----------------------------------\n' \
                f'|\n' \
                f'|<b>----> URL:</b> {url}\n' \
                f'|\n' \
                f'|<b>----> Отсутствие перенаправлений:</b> {krestik if result["redirect"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Поддержка https:</b> {galochka if result["https"] == True else krestik}\n' \
                f'|\n' \
                f'|<b>----> Наличие SSL сертификата:</b> {galochka if result["ssl"] == True else krestik}\n' \
                f'|\n' \
                f'|<b>----> Не пародирует известные домены:</b> {krestik if result["suspicious"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Отсутствие подозрительного JS код:</b> {krestik if result["suspicious_js"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Нормальное количество доменных уровней:</b> {krestik if result["Long level"] == True else galochka}\n' \
                f'|\n' \
                f'|<b>----> Читаемый домен:</b> {krestik if result["Unreadability"] == True else galochka}\n' \
                f'|\n' \
                f'|----------------------------------'
            await message.reply(card, reply=False)
            await state.reset_state()
        except:
            try:
                time.sleep(2)
                parsed_url = urlparse(url)
                domain = 'http://' + parsed_url.netloc + parsed_url.path
                result = check_link(domain)
                galochka, krestik = '✅', '❌'
                await message.reply(
                    """
🔒 <b> ССЫЛКА ИМЕЕТ ПРОТОКОЛ https! </b> 🔒
⚠️ <b> Не удалось подключиться к протоколу https </b> ⚠️
🖥 <b> Идёт замена протокола на http... 🖥</b>
                    """, parse_mode='HTML', reply=False)
                time.sleep(2)
                card = \
                    f'|-----------------------------------\n' \
                    f'|\n' \
                    f'|<b>----> URL:</b> {domain}\n' \
                    f'|\n' \
                    f'|<b>----> Отсутствие перенаправлений:</b> {krestik if result["redirect"] == True else galochka}\n' \
                    f'|\n' \
                    f'|<b>----> Поддержка https:</b> {galochka}\n' \
                    f'|\n' \
                    f'|<b>----> Наличие SSL сертификата:</b> {galochka if result["ssl"] == True else krestik}\n' \
                    f'|\n' \
                    f'|<b>----> Не пародирует известные домены:</b> {krestik if result["suspicious"] == True else galochka}\n' \
                    f'|\n' \
                    f'|<b>----> Отсутствие подозрительного JS код:</b> {krestik if result["suspicious_js"] == True else galochka}\n' \
                    f'|\n' \
                    f'|<b>----> Нормальное количество доменных уровней:</b> {krestik if result["Long level"] == True else galochka}\n' \
                    f'|\n' \
                    f'|<b>----> Читаемый домен:</b> {krestik if result["Unreadability"] == True else galochka}\n' \
                    f'|\n' \
                    f'|----------------------------------'
                await message.reply(card, reply=False)
                await state.reset_state()
            except:
                await message.reply("⚠️ Ссылка в QR-коде некорректная... ⚠️", reply=False)
                await state.reset_state()
    except:
        await message.reply(
            """
|-------------------------------------------------
|
|                                        ⚠️⚠️⚠️
|                     
|--<b>🔴НЕ УДАЛОСЬ РАСПОЗНАТЬ QR-КОД🔴</b>--
|
|                <b>◼️ Причиной может быть: ◼️</b>
|
|---> 1️⃣ - Плохое качество картинки
|
|---> 2️⃣ - QR-кода недействителен
|
|---> 3️⃣ - Недопустимый формат шифрования QR-кода
|
|--------------------------------------------------
            """, parse_mode='HTML', reply=False)
        await state.reset_state()


if __name__ == '__main__':
    executor.start_polling(dp)
