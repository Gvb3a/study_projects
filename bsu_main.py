import fitz
import requests

from urllib3 import disable_warnings
from os import remove
from datetime import datetime
from colorama import init, Fore, Style
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.client.session.aiohttp import AiohttpSession

from bsu_sql import sql_launch, sql_language, sql_saved_message, sql_change_language

init()
# код в комментариях предназначен для pythonanywhere(онлайн-хостинг)
# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot('bot_token')
# bot = Bot('bot_token', session=session)
dp = Dispatcher()


def start_keyboard(l):  # функция для start inline-keyboard (в зависимости от языка)
    # l - язык пользователя. 0 - русский, 1 - белорусский
    inline_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=['Расписание занятий студентов дневного отделения',
                                    'Расклад заняткаў студэнтаў дзённага аддзялення'][l], callback_data='inline_day')],
        [InlineKeyboardButton(text=['Расписание занятий ДО студентов дневного отделения',
                                    'Расклад заняткаў ДН студэнтаў дзённага аддзялення'][l], callback_data='inline_dist')],
        [InlineKeyboardButton(text=['Расписание зачетов студентов дневного отделения',
                                    'Расклад залікаў студэнтаў дзённага аддзялення'][l], callback_data='inline_exam')],
        [InlineKeyboardButton(text=['Расписание консультаций и экзаменов студентов дневного отделения',
                                    'Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення'][l], callback_data='inline_session')]
    ])
    return inline_start_keyboard


def inline_button(path, speciality):  # генерация однотипных inline кнопок
    inline_list = []
    for i in range(4):
        inline_list.append(InlineKeyboardButton(text=f'{i+1} курс', callback_data=f'{path}{i+1}_{speciality}'))
    return inline_list


def create_inline_keyboard(l, path):
    # расписания хранятся по следующему пути:
    # https://philology.bsu.by/files/dnevnoe/{тип расписания}/{курс}_{специальность}.pdf
    inline_belarusian_philology = [InlineKeyboardButton(text=['Белорусская филология', 'Беларуская філалогія'][l],
                                                        callback_data='text')]
    inline_russian_philology = [InlineKeyboardButton(text=['Русская филология', 'Руская філалогія'][l],
                                                     callback_data='text')]
    inline_slavic_philology = [InlineKeyboardButton(text=['Славянская филология', 'Славянская філалогія'][l],
                                                    callback_data='text')]
    inline_classical_philology = [InlineKeyboardButton(text=['Классическая  филология', 'Класічная  філалогія'][l],
                                                       callback_data='text')]
    # на классической филологии только один набор
    inline_classical_philology_3 = [InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_klassiki')]
    inline_romano_germanic_philology = [InlineKeyboardButton(text=['Романо-германская филология', 'Рамана-германская філалогія'][l],
                                                             callback_data='text')]
    inline_oriental_philology = [InlineKeyboardButton(text=['Восточная филология', 'Усходняя філалогія'][l],
                                                      callback_data='text')]
    inline_back = [InlineKeyboardButton(text='Назад', callback_data='back')]

    inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
    inline_belarusian_philology,
    inline_button(path, 'bel'),
    inline_russian_philology,
    inline_button(path, 'rus'),
    inline_slavic_philology,
    inline_button(path, 'slav'),
    inline_classical_philology,
    inline_classical_philology_3,
    inline_romano_germanic_philology,
    inline_button(path, 'rom-germ'),
    inline_oriental_philology,
    inline_button(path, 'vost'),
    inline_back
    ])
    return inline_keyboard


