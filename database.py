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
    print('database neto was created')


# connection = psycopg2.connect(
#     database='neto',
#     user='postgres',
#     password='12345',
#     host='localhost',
#     port='5432'
# )

connection.autocommit = True


def create_users():
    with connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER(9) PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20),
        bdate VARCHAR(10), NOT NULL,
        city_id INTEGER(9) NOT NULL,
        relation INTEGER(1) NOT NULL
        );
    ''')
    print('TABLE users was created')


def create_dating_users():
    with connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dating_users(
        id SERIAL PRIMARY KEY,
        d_user_id INTEGER(9) NOT NULL,
        user_id INTEGER(9) NOT NULL
        );
    ''')


def create_compilation():
    with connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS compilation (
        user_id INTEGER(9) NOT NULL REFERENCES users(user_id),
        d_user_id INTEGER(9) NOT NULL REFERENCES dating_users(user_id),
        CONSTRAINT pk PRIMARY KEY (user_id, d_user_id
        );
    ''')


def insert_users(user_id, first_name, last_name, ):
    with connection.cursor() as cursor:
        cursor.execute('''
        INSERT INTO users(user_id, first_name, last_name, vk_link) 
    VALUES
        ({user_id}, {first_name}, {last_name}, {vk_link}
        );
    ''')


def insert_dating_users(du_vk_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute('''
        INSERT INTO dating_users(du_vk_id, user_id) 
    VALUES
        ({du_vk_id}, {user_id}
        );
        ''')
