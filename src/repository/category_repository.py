from src.database.my_connector import Database
from src.database.models import Categories
db = Database()


async def get_all_categories():
    query = "SELECT * FROM categories"
    return await db.fetch_all(query)


async def get_category_by_id(category_id: int):
    query = "SELECT * FROM categories WHERE id=%s"
    return await db.fetch_one(query, (category_id,))


async def create_category(category: Categories):
    query = "INSERT INTO categories (name) VALUES (%s)"
    params = category.Name
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_category(category_id: int, category: Categories):
    query = "UPDATE categories SET name=%s WHERE id=%s"
    params = category.Name, category_id
    await db.execute_query(query, params)


async def delete_category(category_id: int):
    query = "DELETE FROM categories WHERE id=%s"
    await db.execute_query(query, (category_id,))
