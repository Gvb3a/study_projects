import fitz
import requests

from urllib3 import disable_warnings
from os import remove

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InputFile,
                           InlineKeyboardMarkup)
from pdf2image import convert_from_path

bot = Bot('bot_token')
dp = Dispatcher()

inline_1 = InlineKeyboardButton(
    text='Расписание занятий студентов дневного отделения (ІІ семестр) 2023-2024',
    callback_data='inline_1'
)
inline_2 = InlineKeyboardButton(
    text='Расписание занятий (дистанционное обучение) студентов дневного отделения (ІІ семестр) 2023-2024',
    callback_data='inline_2'
)
inline_3 = InlineKeyboardButton(
    text='Расписание зачетов, консультаций, экзаменов иностранных студентов (I семестр) 2023-2024',
    callback_data='inline_3'
)
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[inline_1],
                     [inline_2],
                     [inline_3]]
)
inline_1_belarusian_philology = InlineKeyboardButton(text='Белорусская филология', callback_data='text')
inline_1_belarusian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_bel.pdf')
inline_1_belarusian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_bel.pdf')
inline_1_belarusian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_bel.pdf')
inline_1_belarusian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_bel.pdf')

inline_1_russian_philology = InlineKeyboardButton(text='Русская филология', callback_data='text')
inline_1_russian_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_rus.pdf')
inline_1_russian_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_rus.pdf')
inline_1_russian_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_rus.pdf')
inline_1_russian_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_rus.pdf')

inline_1_slavic_philology = InlineKeyboardButton(text='Славянская филология', callback_data='text')
inline_1_slavic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_slav.pdf')
inline_1_slavic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_slav.pdf')
inline_1_slavic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_slav.pdf')
inline_1_slavic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_slav.pdf')

inline_1_classical_philology = InlineKeyboardButton(text='Классическая  филология', callback_data='text')
inline_1_classical_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_klassiki.pdf')

inline_1_romano_germanic_philology = InlineKeyboardButton(text='Романо-германская филология', callback_data='text')
inline_1_romano_germanic_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_rom-germ.pdf')
inline_1_romano_germanic_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_rom-germ.pdf')
inline_1_romano_germanic_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_rom-germ.pdf')
inline_1_romano_germanic_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_rom-germ.pdf')

inline_1_oriental_philology = InlineKeyboardButton(text='Восточная филология', callback_data='text')
inline_1_oriental_philology_1 = InlineKeyboardButton(text='1 курс', callback_data='1_vost.pdf')
inline_1_oriental_philology_2 = InlineKeyboardButton(text='2 курс', callback_data='2_vost.pdf')
inline_1_oriental_philology_3 = InlineKeyboardButton(text='3 курс', callback_data='3_vost.pdf')
inline_1_oriental_philology_4 = InlineKeyboardButton(text='4 курс', callback_data='4_vost.pdf')

inline_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_1_belarusian_philology],
        [inline_1_belarusian_philology_1, inline_1_belarusian_philology_2, inline_1_belarusian_philology_3, inline_1_belarusian_philology_4],
        [inline_1_russian_philology],
        [inline_1_russian_philology_1, inline_1_russian_philology_2, inline_1_russian_philology_3, inline_1_russian_philology_4],
        [inline_1_slavic_philology],
        [inline_1_slavic_philology_1, inline_1_slavic_philology_2, inline_1_slavic_philology_3, inline_1_slavic_philology_4],
        [inline_1_classical_philology],
        [inline_1_classical_philology_3],
        [inline_1_romano_germanic_philology],
        [inline_1_romano_germanic_philology_1, inline_1_romano_germanic_philology_2, inline_1_romano_germanic_philology_3, inline_1_romano_germanic_philology_4],
        [inline_1_oriental_philology],
        [inline_1_oriental_philology_1, inline_1_oriental_philology_2, inline_1_oriental_philology_3, inline_1_oriental_philology_4]
    ]
)


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(text='Тип расписания:', reply_markup=start_keyboard)


@dp.callback_query(F.data == 'inline_1')
async def inline_1(callback: CallbackQuery):
    await callback.message.edit_text(text='123', reply_markup=inline_1_keyboard)
    await callback.answer()


@dp.callback_query(F.data == 'inline_2')
async def inline_2(callback: CallbackQuery):
    await callback.answer(text='В разработке')


@dp.callback_query(F.data == 'inline_3')
async def inline_3(callback: CallbackQuery):
    await callback.answer(text='В разработке')


@dp.callback_query(F.data == 'text')
async def text(callback: CallbackQuery):
    await callback.answer(text='Это исключительно декоративная кнопка')


@dp.callback_query(F.data)
async def process_callback_data(callback: types.CallbackQuery):
    data = callback.data
    photos, error, count = main(data)
    if error:
        await bot.send_media_group(callback.from_user.id, media=photos)
        await bot.send_document(callback.from_user.id, document=FSInputFile(data))
    else:
        await bot.send_message(callback.from_user.id, 'Ошибка')

    for i in range(count):
        remove(f'image_{i + 1}.png')
    remove(f'{data}')
    await callback.answer()

@dp.message()
async def main_handler(message: types.Message) -> None:
    photos, error, count = main('3_rom-germ.pdf')
    if error:
        await message.answer_media_group(media=photos)
        await message.answer_document(document=FSInputFile(f'3_rom-germ.pdf'))
    else:
        await message.answer('Ошибка')

    for i in range(count):
        remove(f'image_{i + 1}.png')
    remove(f'3_rom-germ.pdf')


def main(name: str):
    try:
        disable_warnings()
        response = requests.get(f'https://philology.bsu.by/files/dnevnoe/raspisanie/{name}', verify=False)

        with open(name, 'wb') as file:
            file.write(response.content)

        doc = fitz.open(name)
        photos = []
        count = len(doc)
        for i in range(count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"image_{i + 1}.png")
            media = InputMediaPhoto(media=FSInputFile(f"image_{i + 1}.png"))
            photos.append(media)
        return photos, True, count
    except:
        return photos, False, count


if __name__ == '__main__':
    dp.run_polling(bot)
