import psycopg2
from config import get_env

cursor, connection = None, None

# Загрузка базы данных
def load(show_all=False):
    global cursor, connection

    connection = psycopg2.connect(host=get_env("host"),
                                  user=get_env("user"),
                                  password=get_env("password"),
                                  database=get_env("database"))
    connection.autocommit = True
    cursor = connection.cursor()

    # Вывести все доступные базы данных
    if show_all:
        cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        a = cursor.fetchall()
        for el in a:
            try:
                cursor.execute("SELECT * FROM {};".format(el[0]))
                print(el[0])
                print(cursor.fetchall())
            except:
                pass
        
    # cursor.execute("DELETE FROM emotrack WHERE username = 'Айван';")
    # cursor.execute("ALTER TABLE feedback ADD day INT;")

    try:
        cursor.execute("SELECT username FROM emotrack;")
    except:
        # Создание базы данных при ее отсутствии
        cursor.execute("""
            CREATE TABLE emotrack(
                id INT PRIMARY KEY,
                username VARCHAR(15),
                gender VARCHAR(6),
                email VARCHAR(30),
                day INT,
                time VARCHAR(12),
                blocks INT,
                breath BOOL,
                send BOOL,
                city VARCHAR(255)
            );""")
    cursor.execute("SELECT version();")
    print("Connect to database {} correctly".format(cursor.fetchone()))

    # Вывод всех пользователей при старте
    cursor.execute("SELECT username FROM emotrack;")
    print("Users: ", ", ".join([user[0] for user in cursor.fetchall()]))

    return cursor, connection


# Выгрузка базы данных
def unload():
    cursor.close()
    connection.close()
