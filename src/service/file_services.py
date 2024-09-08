import os
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.service.image_services import get_image_by_id, create_image, delete_image
from src.database.models import Images
from src.utils.write_file_into_server import write_file_into_server
from src.utils.return_url_object import return_url_object
from src.utils.list_to_str import encode_list_to_string, decode_string_to_list
from src.utils.custom_logging import setup_logging
from config import Config

config = Config()
log = setup_logging()


async def upload_images(entity_type: str, files: list[UploadFile],
                        entity_id: int, get_entity_by_id, update_entity):
    # Проверяем, существует ли сущность
    existing_entity = get_entity_by_id(entity_id)
    if not existing_entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{entity_type.capitalize()} with ID {entity_id} not found")
    image_ids = []
    for file in files:
        unique_filename = await write_file_into_server(entity_type, file)
        image = create_image(Images(url=f"/{entity_type}/{unique_filename}"))
        image_ids.append(image.ID)
    ids = encode_list_to_string(image_ids)
    existing_entity.ImageID = ids
    update_entity(entity_id, existing_entity)
    return get_entity_by_id(entity_id)


def download_images(entity_type: str, entity_id: int, get_entity_by_id):
    # Проверяем существование сущности
    entity = get_entity_by_id(entity_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{entity_type.capitalize()} with ID {entity_id} not found")
    image_ids = decode_string_to_list(entity.ImageID)
    urls = []
    for image_id in image_ids:
        # Проверяем данные в таблице со ссылками на изображения для сущности
        image = get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with ID {image_id} not found")
        file_path = os.path.join(config.__getattr__("UPLOAD_DIR"), entity_type, image.Url.split("/")[-1])
        if not os.path.exists(file_path):
            log.warning(f"File {file_path} does not exist.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not exists")
        url = return_url_object(image)
        urls.append(url)
    entity_dict = jsonable_encoder(entity.dict())
    return JSONResponse({
        entity_type: entity_dict,
        "urls": urls
    })


def delete_images(entity_type: str, image_ids: list[int]):
    deleted_images = []
    for image_id in image_ids:
        image = get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with ID {image_id} not found")
        file_path = os.path.join(config.__getattr__("UPLOAD_DIR"), entity_type, image.Url.split("/")[-1])
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"File {file_path} deleted successfully.")
        else:
            log.warning(f"File {file_path} does not exist.")
        delete_image(image_id)
        log.info(f"Image record with ID {image_id} deleted from database.")
        deleted_images.append(image_id)
    return {
        "status": "success",
        "deleted_images": deleted_images
    }
