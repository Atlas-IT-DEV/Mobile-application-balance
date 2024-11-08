from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import Users
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class EditUserHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/edit_user\n"
             "user_id=ID\n"
             "name=Имя\n"
             "telegram_id=ID\n"
             "phone=Номер телефона\n"
             "count_bonus=Количество бонусов пользователя\n"
             "referal=Пригласил ли пользователь друга? (True/False)"
             "</pre>\n\n"
             "<code>UserID обязательный</code>\n"
             "<code>Name необязательный</code>\n"
             "<code>TelegramID обязательный</code>\n"
             "<code>Phone необязательный</code>\n"
             "<code>CountBonus необязательный</code>\n"
             "<code>Referal необязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command edit_user")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Сначала напиши команду в формате:</b>\n"
                    f"{EditUserHandler.FORMA}"
                    "<i>Имя пользователя - неразрывная строка</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.info(f"Handling message from user {update.message.from_user.id}")
        try:
            user_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/edit_user'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditUserHandler.FORMA}"
                    "<i>Повнимательнее?</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[user_id] = _get_param(text, {
                "user_id": "int",
                "name": "str",
                "telegram_id": "int",
                "phone": "str",
                "count_bonus": "int",
                "referal": "bool"
            })

            if self.DATA[user_id]:
                log.info(f"Current data for user {user_id}: {self.DATA[user_id]}")

                user = requests.get(
                    f'http://{self.HOST}:{self.SERVER_PORT}/users/id/{self.DATA[user_id]["user_id"]}'
                )
                user = User(**user.json()).dict(by_alias=True)

                user_data = {
                    "name": self.DATA.get(user_id, {}).get("name", user.get("name")),
                    "telegram_id": self.DATA.get(user_id, {}).get("telegram_id", user.get("telegram_id")),
                    "phone": self.DATA.get(user_id, {}).get("phone", user.get("phone")),
                    "count_bonus": self.DATA.get(user_id, {}).get("count_bonus", user.get("count_bonus")),
                    "referal": self.DATA.get(user_id, {}).get("referal", user.get("referal")),
                }

                response = requests.put(
                    f'http://{self.HOST}:{self.SERVER_PORT}/users/{self.DATA[user_id]["user_id"]}',
                    json=user_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Пользователь изменен успешно.",
                                    f"Ошибка при изменении пользователя: \n{response.text}")

                del self.DATA[user_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditUserHandler.FORMA}"
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
