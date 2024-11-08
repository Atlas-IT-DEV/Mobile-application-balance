from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import HistoryPays
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class EditHistoryPaymentHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/edit_history_payment\n"
             "history_payment_id=ID\n"
             "user_id=ID\n"
             "pay=Число\n"
             "</pre>\n\n"
             "<code>HistoryPaymentID обязательный</code>\n"
             "<code>UserID обязательный</code>\n"
             "<code>Pay необязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command edit_history_payment")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Сначала напиши команду в формате:</b>\n"
                    f"{EditHistoryPaymentHandler.FORMA}"
                    "<i>Имя категории сборов - неразрывная строка</i>"
                )
                await update.message.reply_text(instructions, parse_mode='HTML')
                return self.CHOOSING
        except Exception as ex:
            log.exception(f"Failed method: {ex}")

    async def handle_message(self, update: Update, context: CallbackContext) -> int:
        log.info(f"Handling message from user {update.message.from_user.id}")
        try:
            history_payment_id = update.message.from_user.id
            text = update.message.text

            if text.startswith('/cancel'):
                return await self.cancel(update)

            if not text.startswith('/edit_history_payment'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditHistoryPaymentHandler.FORMA}"
                    "<i>Повнимательнее?</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[history_payment_id] = _get_param(text, {
                "history_payment_id": "int",   # ID категории сборов   обязательный
                "user_id": "int",              # ID пользователя   обязательный
                "pay": "int"                   # Число оплаты необязательный
            })

            if self.DATA[history_payment_id]:
                log.info(f"Current data for history_payment {history_payment_id}: {self.DATA[history_payment_id]}")

                history_payment = requests.get(
                    f'https://{self.HOST}:{self.SERVER_PORT}/history_payments/history_payment_id/{self.DATA[history_payment_id]["history_payment_id"]}'
                )   # Получаем информацию о категории сборов
                history_payment = HistoryPays(**history_payment.json()).dict(by_alias=True)

                history_payment_data = {
                    "id": None,
                    "user_id": self.DATA.get(history_payment_id, {}).get("user_id", history_payment.get("user_id")),
                    "pay": self.DATA.get(history_payment_id, {}).get("pay", history_payment.get("pay")),
                }

                response = requests.put(
                    f'http://{self.HOST}:{self.SERVER_PORT}/history_payments/{self.DATA[history_payment_id]["history_payment_id"]}',
                    json=history_payment_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Категория сборов изменена успешно.",
                                    f"Ошибка при изменении категории сборов: \n{response.text}")

                del self.DATA[history_payment_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditHistoryPaymentHandler.FORMA}"
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
