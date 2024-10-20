from src.database.my_connector import db
from src.database.models import SubCategories
from typing import Dict


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


def update_sub_category(sub_category_id: int, sub_category: Dict):
    fields_to_update = [f"{key}=%s" for key in sub_category.keys()]
    params = list(sub_category.values())
    query = f"UPDATE sub_categories SET {', '.join(fields_to_update)} WHERE id=%s"
    params.append(sub_category_id)
    db.execute_query(query, tuple(params))


def delete_sub_category(sub_category_id: int):
    query = "DELETE FROM sub_categories WHERE id=%s"
    db.execute_query(query, (sub_category_id,))
