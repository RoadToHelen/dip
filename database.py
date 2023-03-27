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
            vk_id VARCHAR(20) PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30)
            );
        ''')
        print('Таблица users создана')
    except KeyError:
        return


def create_dating_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dusers(
             du_vk_id VARCHAR(20) PRIMARY KEY,
             du_first_name VARCHAR(30) NOT NULL,
             du_last_name VARCHAR(30),
             vk_id VARCHAR(20)
            );
        ''')
        print('Таблица dusers создана')
    except KeyError:
        return


def create_compilation():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS compilation (
            vk_id VARCHAR(20) NOT NULL REFERENCES users(vk_id),
            du_vk_id VARCHAR(20) NOT NULL REFERENCES dusers(du_vk_id),
            CONSTRAINT pk PRIMARY KEY (vk_id, du_vk_id)
            );
        ''')
        print('Таблица compilation создана')
    except KeyError:
        return

def insert_dating_users(du_vk_id,  du_first_name,  du_last_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO users( du_vk_id,  du_first_name,  du_last_name)
            VALUES
            ('%s', '%s', '%s');
            '''
            % ( du_vk_id,  du_first_name,  du_last_name),
        )
        print('dating_user добавлен в таблицу')
    except KeyError:
        return


def insert_users(vk_id, first_name, last_name):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO dusers(vk_id, first_name, last_name)
            VALUES
            ('%s', '%s', '%s');
            '''
            % (vk_id, first_name, last_name),
        )
        connection.commit()
        cursor.close()
        print('user добавлен в таблицу')
    except KeyError:
        return


def select_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM users''')
            print(cursor.fetchall())
    except KeyError:
        return


def select_dating_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM dusers''')
            print(cursor.fetchall())
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
