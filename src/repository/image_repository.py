from src.database.my_connector import db
from src.database.models import Images


def get_all_images():
    query = "SELECT * FROM images"
    return db.fetch_all(query)


def get_image_by_id(image_id: int):
    query = "SELECT * FROM images WHERE id=%s"
    return db.fetch_one(query, (image_id,))


def create_image(image: Images):
    query = "INSERT INTO images (url) VALUES (%s)"
    params = image.Url
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_image(image_id: int, image: Images):
    query = "UPDATE images SET url=%s WHERE id=%s"
    params = (image.Url, image_id)
    db.execute_query(query, params)


def delete_image(image_id: int):
    query = "DELETE FROM images WHERE id=%s"
    db.execute_query(query, (image_id,))
