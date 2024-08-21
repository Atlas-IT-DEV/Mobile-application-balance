from src.database.my_connector import Database
from src.database.models import Сharacteristics
db = Database()


async def get_all_characteristics():
    query = "SELECT * FROM characteristics"
    return await db.fetch_all(query)


async def get_characteristic_by_id(characteristic_id: int):
    query = "SELECT * FROM characteristics WHERE id=%s"
    return await db.fetch_one(query, (characteristic_id,))


async def create_characteristic(characteristic: Сharacteristics):
    query = "INSERT INTO characteristics (name, type) VALUES (%s, %s)"
    params = characteristic.Name, characteristic.Type
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_characteristic(characteristic_id: int, characteristic: Сharacteristics):
    query = "UPDATE characteristics SET name=%s, type=%s WHERE id=%s"
    params = characteristic.Name, characteristic.Type, characteristic_id
    await db.execute_query(query, params)


async def delete_characteristic(characteristic_id: int):
    query = "DELETE FROM characteristics WHERE id=%s"
    await db.execute_query(query, (characteristic_id,))
