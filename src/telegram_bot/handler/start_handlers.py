from telegram import Update
from telegram.ext import CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel
from src.utils.custom_logging import setup_logging
log = setup_logging()


class StartHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    async def start(self, update: Update, context: CallbackContext) -> None:
        log.info("Command start")
        try:
            if await self.check_authorized(update):
                await update.message.reply_text('Доброго дня администратирования. Используй команды из меню.')
        except Exception as ex:
            log.exception(f"Failed to send message: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        pass

    async def handle_photo(self, update: Update, context: CallbackContext) -> int:
        pass

    async def cancel(self, update: Update) -> int:
        return await _cancel(self, update)

    async def check_authorized(self, update: Update) -> bool:
        return await _check(update, self.AUTHORIZED_USERS)
