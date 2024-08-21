from src.repository import characteristic_repository
from src.database.models import Сharacteristics
from fastapi import HTTPException, status


async def get_all_characteristics():
    characteristics = await haracteristic_repository.get_all_characteristics()
    return [Сharacteristics(**characteristic) for characteristic in characteristics]


async def get_characteristic_by_id(characteristic_id: int):
    characteristic = await characteristic_repository.get_characteristic_by_id(characteristic_id)
    return Сharacteristics(**characteristic) if characteristic else None


async def create_characteristic(characteristic: Сharacteristics):
    characteristic_id = await characteristic_repository.create_characteristic(characteristic)
    return await get_characteristic_by_id(characteristic_id)


async def update_characteristic(characteristic_id: int, characteristic: Сharacteristics):
    await characteristic_repository.update_characteristic(characteristic_id, characteristic)
    return {"message": "Characteristic updated successfully"}


async def delete_characteristic(characteristic_id: int):
    await characteristic_repository.delete_characteristic(characteristic_id)
    return {"message": "Characteristic deleted successfully"}
