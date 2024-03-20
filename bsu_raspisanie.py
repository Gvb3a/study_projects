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

from bsu_sql import sql_launch, sql_user, sql_saved_message
init()

# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot('bot_token')
# bot = Bot('bot_token', session=session)
dp = Dispatcher()

inline_day = [InlineKeyboardButton(text='Расписание занятий студентов дневного отделения', callback_data='inline_day'),
              InlineKeyboardButton(text='Расклад заняткаў студэнтаў дзённага аддзялення', callback_data='inline_day')]
inline_dist = [InlineKeyboardButton(text='Расписание занятий ДО студентов дневного отделения', callback_data='inline_dist'),
                   InlineKeyboardButton(text='Расклад заняткаў ДН студэнтаў дзённага аддзялення', callback_data='inline_dist')]
inline_exam = [InlineKeyboardButton(text='Расписание зачетов студентов дневного отделения', callback_data='inline_exam'),
               InlineKeyboardButton(text='Расклад залікаў студэнтаў дзённага аддзялення', callback_data='inline_exam')]
inline_session = [InlineKeyboardButton(text='Расписание консультаций и экзаменов студентов дневного отделения', callback_data='inline_session'),
                  InlineKeyboardButton(text='Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення', callback_data='inline_session')]


def start_keyboard(l):
    inline_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_day[l]],
        [inline_dist[l]],
        [inline_exam[l]],
        [inline_session[l]]
    ])
    return inline_start_keyboard


def create_inline_keyboard(l, path):

    inline_back = InlineKeyboardButton(text='Назад', callback_data='back')

    inline_belarusian_philology = [InlineKeyboardButton(text='Белорусская филология', callback_data='text'),
                                   InlineKeyboardButton(text='Беларуская філалогія', callback_data='text')]
    inline_belarusian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data=f'{path}1_bel')
    inline_belarusian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data=f'{path}2_bel')
    inline_belarusian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_bel')
    inline_belarusian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data=f'{path}4_bel')

    inline_russian_philology = [InlineKeyboardButton(text='Русская филология', callback_data='text'),
                                InlineKeyboardButton(text='Руская філалогія', callback_data='text')]
    inline_russian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data=f'{path}1_rus')
    inline_russian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data=f'{path}2_rus')
    inline_russian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_rus')
    inline_russian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data=f'{path}4_rus')

    inline_slavic_philology = [InlineKeyboardButton(text='Славянская филология', callback_data='text'),
                               InlineKeyboardButton(text='Славянская філалогія', callback_data='text')]
    inline_slavic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data=f'{path}1_slav')
    inline_slavic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data=f'{path}2_slav')
    inline_slavic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_slav')
    inline_slavic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data=f'{path}4_slav')

    inline_classical_philology = [InlineKeyboardButton(text='Классическая  филология', callback_data='text'),
                                  InlineKeyboardButton(text='Класічная  філалогія', callback_data='text')]
    inline_classical_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_klassiki')

    inline_romano_germanic_philology = [
        InlineKeyboardButton(text='Романо-германская филология', callback_data='text'),
        InlineKeyboardButton(text='Рамана-германская філалогія', callback_data='text')]
    inline_romano_germanic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data=f'{path}1_rom-germ')
    inline_romano_germanic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data=f'{path}2_rom-germ')
    inline_romano_germanic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_rom-germ')
    inline_romano_germanic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data=f'{path}4_rom-germ')

    inline_oriental_philology = [InlineKeyboardButton(text='Восточная филология', callback_data='text'),
                                 InlineKeyboardButton(text='Усходняя філалогія', callback_data='text')]
    inline_oriental_philology_1 = InlineKeyboardButton(text='1 курс', callback_data=f'{path}1_vost')
    inline_oriental_philology_2 = InlineKeyboardButton(text='2 курс', callback_data=f'{path}2_vost')
    inline_oriental_philology_3 = InlineKeyboardButton(text='3 курс', callback_data=f'{path}3_vost')
    inline_oriental_philology_4 = InlineKeyboardButton(text='4 курс', callback_data=f'{path}4_vost')


    inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
    [inline_belarusian_philology[l]],
    [inline_belarusian_philology_1, inline_belarusian_philology_2, inline_belarusian_philology_3, inline_belarusian_philology_4],
    [inline_russian_philology[l]],
    [inline_russian_philology_1, inline_russian_philology_2, inline_russian_philology_3, inline_russian_philology_4],
    [inline_slavic_philology[l]],
    [inline_slavic_philology_1, inline_slavic_philology_2, inline_slavic_philology_3, inline_slavic_philology_4],
    [inline_classical_philology[l]],
    [inline_classical_philology_3],
    [inline_romano_germanic_philology[l]],
    [inline_romano_germanic_philology_1, inline_romano_germanic_philology_2, inline_romano_germanic_philology_3, inline_romano_germanic_philology_4],
    [inline_oriental_philology[l]],
    [inline_oriental_philology_1, inline_oriental_philology_2, inline_oriental_philology_3, inline_oriental_philology_4],
    [inline_back]
    ])
    return inline_keyboard



