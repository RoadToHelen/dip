import psycopg2


def create_db():
    initial_connection = psycopg2.connect(
        database='neto',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )
    initial_connection.close()
    print('БД neto создана')

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    database='neto',
    password='12345'
)

connection.autocommit = True

def create_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            vk_id VARCHAR(9) PRIMARY KEY,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20)
            );
        ''')
        print('Таблица users создана')
    except KeyError:
        return

def insert_users(vk_id, first_name, last_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO users(vk_id, first_name, last_name)
        VALUES
            ('{vk_id}', '{first_name}', '{last_name}'
            );
        ''')
    except KeyError:
        return

def drop_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            DROP TABLE IF EXISTS users;
            '''
            )
            print('Таблица users удалена')
    except KeyError:
        return

def drop_db_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            DROP DATABASE IF EXISTS users;
            '''
            )
            print('База данных users удалена')
    except KeyError:
        return
