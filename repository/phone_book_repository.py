import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",  # имя пользователя бд
        password="root",  # пароль пользователя бд
        host="127.0.0.1",
        port=3306,
        database="phone_book_db"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def login(user_name, password):
    cur.execute(f'SELECT * FROM users where user_name = "{user_name}" and password = "{password}"')
    for (id, user_name, password, birth_date) in cur:
        return id, user_name, password
def addContactIn_book_users(user_id, user_name, phone, birth_date):
    cur.execute(f'INSERT INTO book_users (user_id, name, phone, birth_date) values ({user_id}, "{user_name}", "{phone}", "{birth_date}")')
    conn.commit()


def addUserIn_users(user_name, password, birth_date):
    cur.execute(f'INSERT INTO users (user_name, password, birth_date) values ("{user_name}", "{password}", "{birth_date}")')
    conn.commit()
    return cur.lastrowid

def getAllUsers():
    cur.execute('SELECT * FROM users ORDER BY user_name;')
    users = []
    for (id, user_name, password, birth_date) in cur:
        users.append({'id': id, 'user_name': user_name, 'password': password, 'birth_date': birth_date})

    return users


def getAllUsersByUserId(user_id):
    cur.execute(f'SELECT name, phone, birth_date FROM book_users where user_id = {user_id} ORDER BY name;')
    users = []
    for (user_name, phone, birth_date) in cur:
        users.append({'user_name': user_name, 'phone': phone, 'birth_date': birth_date})

    return users



def getUsersByBirthDate(user_id):
    #cur.execute(f'SELECT * FROM book_users WHERE WEEK(NOW()) = WEEK( birth_date + INTERVAL (YEAR(NOW()) - YEAR(birth_date)) YEAR ) AND user_id = {user_id} ORDER BY name;')\
    cur.execute(f'SELECT * FROM book_users WHERE DATEDIFF(NOW(),birth_date)%365 BETWEEN 0 AND 7 AND user_id = {user_id} ORDER BY name;')
    users = []
    for (user_id, user_name, phone, birth_date) in cur:
        users.append({'user_name': user_name, 'phone': phone, 'birth_date': birth_date})

    return users


def getUserByNamePhoneBirthDate(user_name, phone, birth_date, user_id):
    cur.execute(f'SELECT * FROM book_users where name = "{user_name}" and phone = "{phone}" and birth_date = "{birth_date}" and user_id = {user_id} ORDER BY name;;')
    for (user_id, user_name, phone, birth_date) in cur:
        return user_id, user_name, phone, birth_date


def updateUser(user_id, user_name, phone, birth_date, update_user_name, update_phone, update_birth_date):
    cur.execute(f'UPDATE book_users set name = "{update_user_name}", phone = "{update_phone}", birth_date = "{update_birth_date}"'
                f'WHERE user_id = {user_id} and name = "{user_name}" and phone = "{phone}" and birth_date = "{birth_date}"')
    conn.commit()


def deleteBookUser(user_id, user_name, phone, birth_date):
    cur.execute(f'DELETE FROM book_users WHERE user_id = {user_id} and name = "{user_name}" and phone = "{phone}" and birth_date = "{birth_date}"')
    conn.commit()


def addUserEmailIn_users_email(email):
    cur.execute(f'INSERT INTO users_email (email) values ("{email}");')
    conn.commit()


