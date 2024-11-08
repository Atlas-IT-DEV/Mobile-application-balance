from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class DelSubscriptionHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/del_subscription\n"
             "subscription_id=ID"
             "</pre>\n\n"
             "<code>SubscriptionID обязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command del_subscription")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Напиши команду в формате:</b>\n"
                    f"{DelSubscriptionHandler.FORMA}"
                    "<i>На улице дождь?</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.debug(f"Handling message from user {update.message.from_user.id}")
        try:
            subscription_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/del_subscription'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{DelSubscriptionHandler.FORMA}"
                    "<i>Чем он тебе не понравился? -_-</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[subscription_id] = _get_param(text, {
                "subscription_id": "int"
            })

            if self.DATA[subscription_id]:
                log.debug(f"Current data for subscription {subscription_id}: {self.DATA[subscription_id]}")

                response = requests.delete(
                    f'http://{self.HOST}:{self.SERVER_PORT}/subscriptions/{self.DATA[subscription_id]["subscription_id"]}',
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Подписка удалена успешно.",
                                    f"Ошибка при удалении подписки: \n{response.text}")

                del self.DATA[subscription_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{DelSubscriptionHandler.FORMA}"
                    "<i>По второму кругу.</i>"
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
