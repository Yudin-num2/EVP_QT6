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
                cur.execute("""SELECT * FROM users_authorization WHERE login = %s AND passw = %s""", (login, passw))
                return True if cur.fetchall() else False

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')

