from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _inf_response, format_data_to_html
import requests
from src.utils.custom_logging import setup_logging
log = setup_logging()


class GetUsersListHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/get_users_list"
             "</pre>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command get_users_list")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Подтвердите ввод команды:</b>\n"
                    f"{GetUsersListHandler.FORMA}"
                    "<i>Логика кода просит)</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.debug(f"Handling message from user {update.message.from_user.id}")
        try:
            user_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/get_users_list'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{GetUsersListHandler.FORMA}"
                    "<i>Все прелести станут твои, тебе нужно всего лишь...</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            response = requests.get(
                f'http://{self.HOST}:{self.SERVER_PORT}/users/',
            )

            messages = format_data_to_html(response.json(), max_width=4096)

            for message in messages:
                await _inf_response(update, response,
                                    f"{message}",
                                    f"Ошибка при получении списка пользователей: \n{response.text}")

            return ConversationHandler.END
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
