import psycopg2

class DBTools():
    def __init__(self, connection):
        self.connection = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            database='neto',
            password='12345'
        )

        # self.connection.autocommit = True

    def create_db(self):
        initial_connection = psycopg2.connect(
            database='neto',
            user='postgres',
            password='12345',
            host='localhost',
            port='5432'
        )
        initial_connection.close()
        print('Database neto created')

    def create_users(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                vk_id INTEGER PRIMARY KEY,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30)
                );
                ''')
            print('Table users created')
            return


    def insert_users(self, vk_id, first_name, last_name):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO users(vk_id, first_name, last_name)
            VALUES
            ('%s', '%s', '%s');
            '''
            % (vk_id, first_name, last_name)
        )
        self.connection.commit()
        cursor.close()
        print('user added at table')


    def select_users(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM users''')
            result = cursor.fetchall()
            return result


    def select_duser_ids(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT vk_id FROM users''')
            result = cursor.fetchall()
            return result


    def check_users(self, duser_id):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT vk_id FROM users WHERE vk_id ={duser_id};''')
        out = cursor.fetchall()
        cursor.close()
        return out


    def drop_users(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            cursor.execute('''
            DROP TABLE IF EXISTS users;
            '''
            )
            print('Table users deleted')


    def drop_db_users(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cursor:
            cursor.execute('''
            DROP DATABASE IF EXISTS users;
            '''
            )
            print('Database users deleted')
