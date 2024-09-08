from src.database.my_connector import db
from src.database.models import SubCategories


def get_all_sub_categories():
    query = "SELECT * FROM sub_categories"
    return db.fetch_all(query)


def get_sub_category_by_id(sub_category_id: int):
    query = "SELECT * FROM sub_categories WHERE id=%s"
    return db.fetch_one(query, (sub_category_id,))


def create_sub_category(sub_category: SubCategories):
    query = "INSERT INTO sub_categories (type) VALUES (%s)"
    params = sub_category.Type
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_sub_category(sub_category_id: int, sub_category: SubCategories):
    query = "UPDATE sub_categories SET type=%s WHERE id=%s"
    params = sub_category.Type, sub_category_id
    db.execute_query(query, params)


def delete_sub_category(sub_category_id: int):
    query = "DELETE FROM sub_categories WHERE id=%s"
    db.execute_query(query, (sub_category_id,))
