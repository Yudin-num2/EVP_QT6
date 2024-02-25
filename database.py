import psycopg
import configparser
import logging

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = config.get('Postgre', 'user')
PASSWORD = config.get('Postgre', 'password')
DATABASE = config.get('Postgre', 'database')

def authorization(login: str, passw: str) -> bool:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users_authorization WHERE login = %s AND passw = %s", (login, passw))
                return True if cur.fetchall() else False

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def get_users():
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT (surname, name) FROM users_authorization")
                users = cur.fetchall()
                workers_list = []
                for user in users:
                    surname_name = list(user[0])
                    workers_list.append(' '.join(surname_name))
                
                return workers_list

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')

def select_tasks() -> list:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT task, workers, status FROM current_tasks")
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def add_task(task: str, workers: str, tech_card: str = None):

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                query = cur.execute("INSERT INTO current_tasks(task, workers, tech_card) VALUES(%s, %s, %s)", (task, workers, tech_card))
                print(query)

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')

def select_technological_cards() -> list:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM technological_cards")
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')

def select_machines_name():
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM machines")
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')