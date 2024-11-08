import os
import re
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from config import Config
from src.utils.custom_logging import setup_logging
from datetime import datetime
log = setup_logging()
config = Config()


class BaseCommandHandler(ABC):

    def __init__(self):
        self.DATA = {}
        self.HOST = config.__getattr__("HOST")
        self.SERVER_PORT = config.__getattr__("SERVER_PORT")
        self.AUTHORIZED_USERS = self.__list__(config.__getattr__("AUTHORIZED_USERS"))

    @staticmethod
    def __list__(s: str):
        return list(map(int, s.split(',')))

    @abstractmethod
    async def start(self, update: Update, context: CallbackContext) -> int:
        pass

    @abstractmethod
    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        pass

    @abstractmethod
    async def handle_photo(self, update: Update, context: CallbackContext) -> int:
        pass


async def _check(update: Update, AUTHORIZED_USERS: list):
    user_id = update.message.from_user.id
    if user_id in AUTHORIZED_USERS:
        return True
    else:
        await update.message.reply_text('<b>Тебе здесь не рады.</b>', parse_mode="HTML")
        return False


async def _cancel(self, update: Update) -> int:
    user_id = update.message.from_user.id
    if user_id in self.DATA:
        del self.DATA[user_id]
    await update.message.reply_text('<b>Операция отменена.</b>', parse_mode="HTML")
    return ConversationHandler.END


def _get_param(text, dir_params):
    result_params = {}

    # Разбиваем текст на строки по переводу строки
    lines = text.strip().splitlines()

    # Обрабатываем каждую строку
    for line in lines:
        # Разделяем строку на ключ и значение по первому знаку равно
        if '=' not in line:
            continue
        key, value = map(str.strip, line.split('=', 1))

        # Проверяем, что ключ присутствует в исходных параметрах
        if key in dir_params:
            if dir_params[key] == "str":
                result_params[key] = value
            elif dir_params[key] == "int":
                try:
                    result_params[key] = int(value)
                except ValueError:
                    print(f"Не удалось преобразовать '{value}' к типу int для ключа '{key}'")
            elif dir_params[key] == "bool":
                result_params[key] = value.lower() in ('true', '1', 'yes')
            elif dir_params[key] == "float":
                try:
                    result_params[key] = float(value.replace(',', '.'))  # Учитываем запятую как разделитель
                except ValueError:
                    print(f"Не удалось преобразовать '{value}' к типу float для ключа '{key}'")
            elif dir_params[key] == "date":
                # Пробуем различные форматы дат, чтобы избежать ошибок
                date_formats = [
                    "%d.%m.%Y",       # Формат: день.месяц.год
                    "%Y-%m-%d",       # Формат: год-месяц-день
                    "%Y",             # Формат: только год
                    "%Y-%m-%d %H:%M:%S"  # Формат: год-месяц-день часы:минуты:секунды
                ]
                for fmt in date_formats:
                    try:
                        result_params[key] = f"{datetime.strptime(value, fmt)}"
                        break
                    except ValueError:
                        continue
                else:
                    print(f"Не удалось преобразовать '{value}' к типу date для ключа '{key}'")

    print(result_params)

    return result_params


async def _inf_response(update: Update, response, access: str, error: str):
    if response.status_code == 200:
        await update.message.reply_text(access, parse_mode="HTML")
    else:
        await update.message.reply_text(error, parse_mode="HTML")


def format_data_to_html(data, max_width=4000, max_value_length=11):
    if not data:
        return ["<b>Нет данных для отображения.</b>"]

    # Обрезаем значения до max_value_length
    for item in data:
        for key, value in item.items():
            str_value = str(value)
            if len(str_value) > max_value_length:
                item[key] = f"{str_value[:max_value_length]}..."

    # Определяем ключи и переименовываем их
    key_map = {
        "telegram_id": "tg_id",
        "count_bonus": "bonus",
        "referal": "ref"
    }

    # Получаем все уникальные ключи и переименовываем их
    all_keys = set(key_map.get(key, key) for item in data for key in item.keys())
    keys = sorted(all_keys)  # Сортируем ключи для упрощения отображения

    # Определяем ширину каждого столбца
    column_widths = {key: max(len(str(item.get({v: k for k, v in key_map.items()}.get(key, key), ''))) for item in data) for key in keys}
    column_widths.update({key: max(len(key), column_widths[key]) for key in keys})  # Учитываем ширину заголовка
    total_width = sum(column_widths.values()) + len(keys) * 2  # Дополнительные пробелы для выравнивания

    # Проверяем, если общая ширина превышает максимальную
    if total_width > max_width:
        max_column_width = max_width // len(keys)
        column_widths = {key: min(width, max_column_width) for key, width in column_widths.items()}

    # Создаем заголовок таблицы
    html_content = "<b>Список данных:</b>\n\n<code>"
    html_content += "  ".join(f"{key.ljust(column_widths[key])}" for key in keys) + "\n"
    html_content += "-" * (sum(column_widths.values()) + len(keys) * 2 - 2) + "\n"

    # Форматируем каждую запись
    for item in data:
        row = "  ".join(f"{str(item.get({v: k for k, v in key_map.items()}.get(key, key), '')).ljust(column_widths[key])}" for key in keys)
        html_content += row + "\n"

    html_content += "</code>"

    # Разбиваем сообщение на части, если оно слишком длинное
    messages = []
    while len(html_content) > max_width:
        split_index = html_content.rfind("\n", 0, max_width)
        if split_index == -1:  # Если нет подходящего разрыва строки, разрываем по максимальной ширине
            split_index = max_width
        messages.append(html_content[:split_index].strip())
        html_content = html_content[split_index:].strip()
    messages.append(html_content)

    return messages
