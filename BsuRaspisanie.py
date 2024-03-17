import fitz
import requests

from urllib3 import disable_warnings
from os import remove

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from bsu_sql import sql_launch, sql_user, sql_message

bot = Bot('bot_token')
dp = Dispatcher()

inline_day = [InlineKeyboardButton(text='Расписание занятий студентов дневного отделения', callback_data='inline_day'),
              InlineKeyboardButton(text='Расклад заняткаў студэнтаў дзённага аддзялення', callback_data='inline_day')]

inline_distance = [InlineKeyboardButton(text='Расписание занятий ДО студентов дневного отделения', callback_data='inline_distance'),
                   InlineKeyboardButton(text='Расклад заняткаў ДН студэнтаў дзённага аддзялення', callback_data='inline_distance')]

inline_exam = [InlineKeyboardButton(text='Расписание зачетов студентов дневного отделения', callback_data='inline_exam'),
               InlineKeyboardButton(text='Расклад залікаў студэнтаў дзённага аддзялення', callback_data='inline_exam')]

inline_session = [InlineKeyboardButton(text='Расписание консультаций и экзаменов студентов дневного отделения', callback_data='inline_session'),
                  InlineKeyboardButton(text='Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення', callback_data='inline_session')]


inline_1_belarusian_philology = [InlineKeyboardButton(text='Белорусская филология', callback_data='text'),
                                 InlineKeyboardButton(text='Беларуская філалогія', callback_data='text')]
inline_1_belarusian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_bel')
inline_1_belarusian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_bel')
inline_1_belarusian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_bel')
inline_1_belarusian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_bel')

inline_1_russian_philology = [InlineKeyboardButton(text='Русская филология', callback_data='text'),
                              InlineKeyboardButton(text='Руская філалогія', callback_data='text')]
inline_1_russian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_rus')
inline_1_russian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_rus')
inline_1_russian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_rus')
inline_1_russian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_rus')

inline_1_slavic_philology = [InlineKeyboardButton(text='Славянская филология', callback_data='text'),
                             InlineKeyboardButton(text='Славянская філалогія', callback_data='text')]
inline_1_slavic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_slav')
inline_1_slavic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_slav')
inline_1_slavic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_slav')
inline_1_slavic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_slav')

inline_1_classical_philology = [InlineKeyboardButton(text='Классическая  филология', callback_data='text'),
                                InlineKeyboardButton(text='Класічная  філалогія', callback_data='text')]
inline_1_classical_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_klassiki')

inline_1_romano_germanic_philology = [InlineKeyboardButton(text='Романо-германская филология', callback_data='text'),
                                      InlineKeyboardButton(text='Рамана-германская філалогія', callback_data='text')]
inline_1_romano_germanic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_rom-germ')
inline_1_romano_germanic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_rom-germ')
inline_1_romano_germanic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_rom-germ')
inline_1_romano_germanic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_rom-germ')

inline_1_oriental_philology = [InlineKeyboardButton(text='Восточная филология', callback_data='text'),
                               InlineKeyboardButton(text='Усходняя філалогія', callback_data='text')]
inline_1_oriental_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_vost')
inline_1_oriental_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_vost')
inline_1_oriental_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_vost')
inline_1_oriental_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_vost')

inline_back = InlineKeyboardButton(text='Назад', callback_data='back')


def start_keyboard(l):
    inline_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_day[l]],
        [inline_distance[l]],
        [inline_exam[l]],
        [inline_session[l]]
    ])
    return inline_start_keyboard


