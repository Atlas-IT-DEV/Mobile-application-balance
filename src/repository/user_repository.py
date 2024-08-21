from src.database.my_connector import Database
from src.database.models import User
db = Database()


def get_all_users():
    query = "SELECT * FROM users"
    return db.fetch_all(query)


def get_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE id=%s"
    return db.fetch_one(query, (user_id,))


def get_user_by_phone(phone: str):
    query = "SELECT * FROM users WHERE phone=%s"
    return db.fetch_one(query, (phone,))


def create_user(user: User):
    query = ("INSERT INTO users (first_name, last_name, phone, INN, password, role)"
             " VALUES (%s, %s, %s, %s, %s, %s)")
    params = (user.FName, user.LName, user.Phone, user.INN, user.Password, user.Role)
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_user(user_id: int, user: User):
    query = "UPDATE users SET first_name=%s, last_name=%s, phone=%s, INN=%s, password=%s, role=%s WHERE id=%s"
    params = (user.FName, user.LName, user.Phone, user.INN, user.Password, user.Role, user_id)
    db.execute_query(query, params)


def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id=%s"
    db.execute_query(query, (user_id,))
