from src.database.my_connector import Database
from src.database.models import Products
db = Database()


async def get_all_products():
    query = "SELECT * FROM products"
    return await db.fetch_all(query)


async def get_product_by_id(product_id: int):
    query = "SELECT * FROM products WHERE id=%s"
    return await db.fetch_one(query, (product_id,))


async def create_product(product: Products):
    query = ("INSERT INTO products (name, price, company_id, category_id, image_id)"
             " VALUES (%s, %s, %s, %s, %s)")
    params = (product.Name, product.Price, product.CompanyID, product.CategoryID, product.ImageID)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_product(product_id: int, product: Products):
    query = "UPDATE products SET name=%s, price=%s, company_id=%s, category_id=%s, image_id=%s WHERE id=%s"
    params = (product.Name, product.Price, product.CompanyID, product.CategoryID, product.ImageID, product_id)
    await db.execute_query(query, params)


async def delete_product(product_id: int):
    query = "DELETE FROM products WHERE id=%s"
    await db.execute_query(query, (product_id,))
