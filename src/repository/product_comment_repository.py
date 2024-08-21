from src.database.my_connector import Database
from src.database.models import ProductComments
db = Database()


async def get_all_product_comments():
    query = "SELECT * FROM product_comments"
    return await db.fetch_all(query)


async def get_product_comment_by_id(product_comment_id: int):
    query = "SELECT * FROM product_comments WHERE id=%s"
    return await db.fetch_one(query, (product_comment_id,))


async def create_product_comment(product_comment: ProductComments):
    query = "INSERT INTO product_comments (product_id, comment, created_at) VALUES (%s, %s, %s)"
    params = (product_comment.ProductID, product_comment.Comment, product_comment.CreatedAt)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_product_comment(product_commentt_id: int, product_comment: ProductComments):
    query = "UPDATE product_comments SET product_id=%s, comment=%s, created_at=%s WHERE id=%s"
    params = (product_comment.ProductID, product_comment.Comment, product_comment.CreatedAt, product_comment_id)
    await db.execute_query(query, params)


async def delete_product_comment(product_comment_id: int):
    query = "DELETE FROM product_comments WHERE id=%s"
    await db.execute_query(query, (product_comment_id,))
