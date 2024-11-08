from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import Fees
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
from datetime import datetime
log = setup_logging()


class CreateFeeHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/create_fee\n"
             "name=Имя\n"
             "description=Описание\n"
             "final_cost=Ожидания\n"
             "gathered_cost=Накопления\n"
             "duration=Длительность\n"
             "fee_category_id=КатегорияID\n"
             "image_url=Путь\n"
             "</pre>\n\n"
             "<code>Name обязательный</code>\n"
             "<code>Desc необязательный</code>\n"
             "<code>FCost обязательный</code>\n"
             "<code>GCost обязательный</code>\n"
             "<code>Duration обязательный</code>\n"
             "<code>FeeCategoryID обязательный</code>\n"
             "<code>ImageUrl необязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command create_fee")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Напиши команду в формате:</b>\n"
                    f"{CreateFeeHandler.FORMA}"
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

            if not text.startswith('/create_fee'):
                instructions = (        # ID категории сборов   обязательный
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{CreateFeeHandler.FORMA}"
                    "<i>Чем он тебе не понравился? -_-</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[user_id] = _get_param(text, {
                "name": "str",
                "description": "str",
                "final_cost": "float",
                "gathered_cost": "float",
                "duration": "int",
                "fee_category_id": "int",
                "image_url": "str"
            })

            if self.DATA[user_id]:
                log.debug(f"Current data for user {user_id}: {self.DATA[user_id]}")

                # Преобразуем данные в формат, соответствующий Pydantic модели
                fee_data = Fees(**self.DATA[user_id]).dict(by_alias=True)
                fee_data["created_at"] = f"{fee_data['created_at']}"
                fee_data["date_finish"] = f"{fee_data['date_finish']}"

                response = requests.post(
                    f'http://{self.HOST}:{self.SERVER_PORT}/fees/',
                    json=fee_data,
                    headers=get_token(),
                    params={"duration": self.DATA[user_id].get("duration")}
                )

                await _inf_response(update, response,
                                    "Категория сборов создана успешно.",
                                    f"Ошибка при создании категории сборов: \n{response.text}")

                del self.DATA[user_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{CreateFeeHandler.FORMA}"
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
