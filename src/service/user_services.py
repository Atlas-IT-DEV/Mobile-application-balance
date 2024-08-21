from src.repository import user_repository
from src.database.models import User
from fastapi import HTTPException, status, Form
from src.utils.hashing import validate_password


def get_all_users():
    users = user_repository.get_all_users()
    return [Users(**user) for user in users]


def get_user_by_id(user_id: int):
    user = user_repository.get_user_by_id(user_id)
    return Users(**user) if user else None


def get_user_by_phone(phone: str):
    user = user_repository.get_user_by_phone(phone)
    return Users(**user) if user else None


def create_user(user: User):
    user_id = user_repository.create_user(user)
    return get_user_by_id(user_id)


def update_user(user_id: int, user: User):
    user_repository.update_user(user_id, user)
    return {"message": "User updated successfully"}


def delete_user(user_id: int):
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}

