from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import SubCategories
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class EditSubCategoryHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/edit_sub_category\n"
             "sub_category_id=ID\n"
             "name=Имя\n"
             "</pre>\n\n"
             "<code>SubCategoryID обязательный</code>\n"
             "<code>Name необязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command edit_sub_category")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Сначала напиши команду в формате:</b>\n"
                    f"{EditSubCategoryHandler.FORMA}"
                    "<i>Имя категории сборов - неразрывная строка</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.info(f"Handling message from user {update.message.from_user.id}")
        try:
            sub_category_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/edit_sub_category'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditSubCategoryHandler.FORMA}"
                    "<i>Повнимательнее?</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[sub_category_id] = _get_param(text, {
                "sub_category_id": "int",   # ID категории сборов   обязательный
                "name": "str"                # Название категории сборов необязательный
            })

            if self.DATA[sub_category_id]:
                log.info(f"Current data for sub_category {sub_category_id}: {self.DATA[sub_category_id]}")

                sub_category = requests.get(
                    f'https://{self.HOST}:{self.SERVER_PORT}/sub_categories/sub_category_id/{self.DATA[sub_category_id]["sub_category_id"]}'
                )   # Получаем информацию о категории сборов
                sub_category = SubCategories(**sub_category.json()).dict(by_alias=True)

                sub_category_data = {
                    "id": None,
                    "type": self.DATA.get(sub_category_id, {}).get("type", sub_category.get("type")),
                    "name": self.DATA.get(sub_category_id, {}).get("name", sub_category.get("name")),
                }

                response = requests.put(
                    f'http://{self.HOST}:{self.SERVER_PORT}/sub_categories/{self.DATA[sub_category_id]["sub_category_id"]}',
                    json=sub_category_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Категория сборов изменена успешно.",
                                    f"Ошибка при изменении категории сборов: \n{response.text}")

                del self.DATA[sub_category_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditSubCategoryHandler.FORMA}"
                    "<i>Ну да, ну да, пошел я...</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed to handle message: {ex}")
            await update.message.reply_text('<b>Произошла ошибка при обработке информации.</b>', parse_mode="HTML")
            return self.CHOOSING

    async def handle_photo(self, update: Update, context: CallbackContext) -> int:
        return ConversationHandler.END

    async def cancel(self, update: Update) -> int:
        return await _cancel(self, update)

    async def check_authorized(self, update: Update) -> bool:
        return await _check(update, self.AUTHORIZED_USERS)
