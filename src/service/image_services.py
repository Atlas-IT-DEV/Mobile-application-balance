from src.repository import image_repository
from src.database.models import Images
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists


def get_all_images():
    images = image_repository.get_all_images()
    return [Images(**image) for image in images]


def get_image_by_id(image_id: int):
    image = image_repository.get_image_by_id(image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return Images(**image) if image else None


def create_image(image: Images):
    check_if_exists(
        get_all=get_all_images,
        attr_name="Url",
        attr_value=image.Url,
        exception_detail='Image already exist'
    )
    image_id = image_repository.create_image(image)
    return get_image_by_id(image_id)


def update_image(image_id: int, image: Images):
    check_for_duplicates(
        get_all=get_all_images,
        check_id=image_id,
        attr_name="Url",
        attr_value=image.Url,
        exception_detail='Image already exist'
    )
    image_repository.update_image(image_id, image)
    return {"message": "Image updated successfully"}


def delete_image(image_id: int):
    get_image_by_id(image_id)
    image_repository.delete_image(image_id)
    return {"message": "Image deleted successfully"}
