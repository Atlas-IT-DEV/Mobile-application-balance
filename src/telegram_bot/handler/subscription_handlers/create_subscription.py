from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import SubScripts
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class CreateSubscriptionHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/create_subscription\n"
             "user_id=ID\n"
             "fee_id=ID\n"
             "type_sub_id=ID\n"
             "</pre>\n\n"
             "<code>UserID обязательный</code>\n"
             "<code>FeeID обязательный</code>\n"
             "<code>TypeSubID обязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command create_subscription")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Напиши команду в формате:</b>\n"
                    f"{CreateSubscriptionHandler.FORMA}"
                    "<i>На улице дождь?</i>"
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

            if not text.startswith('/create_subscription'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{CreateSubscriptionHandler.FORMA}"
                    "<i>Чем он тебе не понравился? -_-</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[user_id] = _get_param(text, {
                "user_id": "int",   # ID пользователя   обязательный
                "fee_id": "int",    # ID сбора   обязательный
                "type_sub_id": "int"    # ID типа подписки   обязательный
            })

            if self.DATA[user_id]:
                log.debug(f"Current data for user {user_id}: {self.DATA[user_id]}")

                # Преобразуем данные в формат, соответствующий Pydantic модели
                subscription_data = Subscriptions(user_id=self.DATA[user_id]["user_id"], fee_id=self.DATA[user_id]["fee_id"], type_sub_id=self.DATA[user_id]["type_sub_id"]).dict(by_alias=True)

                response = requests.post(
                    f'http://{self.HOST}:{self.SERVER_PORT}/subscriptions/',
                    json=subscription_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Подписка создана успешно.",
                                    f"Ошибка при создании подписки: \n{response.text}")

                del self.DATA[user_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{CreateSubscriptionHandler.FORMA}"
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
