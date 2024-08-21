from src.database.my_connector import Database
from src.database.models import ProductCharacteristics
from datetime import datetime
db = Database()


async def get_all_product_characteristics():
    query = "SELECT * FROM Product_Characteristics"
    return await db.fetch_all(query)


async def get_product_characteristic_by_id(product_characteristic_id: int):
    query = "SELECT * FROM Product_Characteristics WHERE id=%s"
    return await db.fetch_one(query, (product_characteristic_id,))


async def get_product_characteristic_by_user_id(user_id: int):
    query = "SELECT * FROM product_characteristics WHERE user_id=%s"
    return await db.fetch_all(query, (user_id,))


async def create_product_characteristic(product_characteristic: ProductCharacteristics):
    query = "INSERT INTO product_characteristics (product_id, characteristic_id, value) VALUES (%s, %s, %s)"
    params = (product_characteristic.ProductID, product_characteristic.CharacteristicID, product_characteristic.Value)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_product_characteristic(product_characteristic_id: int, product_characteristic: ProductCharacteristics):
    query = "UPDATE product_characteristics SET product_id=%s, characteristic_id=%s, value=%s WHERE id=%s"
    params = (product_characteristic.ProductID, product_characteristic.CharacteristicID, product_characteristic.Value,
              product_characteristic_id)
    await db.execute_query(query, params)


async def delete_order(product_characteristic_id: int):
    query = "DELETE FROM product_characteristics WHERE id=%s"
    await db.execute_query(query, (product_characteristic_id,))







