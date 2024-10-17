import sqlite3
from sqlite3 import Connection, Cursor
from os import path
import logging

connection: Connection
cur: Cursor


class DB():

    def load_database(dbname="db.sqlite3"):
        global connection, cur

        try:
            logging.info("Connecting database")
            dbname = path.join("database", dbname)
            connection = sqlite3.connect(dbname)
            cur = connection.cursor()

            logging.info("Database connected")
        except:
            logging.error("Database connection failed")
            raise ValueError("Database connection failed")

    def create_tables():
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cur.fetchall()]

        if not "users" in tables:
            logging.info("Creating table users")
            cur.execute("""create table users (
                            id integer primary key autoincrement,
                            telegram_id bigint not null,
                            name varchar(50) not null,
                            username varchar(50),
                            role varchar(15) not null default 'user',
                            registered timestamp
                            )""")

        if not "repetitions" in tables:
            logging.info("Creating table repetitions")
            cur.execute("""create table repetitions (
                            id integer primary key autoincrement,
                            chat_id bigint not null,
                            message_id int not null,
                            button_text varchar(30) default '',
                            button_link varchar(100) default '',
                            time_to_send timestamp,
                            confirmed bool default false,
                            is_send bool default false
                            )""")

        connection.commit()

    def get(prompt, values=[], one=False):
        try:
            cur.execute(prompt, values)
            if one:
                return cur.fetchone()
            else:
                return cur.fetchall()
        except Exception as e:
            logging.warning("Prompt " + prompt + " with values " + str(values) + " failed")
            logging.warning(e)
            return False

    def get_dict(prompt, values=[], one=False):
        try:
            cur.execute(prompt, values)
            desc = [row[0] for row in cur.description]
            if one:
                return dict(zip(desc, cur.fetchone()))
            else:
                return [dict(zip(desc, res)) for res in cur.fetchall()]
        except Exception as e:
            logging.warning("Prompt " + prompt + " with values " + str(values) + " failed")
            logging.warning(e)
            return False

    def commit(prompt, values=[]):
        try:
            cur.execute(prompt, values)
            connection.commit()
            return True
        except Exception as e:
            logging.warning("Prompt " + prompt + " with values " + str(values) + " failed")
            logging.warning(e)
            return False

    def commit_many(prompt, values=[]):
        try:
            cur.executemany(prompt, values)
            connection.commit()
            return True
        except Exception as e:
            logging.warning("Prompt " + prompt + " with values " + str(values) + " failed")
            logging.warning(e)
            return False

    def unload_database():
        logging.info("Closing database")
        connection.close()
        logging.info("Database closed")
