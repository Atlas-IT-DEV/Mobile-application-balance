from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.utils.custom_logging import setup_logging
from config import Config
log = setup_logging()
config = Config()


class AddPermitionHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/add_permition\n"
             "telegram_id=ID"
             "</pre>"
             "Вы можете ввести сразу несколько ID через запятую вот так:\n"
             "12345,67890\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command add permition")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Напиши команду в формате:</b>\n"
                    f"{AddPermitionHandler.FORMA}"
                    "<i>И пожелай удачи</i>"
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

            if not text.startswith('/add_permition'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{AddPermitionHandler.FORMA}"
                    "<i>Удача не помогла</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[user_id] = _get_param(text, {
                "telegram_id": "str"
            })

            if user_id in self.DATA:
                log.debug(f"Current data for user {user_id}: {self.DATA[user_id]}")

                # Добавляем администратора в переменные среды
                config.__setattr__("AUTHORIZED_USERS", self.DATA[user_id]["telegram_id"])

                await update.message.reply_text("Администраторы успешно добавлены.", parse_mode="HTML")

                del self.DATA[user_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{AddPermitionHandler.FORMA}"
                    "<i>Попробуй еще раз.</i>"
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