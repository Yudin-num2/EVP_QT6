import psycopg
import configparser
import logging

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = config.get('Postgre', 'user')
PASSWORD = config.get('Postgre', 'password')
DATABASE = config.get('Postgre', 'database')

def authorization(login: str, passw: str) -> list:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users_authorization WHERE login = %s AND passw = %s", (login, passw))
                return cur.fetchall()

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def get_users() -> list:
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT surname, name FROM users_authorization")
                users = cur.fetchall()
                workers_list = []
                for user in users:
                    surname, name = user
                    workers_list.append(' '.join((surname, name)))
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
                cur.execute("SELECT * FROM current_tasks WHERE status <> 'Выполнено'")
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def add_task(task: str, workers: str = None, tech_card: str = None, photo_name: str = None) -> None:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO current_tasks(task, workers, tech_card, path_to_photo) VALUES(%s, %s, %s, %s)",
                                     (task, workers, tech_card, photo_name))
                conn.commit()

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
                cur.execute("SELECT name,operations FROM technological_cards")
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def select_machines_name() -> list:
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


def select_indicators() -> list:
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM indicators")
                indicators = cur.fetchall()
                indicators_list = []
                for indicator in indicators:
                    ind = list(indicator[0])
                    indicators_list.append(' '.join(ind))
                return indicators_list

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def select_task(task) -> list:
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM current_tasks WHERE task = %s ORDER BY datetime DESC", (task,))
                rows = cur.fetchall()
                return rows[0]

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def set_new_status(task, status, workers, author) -> None:

    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE current_tasks SET status = %s 
                            WHERE task = %s AND workers = %s AND author = %s""", (status, task, workers, author))
                conn.commit()

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def update_task_info(prev_task_name, prev_workers, task, workers) -> None:
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE current_tasks SET task = %s, workers = %s
                            WHERE task = %s AND workers = %s""", (task, workers, prev_task_name, prev_workers))
                conn.commit()

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')


def select_technological_operations(name):
    try:
        with psycopg.connect(host="127.0.0.1",
                              port=5432,
                              user=USERNAME,
                              password=PASSWORD,
                              dbname=DATABASE) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT operations FROM technological_cards WHERE name = %s", (name,))
                rows = cur.fetchall()
                return rows

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')