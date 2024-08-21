from src.repository import product_comment_repository
from src.database.models import ProductComments


async def get_all_product_comments():
    product_comments = await product_comment_repository.get_all_product_comments()
    return [ProductComments(**product_comment) for product_comment in product_comments]


async def get_product_comment_by_id(product_comment_id: int):
    product_comment = await product_comment_repository.get_product_comment_by_id(product_comment_id)
    return ProductComments(**product_comment) if product_comment else None


async def create_product_comment(product_comment: ProductComments):
    product_comment_id = await product_comment_repository.create_product_comment(product_comment)
    return await get_product_comment_by_id(product_comment_id)


async def update_product_comment(product_comment_id: int, product_comment: ProductComments):
    await product_comment_repository.update_product_comment(product_comment_id, product_comment)
    return {"message": "Order comment updated successfully"}


async def delete_order_comment(order_comment_id: int):
    await order_comment_repository.delete_order_comment(order_comment_id)
    return {"message": "Order comment deleted successfully"}
