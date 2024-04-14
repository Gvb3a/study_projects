import fitz
import requests
import datetime

from urllib3 import disable_warnings
from os import remove
from colorama import init, Fore, Style
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.client.session.aiohttp import AiohttpSession

from bsu_sql import sql_launch, sql_mode_or_language, sql_saved_message, sql_change_mode_or_language, sql_stat, plot

init()
# код в комментариях предназначен для pythonanywhere(онлайн-хостинг)
# session = AiohttpSession(proxy="http://proxy.server:3128")
bot_token = 'bot_token'  # https://t.me/BotFather
bot = Bot(bot_token)
# bot = Bot(bot_token, session=session)
dp = Dispatcher()


def start_keyboard(l):  # функция для start inline-keyboard (в зависимости от языка)
    # l - язык пользователя. 0 - русский, 1 - белорусский
    inline_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=['Расписание занятий студентов дневного отделения',
                                    'Расклад заняткаў студэнтаў дзённага аддзялення'][l], callback_data='inline_raspisanie')],
        [InlineKeyboardButton(text=['Расписание занятий ДО студентов дневного отделения',
                                    'Расклад заняткаў ДН студэнтаў дзённага аддзялення'][l], callback_data='inline_USRDO')],
        [InlineKeyboardButton(text=['Расписание зачетов студентов дневного отделения',
                                    'Расклад залікаў студэнтаў дзённага аддзялення'][l], callback_data='inline_zachet')],
        [InlineKeyboardButton(text=['Расписание консультаций и экзаменов студентов дневного отделения',
                                    'Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення'][l], callback_data='inline_sesia')]
    ])
    return inline_start_keyboard


def inline_button(path, speciality):  # генерация однотипных inline кнопок
    inline_list = []
    for i in range(4):
        inline_list.append(InlineKeyboardButton(text=f'{i+1} курс', callback_data=f'{path}/{i+1}_{speciality}'))
    return inline_list


def create_main_inline_keyboard(l, path):
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
    inline_classical_philology_3 = [InlineKeyboardButton(text='3 курс', callback_data=f'{path}/3_klassiki')]

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


main_dict = {  # будет использоваться для 'расшифрования'
    'raspisanie': ['Расписание занятий студентов дневного отделения (ІІ семестр) 2023-2024 ',
                   'Расклад заняткаў студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024 '],
    'USRDO': ['Расписание занятий (дистанционное обучение) студентов дневного отделения (ІІ семестр) 2023-2024 ',
              'Расклад заняткаў (дыстанцыйнае навучанне) студэнтаў дзённага аддзялення (ІІ семестр) 2023-2024 '],
    'zachet': ['Расписание зачетов студентов дневного отделения (І семестр) 2023-2024 ',
               'Расклад залікаў студэнтаў дзённага аддзялення (І семестр) 2023-2024 '],
    'sesia': ['Расписание консультаций и экзаменов студентов дневного отделения (І семестр 2023-2024) ',
              'Расклад кансультацый і экзаменаў студэнтаў дзённага аддзялення (І семестр 2023-2024) ']

}
sup_dict = {
    'bel': ['белорусская филология', 'беларуская філалогія'],
    'rus': ['русская филология', 'руская філалогія'],
    'slav': ['славянская филология', 'славянская філалогія'],
    'klassiki': ['классическая  филология', 'класічная  філалогія'],
    'rom-germ': ['романо-германская филология', 'рамана-германская філалогія'],
    'vost': ['восточная филология', 'усходняя філалогія']
}
start_list = ['Выберите тип расписания. После окончательного выбора бот запомнит Ваше расписание и будет присылать его '
              'при отправке любого сообщения.', 'Абярыце тып раскладу. Пасля канчатковага выбару бот запомніць Ваш '
              'расклад і будзе дасылаць яго пры адпраўцы любога паведамлення']


def now():  # узнаем время, учитывая временной пояс (на pythonanywhere он отличается от нашего)
    delta = datetime.timedelta(hours=3, minutes=0)
    current_time = datetime.datetime.now(datetime.timezone.utc) + delta
    return current_time.strftime("%H:%M:%S %d.%m.%Y")


def name_fuc(username, name):  # функция для username. Просто когда username будет недоступен, возвращаем name
    return username if username is not None else name