@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    l = sql_user(message.from_user.id, 1)
    await message.answer(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит Ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць Ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))
    print(f'{Fore.RED}/start{Style.RESET_ALL} by {Fore.BLUE}{message.from_user.first_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.callback_query(F.data == 'inline_day')
async def inline_day_handler(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Расписание занятий студентов дневного отделения (ІІ семестр) 2023-2024. Выберете специальность',
              'Расклад заняткаў студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'raspisanie/'))
    await callback.answer()


@dp.callback_query(F.data == 'inline_dist')
async def inline_dist_handler(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Расписание занятий (дистанционное обучение) студентов дневного отделения (ІІ семестр) 2023-2024. Выберете специальность',
              'Расклад заняткаў (дыстанцыйнае навучанне) студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'USRDO/'))
    await callback.answer()



@dp.callback_query(F.data == 'inline_exam')
async def inline_exam_handler(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Расписание зачетов студентов дневного отделения (І семестр) 2023-2024. Выберете специальность',
              'Расклад залікаў студэнтаў дзённага аддзялення (І семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'zachet/'))
    await callback.answer()


@dp.callback_query(F.data == 'inline_session')
async def inline_session_handler(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Расписание консультаций и экзаменов студентов дневного отделения (І семестр 2023-2024). Выберете специальность',
              'Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення (І семестр 2023-2024). Абярыце спецыяльнасць'][l],
        reply_markup=create_inline_keyboard(l, 'sesia/'))
    await callback.answer()


@dp.callback_query(F.data == 'text')
async def inline_text(callback: CallbackQuery):
    await callback.answer(text=['Это исключительно декоративная кнопка', 'Гэта выключна дэкаратыўная кнопка'][sql_user(callback.from_user.id, 1)])


@dp.callback_query(F.data == 'back')
async def inline_back_fuc(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит Ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць Ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))
    await callback.answer()


@dp.callback_query(F.data)
async def process_callback_data(callback: types.CallbackQuery):
    name = callback.from_user.first_name
    user_id = callback.from_user.id
    link = callback.data
    callback_id = callback.id
    await main(link, user_id, callback_id)
    name_file = link[link.rfind('/') + 1:]
    remove(f'{name_file}_{callback_id}.pdf')
    await callback.answer()
    sql_saved_message(callback.from_user.username, callback.from_user.id, link)
    print(f'{Fore.GREEN}{link}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.message(Command('language'))
async def command_language(message: Message) -> None:
    await message.answer(['Язык был изменен', 'Мова была зменена'][sql_user(message.from_user.id, 0)])
    print(f'{Fore.RED}/language{Style.RESET_ALL} by {Fore.BLUE}{message.from_user.first_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


@dp.message()
async def main_handler(message: types.Message) -> None:
    name = message.from_user.first_name
    user_id = message.from_user.id
    message_id = message.message_id
    link = sql_saved_message(name, user_id, 0)
    await main(link, user_id, message_id)
    name_file = link[link.rfind('/')+1:]
    remove(f'{name_file}_{message_id}.pdf')
    print(f'{Fore.GREEN}{link}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')


async def main(data, user_id, message_id):
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
            media = InputMediaPhoto(media=FSInputFile(f"{name}_{message_id}_{i + 1}.png"))
            photos.append(media)

        await bot.send_media_group(user_id, media=photos)
        await bot.send_document(user_id, document=FSInputFile(f'{name}_{message_id}.pdf'))

        for i in range(count):
            remove(f'{name}_{message_id}_{i + 1}.png')
    except:
        await bot.send_message(user_id, ['Ошибка 404. Страница не найдена', 'Памылка 404. Старонка не знойдзена'][sql_user(user_id, 1)])


if __name__ == '__main__':
    sql_launch()
    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')
    dp.run_polling(bot)
