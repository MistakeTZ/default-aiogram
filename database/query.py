from datetime import datetime
from database.models import cursor


# Добавление нового пользователя в базу данных
def add_user(id, username, day, time):
    if get_user(id):
        update_field(id, "username", username)
        return False
    a = time.split(":")
    stmt = """INSERT INTO emotrack (id, username, day, time, blocks) VALUES ({}, '{}', '{}', '{}', {});""".format(id, username, day, a[0]+" "+a[1], -2)
    # query = insert(users).values(id=id, username=username, gender="none", email="none", day=day, time=a[0]+" "+a[1], blocks=-1, breath=False, send=False)
    cursor.execute(stmt)


# Проверка всех пользователей на время рассылки
def is_time(time: datetime) -> list:
    need = time.hour * 60 + time.minute
    # stmt = """
    #         SELECT * FROM emotrack WHERE day = {};
    #         """.format(weekday)
    # cursor.execute(stmt)
    # all = cursor.fetchall()
    all = get_all()
    output = [el[0] for el in all if (0 <= need - (int(el[5].split(":")[0]) * 60 + int(el[5].split(":")[1])) < 2)]

    stmt = """
            SELECT * FROM emotrack WHERE send = {};
            """.format(True)
    cursor.execute(stmt)

    return output


# Обновление поля в базе данных для пользователя
def update_field(id, field, value):
    stmt = """
            UPDATE emotrack SET {} = {} WHERE id = {};
            """.format(field, f"'{value}'" if isinstance(value, str) else value, id)
    try:
        cursor.execute(stmt)
    except Exception as e:
        print(e)


# Получение всех пользователей
def get_all():
    cursor.execute("SELECT * FROM emotrack;")
    return cursor.fetchall()


# Получение одного пользователя по ID
def get_user(id):
    try:
        cursor.execute("SELECT * FROM emotrack WHERE id = {};".format(id))
        return cursor.fetchone()
    except Exception:
        return False


# Добавление фидбека
def add_feedback(id, feedback, day):
    if len(feedback) > 255:
        feedback = feedback[:255]
    try:
        cursor.execute("SELECT MAX(number) FROM feedback;")
        count = cursor.fetchone()[0]
        
        stmt = """INSERT INTO feedback (number, user_id, feedback, day) VALUES ({}, {}, '{}', {});""".format(count + 1 if isinstance(count, int) else 0, id, feedback, day)
        cursor.execute(stmt)
    except Exception:
        return False


# Получение ссылки по дню
def get_link(day):
    try:
        cursor.execute("SELECT link FROM links WHERE day = {};".format(day))
        return cursor.fetchone()[0]
    except Exception:
        return False
    