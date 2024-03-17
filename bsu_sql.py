import sqlite3


def sql_launch():
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
        name TEXT,
        id INTEGER PRIMARY KEY,
        message TEXT,
        language INT
        )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS message (
            name TEXT,
            message TEXT,
            time TEXT
            )
            ''')
    connection.commit()
    connection.close()


def sql_saved_message(name, user_id, message):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()
    if row is not None and row[1] is not None:
        if row[0] != name:
            cursor.execute(f"UPDATE user SET name = '{name}' WHERE id = {user_id}")
            connection.commit()
    else:
        cursor.execute(f"INSERT INTO user(name, id, message, language) VALUES ('{name}', {user_id}, '{message}', 0)")
        print(f'Новый пользователь {name}')
        connection.commit()

    if message == 0:
        connection.close()
        return row[2]
    else:
        cursor.execute(f"UPDATE user SET message = '{message}' WHERE id = {user_id}")
        connection.commit()
        connection.close()
        return message


def sql_user(user_id, mode):
    connection = sqlite3.connect('bsu_database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()
    if row is None:
        cursor.execute(f"INSERT INTO user(id, language) VALUES ({user_id}, 0)")
        connection.commit()
        connection.close()
        return 0
    elif mode:
        connection.close()
        return row[3]
    else:
        new_mode = 0 if row[3] else 1
        cursor.execute(f"UPDATE user SET language = {new_mode} WHERE id = {user_id}")
        connection.commit()
        connection.close()
        return new_mode
