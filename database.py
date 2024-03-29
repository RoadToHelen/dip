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
    print('Database neto created')

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    database='neto',
    password='12345'
)

connection.autocommit = True

# class DBTools:
def create_users():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            vk_id INTEGER PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30)
            );
            ''')
        print('Table users created')
        return


def insert_users(vk_id, first_name, last_name):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO users(vk_id, first_name, last_name)
        VALUES
        ('%s', '%s', '%s');
        '''
        % (vk_id, first_name, last_name)
    )
    connection.commit()
    cursor.close()
    print('user added at table')


def select_users():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM users''')
        result = cursor.fetchall()
        return result

def select_duser_ids():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT vk_id FROM users''')
        result = cursor.fetchall()
        return result


def check_users(duser_id):
    cursor = connection.cursor()
    cursor.execute(f'''SELECT vk_id FROM users WHERE vk_id ={duser_id};''')
    out = cursor.fetchall()
    cursor.close()
    return out


def drop_users():
    with connection.cursor() as cursor:
        cursor.execute('''
        DROP TABLE IF EXISTS users;
        '''
        )
        print('Table users deleted')


def drop_db_users():
    with connection.cursor() as cursor:
        cursor.execute('''
        DROP DATABASE IF EXISTS users;
        '''
        )
        print('Database users deleted')