def day_keyboard(l):
    inline_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
    [inline_1_belarusian_philology[l]],
    [inline_1_belarusian_philology_1, inline_1_belarusian_philology_2, inline_1_belarusian_philology_3, inline_1_belarusian_philology_4],
    [inline_1_russian_philology[l]],
    [inline_1_russian_philology_1, inline_1_russian_philology_2, inline_1_russian_philology_3, inline_1_russian_philology_4],
    [inline_1_slavic_philology[l]],
    [inline_1_slavic_philology_1, inline_1_slavic_philology_2, inline_1_slavic_philology_3, inline_1_slavic_philology_4],
    [inline_1_classical_philology[l]],
    [inline_1_classical_philology_3],
    [inline_1_romano_germanic_philology[l]],
    [inline_1_romano_germanic_philology_1, inline_1_romano_germanic_philology_2, inline_1_romano_germanic_philology_3, inline_1_romano_germanic_philology_4],
    [inline_1_oriental_philology[l]],
    [inline_1_oriental_philology_1, inline_1_oriental_philology_2, inline_1_oriental_philology_3, inline_1_oriental_philology_4],
    [inline_back]
    ])
    return inline_day_keyboard


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    l = sql_user(message.from_user.id, 1)
    await message.answer(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))


@dp.callback_query(F.data == 'inline_day')
async def inline_day_handler(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Расписание занятий студентов дневного отделения (ІІ семестр) 2023-2024. Выберете специальность',
              'Расклад заняткаў студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024. Абярыце спецыяльнасць'][l],
        reply_markup=day_keyboard(l))
    await callback.answer()


@dp.callback_query(F.data == 'inline_distance')
async def inline_2(callback: CallbackQuery):
    await callback.answer(text='В разработке')

@dp.callback_query(F.data == 'inline_exam')
async def inline_2(callback: CallbackQuery):
    await callback.answer(text='В разработке')

@dp.callback_query(F.data == 'inline_session')
async def inline_2(callback: CallbackQuery):
    await callback.answer(text='В разработке')


@dp.callback_query(F.data == 'text')
async def text(callback: CallbackQuery):
    await callback.answer(text=['Это исключительно декоративная кнопка', 'Гэта выключна дэкаратыўная кнопка'][sql_user(callback.from_user.id, 1)])


@dp.callback_query(F.data == 'back')
async def inline_back_fuc(callback: CallbackQuery):
    l = sql_user(callback.from_user.id, 1)
    await callback.message.edit_text(
        text=['Выберите тип расписания. После окончательного выбора бот запомнит ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення'][l],
        reply_markup=start_keyboard(l))
    await callback.answer()


@dp.callback_query(F.data)
async def process_callback_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id
    photos, error, count = main(data)
    if error:
        await bot.send_media_group(user_id, media=photos)
        await bot.send_document(user_id, document=FSInputFile(f'{data}.pdf'))

        for i in range(count):
            remove(f'{data}_{i + 1}.png')
        remove(f'{data}.pdf')
    else:
        await bot.send_message(user_id, 'Ошибка')
    sql_message(callback.from_user.username, user_id, data)
    await callback.answer()


@dp.message(Command('language'))
async def command_start(message: Message) -> None:
    await message.answer(['Язык был изменен', 'Мова была зменена'][sql_user(message.from_user.id, 0)])


@dp.message()
async def main_handler(message: types.Message) -> None:
    name = message.from_user.first_name
    if message.from_user.username is not None:
        name += f'({message.from_user.username})'
    user_id = message.from_user.id
    data = sql_message(name, user_id, 0)
    photos, error, count = main(data)
    if error and data != 0:
        await bot.send_media_group(user_id, media=photos)
        await bot.send_document(user_id, document=FSInputFile(f'{data}.pdf'))

        for i in range(count):
            remove(f'{data}_{i + 1}.png')
        remove(f'{data}.pdf')
    else:
        await bot.send_message(user_id, 'Ошибка')


def main(name: str):
    try:
        disable_warnings()
        response = requests.get(f'https://philology.bsu.by/files/dnevnoe/raspisanie/{name}.pdf', verify=False)

        with open(f'{name}.pdf', 'wb') as file:
            file.write(response.content)

        doc = fitz.open(f'{name}.pdf')
        photos = []
        count = len(doc)
        for i in range(count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"{name}_{i + 1}.png")
            media = InputMediaPhoto(media=FSInputFile(f"{name}_{i + 1}.png"))
            photos.append(media)
        return photos, True, count
    except:
        return [], False, 0


if __name__ == '__main__':
    sql_launch()
    dp.run_polling(bot)
