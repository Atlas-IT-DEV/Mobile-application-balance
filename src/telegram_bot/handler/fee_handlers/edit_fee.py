from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.telegram_bot.handler.base_hendlers import BaseCommandHandler, _check, _cancel, _get_param, _inf_response
import requests
from src.database.models import Fees
from src.utils.custom_logging import setup_logging
from src.utils.admin_auth_bot import get_token
log = setup_logging()


class EditFeeHandler(BaseCommandHandler):
    CHOOSING, WAITING_FOR_PHOTO = range(2)

    FORMA = ("<pre>"
             "/edit_fee\n"
             "fee_id=ID\n"
             "name=Имя\n"
             "description=Описание\n"
             "final_cost=Ожидания\n"
             "gathered_cost=Накопления\n"
             "created_at=Старт\n"
             "date_finish=Закрытие\n"
             "fee_category_id=КатегорияID\n"
             "image_url=Путь\n"
             "</pre>\n\n"
             "<code>FeeID обязательный</code>\n"
             "<code>Name обязательный</code>\n"
             "<code>Desc необязательный</code>\n"
             "<code>FCost обязательный</code>\n"
             "<code>GCost обязательный</code>\n"
             "<code>CreatedAt необязательный</code>\n"
             "<code>DateFinish необязательный</code>\n"
             "<code>FeeCategoryID обязательный</code>\n"
             "<code>ImageUrl необязательный</code>\n\n")

    async def start(self, update: Update, context: CallbackContext) -> int:
        log.info("Command edit_fee")
        try:
            if await self.check_authorized(update):
                instructions = (
                    "<b>Сначала напиши команду в формате:</b>\n"
                    f"{EditFeeHandler.FORMA}"
                    "<i>Имя категории сборов - неразрывная строка</i>"
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

            if not text.startswith('/edit_fee'):
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditFeeHandler.FORMA}"
                    "<i>Повнимательнее?</i>"
                )
                await update.message.reply_text(instructions, parse_mode="HTML")
                return self.CHOOSING

            self.DATA[user_id] = _get_param(text, {
                "fee_id": "int",
                "name": "str",
                "description": "str",
                "final_cost": "float",
                "gathered_cost": "float",
                "created_at": "date",
                "date_finish": "date",
                "fee_category_id": "int",
                "image_url": "str"
            })

            if self.DATA[user_id]:
                log.info(f"Current data for fee {user_id}: {self.DATA[user_id]}")

                fee = requests.get(
                    f'http://{self.HOST}:{self.SERVER_PORT}/fees/fee_id/{self.DATA[user_id]["fee_id"]}'
                )
                fee = Fees(**fee.json()).dict(by_alias=True)

                fee_data = {
                    "name": self.DATA.get(user_id, {}).get("name", fee.get("name")),
                    "description": self.DATA.get(user_id, {}).get("description", fee.get("description")),
                    "final_cost": self.DATA.get(user_id, {}).get("final_cost", fee.get("final_cost")),
                    "gathered_cost": self.DATA.get(user_id, {}).get("gathered_cost", fee.get("gathered_cost")),
                    "created_at": self.DATA.get(user_id, {}).get("created_at", fee.get("created_at")),
                    "date_finish": self.DATA.get(user_id, {}).get("date_finish", fee.get("date_finish")),
                    "fee_category_id": self.DATA.get(user_id, {}).get("fee_category_id", fee.get("fee_category_id")),
                    "image_url": self.DATA.get(user_id, {}).get("image_url", fee.get("image_url")),
                }

                fee_data["created_at"] = f"{fee_data['created_at']}"
                fee_data["date_finish"] = f"{fee_data['date_finish']}"

                response = requests.put(
                    f'http://{self.HOST}:{self.SERVER_PORT}/fees/{self.DATA[user_id]["fee_id"]}',
                    json=fee_data,
                    headers=get_token()
                )

                await _inf_response(update, response,
                                    "Категория сборов изменена успешно.",
                                    f"Ошибка при изменении категории сборов: \n{response.text}")

                del self.DATA[user_id]
                return ConversationHandler.END
            else:
                instructions = (
                    "<b>Некорректный ввод команды. Используй команду в формате: </b>\n"
                    f"{EditFeeHandler.FORMA}"
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
