from sqliteorm import SQLiteORM
from sqliteorm.models.table import Table
from sqliteorm.models.fileds import IntegerColumn, TextColumn, DateTimeColumn, BooleanColumn
from os import path


# Initialize DB
db: SQLiteORM
users: Table
repetitions: Table

# Define a model
class Users(Table):
    id = IntegerColumn("id")
    telegram_id = IntegerColumn("telegram_id", is_null=False)
    name = TextColumn("name", is_null=False)
    username = TextColumn("username")
    role = TextColumn("role", default_value="user", is_null=False)
    restricted = BooleanColumn("restricted", default_value=False)
    registered = DateTimeColumn("registered", default_value="current_timestamp")

    def __init__(self, db):
        super().__init__(db, "users")


class Repetitions(Table):
    id = IntegerColumn("id")
    chat_id = IntegerColumn("chat_id", is_null=False)
    message_id = IntegerColumn("message_id", is_null=False)
    button_text = TextColumn("button_text", default_value="", is_null=False)
    button_link = TextColumn("button_link", default_value="", is_null=False)
    time_to_send = DateTimeColumn("time_to_send", is_null=False)
    confirmed = BooleanColumn("confirmed", default_value=False)
    is_send = BooleanColumn("is_send", default_value=False)

    def __init__(self, db):
        super().__init__(db, "repetitions")


def init_db():
    global db, users, repetitions

    db = SQLiteORM(path.join("database", "db.sqlite3"))

    # Register table
    users = Users(db)
    db.add_table(users)

    repetitions = Repetitions(db)
    db.add_table(repetitions)