@dp.message(CommandStart())  # Обработчик команды /start. Вызывает меню выбора типа расписания
async def command_start_handler(message: Message) -> None:
    l = sql_language(message.from_user.id)  # из базы данных узнаем язык пользователя
    await message.answer(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит Ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць Ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))
    print(f'{Fore.RED}/start{Style.RESET_ALL} by {Fore.BLUE}{message.from_user.first_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.callback_query(F.data == 'inline_day')
async def inline_day_handler(callback: CallbackQuery):
    l = sql_language(callback.from_user.id)
    await callback.message.edit_text(
        text=['Расписание занятий студентов дневного отделения (ІІ семестр) 2023-2024. Выберете специальность',
              'Расклад заняткаў студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'raspisanie/'))
    await callback.answer()


@dp.callback_query(F.data == 'inline_dist')
async def inline_dist_handler(callback: CallbackQuery):
    l = sql_language(callback.from_user.id)
    await callback.message.edit_text(
        text=['Расписание занятий (дистанционное обучение) студентов дневного отделения (ІІ семестр) 2023-2024. Выберете специальность',
              'Расклад заняткаў (дыстанцыйнае навучанне) студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'USRDO/'))
    await callback.answer()


@dp.callback_query(F.data == 'inline_exam')
async def inline_exam_handler(callback: CallbackQuery):
    l = sql_language(callback.from_user.id)
    await callback.message.edit_text(
        text=['Расписание зачетов студентов дневного отделения (І семестр) 2023-2024. Выберете специальность',
              'Расклад залікаў студэнтаў дзённага аддзялення (І семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'zachet/'))
    await callback.answer()


@dp.callback_query(F.data == 'inline_session')
async def inline_session_handler(callback: CallbackQuery):
    l = sql_language(callback.from_user.id)
    await callback.message.edit_text(
        text=['Расписание консультаций и экзаменов студентов дневного отделения (І семестр 2023-2024). Выберете специальность',
              'Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення (І семестр 2023-2024). Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'sesia/'))
    await callback.answer()


@dp.callback_query(F.data == 'text')
async def inline_text(callback: CallbackQuery):
    await callback.answer(text=['Это исключительно декоративная кнопка', 'Гэта выключна дэкаратыўная кнопка'][sql_language(callback.from_user.id)])


@dp.callback_query(F.data == 'back')
async def inline_back_fuc(callback: CallbackQuery):
    l = sql_language(callback.from_user.id)
    await callback.message.edit_text(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит Ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць Ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))
    await callback.answer()


@dp.callback_query(F.data)
async def process_callback_data(callback: types.CallbackQuery):
    name = callback.from_user.first_name
    link = callback.data
    await main(link, callback.from_user.id, callback.id)
    await callback.answer()
    sql_saved_message(callback.from_user.username, callback.from_user.id, link)
    print(f'{Fore.GREEN}{link}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.message(Command('language'))
async def command_language(message: Message) -> None:
    await message.answer(['Язык был изменен', 'Мова была зменена'][sql_change_language(message.from_user.id)])
    print(f'{Fore.RED}/language{Style.RESET_ALL} by {Fore.BLUE}{message.from_user.first_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.message()
async def main_handler(message: types.Message) -> None:
    name = message.from_user.first_name
    user_id = message.from_user.id
    link = sql_saved_message(name, user_id, 0)
    await main(link, user_id, message.message_id)
    print(f'{Fore.GREEN}{link}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


async def main(data, user_id, message_id):
    l = sql_language(user_id)
    try:
        disable_warnings()
        response = requests.get(f'https://philology.bsu.by/files/dnevnoe/{data}.pdf', verify=False)
        name = data[data.rfind('/')+1:]

        with open(f'{name}_{message_id}.pdf', 'wb') as file:
            file.write(response.content)

        doc = fitz.open(f'{name}_{message_id}.pdf')
        photos = []
        count = len(doc)
        for i in range(count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"{name}_{message_id}_{i + 1}.png")
            photos.append(InputMediaPhoto(media=FSInputFile(f"{name}_{message_id}_{i + 1}.png")))
        doc.close()

        await bot.send_media_group(user_id, media=photos)

        for i in range(count):
            remove(f'{name}_{message_id}_{i + 1}.png')
        remove(f'{name}_{message_id}.pdf')

    except:
        await bot.send_message(user_id, ['Ошибка 404. Страница не найдена', 'Памылка 404. Старонка не знойдзена'][l])


if __name__ == '__main__':
    sql_launch()
    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')
    dp.run_polling(bot)
