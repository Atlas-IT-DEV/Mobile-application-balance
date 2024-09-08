from src.database.my_connector import db
from src.database.models import FeeCategories


def get_all_fee_categories():
    query = "SELECT * FROM fee_categories"
    return db.fetch_all(query)


def get_fee_category_by_id(fee_category_id: int):
    query = "SELECT * FROM fee_categories WHERE id=%s"
    return db.fetch_one(query, (fee_category_id,))


def create_fee_category(fee_category: FeeCategories):
    query = "INSERT INTO fee_categories (name) VALUES (%s)"
    params = fee_category.Name
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_fee_category(fee_category_id: int, fee_category: FeeCategories):
    query = "UPDATE fee_categories SET name=%s WHERE id=%s"
    params = fee_category.Name, fee_category_id
    db.execute_query(query, params)


def delete_fee_category(fee_category_id: int):
    query = "DELETE FROM fee_categories WHERE id=%s"
    db.execute_query(query, (fee_category_id,))
