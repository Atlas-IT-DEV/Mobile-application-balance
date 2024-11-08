from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import SubScripts
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class EditSubscriptionHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/edit_subscription\n"
             "subscription_id=ID\n"
             "user_id=ID\n"
             "fee_id=ID\n"
             "type_sub_id=ID\n"
             "</pre>\n\n"
             "<code>SubscriptionID обязательный</code>\n"
             "<code>UserID обязательный</code>\n"
             "<code>FeeID обязательный</code>\n"
             "<code>TypeSubID обязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command edit_subscription")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Сначала напиши команду в    формате:</b>\n"
                    f"{EditSubscriptionHandler.FORMA}"
                    "<i>Имя подписки - неразрывная строка</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.info(f"Handling message from user {update.message.from_user.id}")
        try:
            subscription_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/edit_subscription'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditSubscriptionHandler.FORMA}"
                    "<i>Повнимательнее?</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[subscription_id] = _get_param(text, {
                "subscription_id": "int",   # ID подписки   обязательный
                "user_id": "int",           # ID пользователя   обязательный
                "fee_id": "int",            # ID сбора   обязательный
                "type_sub_id": "int"        # ID типа подписки   обязательный
            })

            if self.DATA[subscription_id]:
                log.info(f"Current data for subscription {subscription_id}: {self.DATA[subscription_id]}")

                subscription = requests.get(
                    f'https://{self.HOST}:{self.SERVER_PORT}/subscriptions/subscription_id/{self.DATA[subscription_id]["subscription_id"]}'
                )   # Получаем информацию о подписке
                subscription = Subscriptions(**subscription.json()).dict(by_alias=True)

                subscription_data = {
                    "id": None,
                    "user_id": self.DATA.get(subscription_id, {}).get("user_id", subscription.get("user_id")),
                    "fee_id": self.DATA.get(subscription_id, {}).get("fee_id", subscription.get("fee_id")),
                    "type_sub_id": self.DATA.get(subscription_id, {}).get("type_sub_id", subscription.get("type_sub_id")),
                }

                response = requests.put(
                    f'http://{self.HOST}:{self.SERVER_PORT}/subscriptions/{self.DATA[subscription_id]["subscription_id"]}',
                    json=subscription_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Подписка изменена успешно.",
                                    f"Ошибка при изменении подписки: \n{response.text}")

                del self.DATA[subscription_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditSubscriptionHandler.FORMA}"
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
