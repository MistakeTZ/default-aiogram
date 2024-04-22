from datetime import datetime
from database.models import cursor


# Добавление нового пользователя в базу данных
def add_user(id, username, day, time):
    if get_user(id):
        update_field(id, "username", username)
        return False
    a = time.split(":")
    stmt = """INSERT INTO  (id, username, day, time, blocks) VALUES ({}, '{}', '{}', '{}', {});""".format(id, username, day, a[0]+" "+a[1], -2)
    cursor.execute(stmt)


# Обновление поля в базе данных для пользователя
def update_field(id, field, value):
    stmt = """
            UPDATE  SET {} = {} WHERE id = {};
            """.format(field, f"'{value}'" if isinstance(value, str) else value, id)
    try:
        cursor.execute(stmt)
    except Exception as e:
        print(e)


# Получение всех пользователей
def get_all():
    cursor.execute("SELECT * FROM ;")
    return cursor.fetchall()


# Получение одного пользователя по ID
def get_user(id):
    try:
        cursor.execute("SELECT * FROM  WHERE id = {};".format(id))
        return cursor.fetchone()
    except Exception:
        return False


# Добавление фидбека
def add_feedback(id, feedback, day):
    if len(feedback) > 255:
        feedback = feedback[:255]
    try:
        cursor.execute("SELECT MAX(number) FROM ;")
        count = cursor.fetchone()[0]
        
        stmt = """INSERT INTO feedback (number, user_id, feedback, day) VALUES ({}, {}, '{}', {});""".format(count + 1 if isinstance(count, int) else 0, id, feedback, day)
        cursor.execute(stmt)
    except Exception:
        return False
    