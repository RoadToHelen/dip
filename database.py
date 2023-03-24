import psycopg2
# import sqlalchemy

# DSN = 'postgresql://postgres:12345@localhost:5432/neto'
# engine = sqlalchemy.create_engine(DSN)
# connection = engine.connect()


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
    with connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        vk_id VARCHAR(9) PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20),
        vk_link VARCHAR(30) NOT NULL
        );
    ''')
    print('Таблица users создана')

def insert_users(vk_id, first_name, last_name, vk_link):
    with connection.cursor() as cursor:
        cursor.execute('''
        INSERT INTO users(vk_id, first_name, last_name, vk_link)
    VALUES
        ('{vk_id}', '{first_name}', '{last_name}', '{vk_link}'
        );
    ''')

def drop_users():
    with connection.cursor() as cursor:
        cursor.execute('''
        DROP TABLE IF EXISTS users;
        '''
        )
        print('Таблица users удалена')
