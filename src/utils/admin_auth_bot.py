from src.utils.custom_logging import setup_logging
from config import Config
import requests
config = Config()
log = setup_logging()


def get_token():
    response = requests.post(
        f'http://{config.__getattr__("HOST")}:{config.__getattr__("SERVER_PORT")}/signin/',
        json={
            "phone": "administr",
            "password": "234567623454322345"
        }
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
