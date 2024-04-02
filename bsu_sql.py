import sqlite3
import datetime
import matplotlib.pyplot as plt
import numpy as np


def current_time():
    delta = datetime.timedelta(hours=3, minutes=0)
    current_time = datetime.datetime.now(datetime.timezone.utc) + delta
    return current_time.strftime("%H:%M:%S %d.%m.%Y")


def sql_launch():
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
        name TEXT,
        id INTEGER PRIMARY KEY,
        message TEXT,
        language INT,
        mode INT
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stat (
        name TEXT,
        type TEXT,
        speciality TEXT,
        course TEXT,
        time TEXT
        )
        ''')
    connection.commit()
    connection.close()


def sql_stat(name, data):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    data = data.split('/')
    type_data = data[0]
    course, speciality = data[1].split('_')

    cursor.execute(f"INSERT INTO stat(name, type, speciality, course, time) VALUES ('{name}', '{type_data}', "
                   f"'{speciality}', '{course}', '{current_time()}')")

    connection.commit()
    connection.close()


def plot():
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM stat')  # получаем информацию из таблицы
    rows = cursor.fetchall()  # заносим ее в список

    day = int(datetime.datetime.now().strftime("%d"))  # узнаем сегодняшний день
    mounth = datetime.datetime.now().strftime("%m")
    i = -1
    # создаем списки, в которых находятся 24 списка
    day_data: list[list[int]] = [0 for _ in range(24)]
    average_day_data: list[list[int]] = [0 for _ in range(24)]
    # цикл исполняется, пока день равен сегодняшнему, и пока не пройдется по всем элементам
    while len(rows) >= abs(i) and int(rows[i][4][9:11]) == day:
        j = int(rows[i][4][0:2])
        day_data[j] += 1
        i -= 1

    i = -1
    while len(rows) >= abs(i) and rows[i][4][12:14] == mounth:
        j = int(rows[i][4][0:2])
        average_day_data[j] += 1 / int(day)
        i -= 1

    plt.bar(range(24), day_data)
    plt.plot(range(24), average_day_data, color='r')
    for i in range(len(day_data)):
        if day_data[i] != 0:
            plt.text(i, day_data[i], str(day_data[i]), ha='center', va='bottom')  # добавление подписей к каждой ячейке

    plt.xticks(np.arange(0, 24, step=2), np.arange(0, 24, step=2))  # пронумеровать каждые 2 столбца

    name = datetime.datetime.now().strftime("%H:%M:%S")

    plt.savefig(f'{name}.png')
    plt.clf()
    connection.close()
    return name


def sql_saved_message(name, user_id, message):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()
    if row is not None and row[1] is not None:
        if row[0] != name:
            cursor.execute(f"UPDATE user SET name = '{name}' WHERE id = {user_id}")
    else:
        cursor.execute(f"INSERT INTO user(name, id, message, language) VALUES ('{name}', {user_id}, '0', 0)")
        connection.commit()
        print(f'Новый пользователь {name}')
        return 'error'

    if message == 0:
        connection.close()
        return row[2] if row[2] != '0' else 'error'
    else:
        cursor.execute(f"UPDATE user SET message = '{message}' WHERE id = {user_id}")
        connection.commit()
        connection.close()
        return message


def sql_mode_or_language(user_id, what):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()

    if row is None:
        cursor.execute(f"INSERT INTO user(id, language, mode) VALUES ({user_id}, 0, 1)")
        connection.commit()
        connection.close()
        return 0
    else:
        connection.close()
        return row[3 if what == 'language' else 4]


def sql_change_mode_or_language(user_id, changeable):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    mode_or_language = sql_mode_or_language(user_id, changeable)
    new_mode = 0 if mode_or_language else 1
    cursor.execute(f"UPDATE user SET {changeable} = {new_mode} WHERE id = {user_id}")

    connection.commit()
    connection.close()
    return new_mode