@dp.message(CommandStart())  # Обработчик команды /start. Вызывает меню выбора
async def command_start_handler(message: Message) -> None:
    l = sql_mode_or_language(message.from_user.id, 'language')  # из базы данных узнаем язык пользователя
    await message.answer(text=start_list[l], reply_markup=start_keyboard(l))
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    print(f'{Fore.RED}start{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.callback_query(F.data == 'text')  # реакция, при нажатии на декоративные кнопки
async def inline_text(callback: CallbackQuery):
    await callback.answer(text=['Это исключительно декоративная кнопка', 'Гэта выключна дэкаратыўная кнопка'][sql_mode_or_language(callback.from_user.id, 'language')])


@dp.callback_query(F.data == 'back')   # воссоздает то же меню, что и /start
async def inline_back_handler(callback: CallbackQuery):
    l = sql_mode_or_language(callback.from_user.id, 'language')
    await callback.message.edit_text(text=start_list[l], reply_markup=start_keyboard(l))
    await callback.answer()


def inline_mode_language(l, mode):
    return InlineKeyboardMarkup(inline_keyboard=
    [[InlineKeyboardButton(text=['Изменить обратно', 'Змяніць назад'][l], callback_data=mode)]])


@dp.message(Command('language'))  # Обработчик команды /language
async def command_language(message: Message) -> None:
    user_id = message.from_user.id
    l = sql_change_mode_or_language(user_id, 'language')  # меняем язык и узнаем его
    text = ['Язык был изменен', 'Мова была зменена'][l]
    await message.answer(text=text, reply_markup=inline_mode_language(l, 'language'))
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    print(f'{Fore.RED}language{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.callback_query(F.data == 'language')  # при нажатии на кнопку смены языка
async def callback_language(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    l = sql_change_mode_or_language(user_id, 'language')
    text = ['Язык был изменен', 'Мова была зменена'][l]
    await callback.message.edit_text(text=text, reply_markup=inline_mode_language(l, 'language'))
    name = name_fuc(callback.from_user.username, callback.from_user.first_name)
    print(f'{Fore.YELLOW}language{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.message(Command('mode'))
async def command_mode(message: Message) -> None:
    user_id = message.from_user.id
    l = sql_mode_or_language(user_id, 'language')
    text = (f"{['режим изменен на', 'Рэжым зменены на'][l]} "
            f"{['pdf', 'png'][sql_change_mode_or_language(user_id, 'mode')]}")
    await message.answer(text=text, reply_markup=inline_mode_language(l, 'mode'))
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    print(f'{Fore.RED}mode{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.callback_query(F.data == 'mode')
async def callback_mode(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    l = sql_mode_or_language(user_id, 'language')
    text = (f"{['Режим изменен на', 'Рэжым зменены на'][l]} "
            f"{['pdf', 'png'][sql_change_mode_or_language(user_id, 'mode')]}")
    await callback.message.edit_text(text=text, reply_markup=inline_mode_language(l, 'mode'))
    name = name_fuc(callback.from_user.username, callback.from_user.first_name)
    print(f'{Fore.YELLOW}mode{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


def setting_inline_keyboard(l):
    language = [InlineKeyboardButton(text=['Изменить язык', 'Змяніць мову'][l], callback_data='setting-language')]
    mode = [InlineKeyboardButton(text=['Изменить режим', 'Змяніць рэжым'][l], callback_data='setting-mode')]
    back = [InlineKeyboardButton(text=['Изменить расписание', 'Змяніць расклад'][l], callback_data='back')]
    return InlineKeyboardMarkup(inline_keyboard=[language, mode, back])


@dp.message(Command('setting'))
async def command_mode(message: Message) -> None:
    user_id = message.from_user.id
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    link = sql_saved_message(name, user_id, 0)
    l = sql_mode_or_language(user_id, 'language')
    language = ['Язык: русский', 'Мова: беларуская'][l]
    saved_message = ['Сохраненное расписание:', 'Захаваны расклад:'][l] + link
    m = 'png' if sql_mode_or_language(user_id, 'mode') else 'pdf'
    mode = [f'Режим: {m}', f'Рэжым {m}'][l]
    await message.answer(f'id: {user_id}\n'
                         f'{saved_message}\n'
                         f'{language}\n'
                         f'{mode}', reply_markup=setting_inline_keyboard(l))
    print(f'{Fore.RED}setting{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.callback_query(F.data == 'setting-language')
async def callback_mode(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    name = name_fuc(callback.from_user.username, callback.from_user.first_name)
    link = sql_saved_message(name, user_id, 0)
    l = sql_change_mode_or_language(user_id, 'language')
    language = ['Язык: русский', 'Мова: беларуская'][l]
    saved_message = ['Сохраненное расписание:', 'Захаваны расклад:'][l] + link
    m = 'png' if sql_mode_or_language(user_id, 'mode') else 'pdf'
    mode = [f'Режим: {m}', f'Рэжым {m}'][l]
    await callback.message.edit_text(f'id: {user_id}\n'
                                    f'{saved_message}\n'
                                    f'{language}\n'
                                    f'{mode}', reply_markup=setting_inline_keyboard(l))


@dp.callback_query(F.data == 'setting-mode')
async def callback_mode(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    name = name_fuc(callback.from_user.username, callback.from_user.first_name)
    link = sql_saved_message(name, user_id, 0)
    l = sql_mode_or_language(user_id, 'mode')
    language = ['Язык: русский', 'Мова: беларуская'][l]
    saved_message = ['Сохраненное расписание:', 'Захаваны расклад:'][l] + link
    m = 'png' if sql_change_mode_or_language(user_id, 'mode') else 'pdf'
    mode = [f'Режим: {m}', f'Рэжым {m}'][l]
    await callback.message.edit_text(f'id: {user_id}\n'
                                    f'{saved_message}\n'
                                    f'{language}\n'
                                    f'{mode}', reply_markup=setting_inline_keyboard(l))


help_message = ['Данный телеграмм бот предоставляет удобный доступ к расписанию филфака БГУ. Просто '
                'отправьте команду /start и выберете нужное для вас расписание. После отправки '
                'любого сообщения бот будет отправлять последние выбранное сообщение. Под отправленным сообщением будет'
                ' кнопка "обновить", при нажатии на которую будет присылаться выше расположенное расписание.\n\n'
                'Команды:\n'
                '/start - вызывает меню для выбора расписания\n'
                '/help - сообщение для получения помощи\n'
                '/language - поскольку заказчик разговаривает на белорусском языке, то пришлось добавить смену языка\n'
                '/mode - меняет режим. Всего доступно два режима: pdf и png\n'
                '/setting - сообщение, где вы можете посмотреть ваши настройки\n\n'
                'Если бот перестал работать, то писать сюда: @gvb3a',
                'Гэты тэлеграм бот дае зручны доступ да раскладу філфака БДУ. Проста '
                'Дашліце каманду /start і вылучыце патрэбны для вас расклад. Пасля адпраўкі '
                'любога паведамлення бот будзе адпраўляць апошнія абранае паведамленне. Пад адпраўленым паведамленнем '
                'будзе кнопка "абнавіць", пры націску на якую будзе дасылацца вышэй размешчаны расклад.\n\n'
                'Каманды:\n'
                '/start - выклікае меню для выбару раскладу\n'
                '/help - паведамленне для атрымання дапамогі\n'
                '/language - паколькі заказчык размаўляе на беларускай мове, то прыйшлося дадаць змену мовы\n'
                '/mode - мяняе рэжым. Усяго даступна два рэжыму: pdf і png\n'
                '/setting - паведамленне, дзе вы можаце паглядзець вашыя наладкі\n\n'
                'Калі бот перастаў працаваць, то пісаць сюды: @gvb3a']


@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    l = sql_mode_or_language(message.from_user.id, 'language')
    await message.answer(help_message[l])
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    print(f'{Fore.RED}help{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.message(Command('stat'))
async def command_stat(message: Message) -> None:
    await message.answer('Загрузка...')
    file_name = plot()
    await message.answer_photo(photo=FSInputFile(f'{file_name}.png'))
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    remove(f'{file_name}.png')
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    print(f'{Fore.RED}stat{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.callback_query(F.data)
async def callback_data(callback: types.CallbackQuery):
    data = callback.data
    l = sql_mode_or_language(callback.from_user.id, 'language')
    name = name_fuc(callback.from_user.username, callback.from_user.first_name)
    if data[:6] == 'inline':
        data = data[7:]
        await callback.message.edit_text(text=main_dict[data][l]+['Выберете специальность', 'Абярыце спецыяльнасць'][l],
                                         reply_markup=create_main_inline_keyboard(l, data))
        await callback.answer()
    else:
        await main(data, callback.from_user.id, callback.id, l, name, 'new message')
        await callback.answer()
        print(f'{Fore.GREEN}{data}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


@dp.message()
async def main_handler(message: types.Message) -> None:
    name = name_fuc(message.from_user.username, message.from_user.first_name)
    user_id = message.from_user.id
    link = sql_saved_message(name, user_id, 0)
    l = sql_mode_or_language(user_id, 'language')
    if link == 'error':
        await message.answer(['Ваше сохраненное расписание не обнаружено. Скорее всего, админ сбросил базу данных. Используйте команду /start и заново выберите расписание',
                              'Ваш захаваны расклад не выяўлены. Хутчэй за ўсё, адмін скінуў базу дадзеных. Выкарыстоўвайце каманду /start і зноўку абярыце расклад'][l])
    else:
        await main(link, user_id, message.message_id, l, name, 'new message')
    print(f'{Fore.GREEN}{link}{Style.RESET_ALL} by {Fore.BLUE}{name}{Style.RESET_ALL} at {now()}')


async def main(data, user_id, message_id, l, name, update_or_new):
    try:  # при возникновении ошибки (к примеру, файл не найден) этот код прекратиться
        disable_warnings()  # без этого вылезает предупреждение, что сайт филфака бгу не безопасен)
        response = requests.get(f'https://philology.bsu.by/files/dnevnoe/{data}.pdf', verify=False)
        # скачиваем pdf файл
        name_file = data.split('/')[1]  # raspisanie/3_rom-germ >>> 3_rom-germ

        with open(f'{name_file}_{message_id}.pdf', 'wb') as file:
            file.write(response.content)  # сохраняем файл

        cap = name_file.split('_')  # 3_rom-germ >>> [3, rom-germ]
        # Тут я расшифровываю путь. В словаре main_dict находятся значения raspisanie, USRDO, zachet и sesia
        # В sup_dict - bel, rus, slav, klassiki, rom-germ, vost. В cap[0] - курс
        caption = main_dict[data.split('/')[0]][l] + sup_dict[cap[1]][l] + ' ' + cap[0] + ' курс'
        mode = sql_mode_or_language(user_id, 'mode')
        inline_update = [InlineKeyboardButton(text=['Обновить', 'Аднавіць'][l],
                                              callback_data=f'{data}')]
        inline_update_keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_update])

        if mode == 1:
            doc = fitz.open(f'{name_file}_{message_id}.pdf')  # начинается магия по преобразованию pdf в png
            photos = []  # Тут будут храниться фотки. Нужно их занести в список
            count = len(doc)  # количество страниц
            n = 2  # качество страниц
            #  Дальше идёт код, которые преобразует страницы pdf файла в png. Если честно, то я без понятия, как он работает
            for i in range(count):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(n, n))
                pix.save(f"{name_file}_{message_id}_{i + 1}.png")  # сохраняем файл
                photos.append(InputMediaPhoto(media=FSInputFile(f"{name_file}_{message_id}_{i + 1}.png"),
                                              caption=caption if i == 0 else None))  # добавляем в список
            doc.close()  # Закрываем документ. Иначе мы не сможем с ним взаимодействовать

            inline_back = [InlineKeyboardButton(text='Меню', callback_data='back')]
            await bot.send_media_group(user_id, media=photos)  # отправляем фотки
            await bot.send_message(user_id, text=
                                    ['Нажмите на кнопку или отправьте любое сообщение, что бы обновить расписание',
                                    'Націсніце на кнопку або адпраўце любое паведамленне, каб абнавіць расклад'][l],
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[inline_update, inline_back]))

            for i in range(count):  # удаляем фотки
                remove(f'{name_file}_{message_id}_{i + 1}.png')
        else:
            doc = FSInputFile(f'{name_file}_{message_id}.pdf')
            await bot.send_document(user_id, document=doc, reply_markup=inline_update_keyboard, caption=caption)
        remove(f'{name_file}_{message_id}.pdf')  # удаляем pdf

    except:  # действия, в случаи ошибки
        await bot.send_message(user_id, ['Ошибка 404. Страница не найдена', 'Памылка 404. Старонка не знойдзена'][l])
    sql_stat(name, data)  # заносим данные об запросе в базу данных


# запуск бота
if __name__ == '__main__':
    sql_launch()  # проверка базы данных
    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {now()}')  # сообщение о запуске
    dp.run_polling(bot)
