import os
import uuid
from src.service import user_services, image_services, product_services
from src.database.models import Users, Images, Products
from fastapi import HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()
UPLOAD_DIR_PRODUCT = "./src/public/products"
UPLOAD_DIR_AVATAR = "./src/public/avatars"


async def upload_avatar(file: UploadFile = File(...), user: Users = None):
    file_location = await file_writer(file, UPLOAD_DIR_AVATAR)
    # Создаем информацию в базе данных о пути изображения
    image = await image_services.create_image(Images(url=file_location))
    user.IconID = image.ID
    update = await user_services.update_user(user.ID, user)
    if not update:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User update failed")
    # Получаем обновленного пользователя и проверяем данные
    updated_user = await user_services.get_user_by_id(user.ID)
    if not updated_user or updated_user.IconID is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User update failed")
    return updated_user


async def upload_product(file: UploadFile = File(...), product: Products = None):
    file_location = await file_writer(file, UPLOAD_DIR_PRODUCT)
    # Создаем информацию в базе данных о пути изображения
    image = await image_services.create_image(Images(url=file_location))
    product.ImageID = image.ID
    update = await product_services.update_product(product.ID, product)
    if not update:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Product update failed")
    # Получаем обновленный товар и проверяем данные
    updated_product = await product_services.get_product_by_id(product.ID)
    if not updated_product or updated_product.ImageID is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Product update failed")
    return updated_product


async def download_avatar(user: Users = None):
    # Проверяем данные в таблице со ссылками на изображения
    image = await image_services.get_image_by_id(user.IconID)
    if not image:
        raise HTTPException(status_code=404, detail="Image not exist")
    # Проверяем существование файла в папке
    if not os.path.exists(image.Url):
        raise HTTPException(status_code=404, detail="File not exist")
    return FileResponse(image.Url)


async def download_product(product: Products = None):
    # Проверяем данные в таблице со ссылками на изображения
    image = await image_services.get_image_by_id(product.ImageID)
    if not image:
        raise HTTPException(status_code=404, detail="Image not exist")
    # Проверяем существование файла в папке
    if not os.path.exists(image.Url):
        raise HTTPException(status_code=404, detail="File not exist")
    return FileResponse(image.Url)


async def file_writer(file, path):
    """
    Function for writing file.

    :param file: File to be written
    :param path: Path to file
    :return: File writer object
    """
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(path, unique_filename)
    os.makedirs(path, exist_ok=True)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    return file_location
