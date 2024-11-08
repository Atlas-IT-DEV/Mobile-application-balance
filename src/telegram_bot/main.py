import os
from src.utils.custom_logging import setup_logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.telegram_bot.handler.start_handlers import StartHandler

from src.telegram_bot.handler.user_handlers.get_users_list_handlers import GetUsersListHandler
from src.telegram_bot.handler.user_handlers.create_user_handlers import CreateUserHandler
from src.telegram_bot.handler.user_handlers.edit_user_handlers import EditUserHandler
from src.telegram_bot.handler.user_handlers.del_user_handlers import DelUserHandler

from src.telegram_bot.handler.fee_category_handlers.get_fee_categories_list import GetFeeCategoriesListHandler
from src.telegram_bot.handler.fee_category_handlers.create_fee_category import CreateFeeCategoryHandler
from src.telegram_bot.handler.fee_category_handlers.edit_fee_category import EditFeeCategoryHandler
from src.telegram_bot.handler.fee_category_handlers.del_fee_category import DelFeeCategoryHandler

from src.telegram_bot.handler.sub_category_handlers.get_sub_categories_list import GetSubCategoriesListHandler
from src.telegram_bot.handler.sub_category_handlers.create_sub_category import CreateSubCategoryHandler
from src.telegram_bot.handler.sub_category_handlers.edit_sub_category import EditSubCategoryHandler
from src.telegram_bot.handler.sub_category_handlers.del_sub_category import DelSubCategoryHandler

from src.telegram_bot.handler.fee_handlers.get_fees_list import GetFeesListHandler
from src.telegram_bot.handler.fee_handlers.create_fee import CreateFeeHandler
from src.telegram_bot.handler.fee_handlers.edit_fee import EditFeeHandler
from src.telegram_bot.handler.fee_handlers.del_fee import DelFeeHandler

from src.telegram_bot.handler.history_payment_handlers.get_history_payments_list import GetHistoryPaymentsListHandler
from src.telegram_bot.handler.history_payment_handlers.create_history_payment import CreateHistoryPaymentHandler
from src.telegram_bot.handler.history_payment_handlers.edit_history_payment import EditHistoryPaymentHandler
from src.telegram_bot.handler.history_payment_handlers.del_history_payment import DelHistoryPaymentHandler

from src.telegram_bot.handler.history_payment_handlers.get_history_payment_by_fee import GetHistoryPaymentByFeeHandler
from src.telegram_bot.handler.history_payment_handlers.get_history_payment_by_fee_user import GetHistoryPaymentByFeeUserHandler
from src.telegram_bot.handler.history_payment_handlers.get_history_payment_by_user import GetHistoryPaymentByUserHandler

from src.telegram_bot.handler.image_upload_handlers.image_upload_fee import ImageUploadFeeHandler
from src.telegram_bot.handler.image_upload_handlers.image_delete_fee import ImageDeleteFeeHandler

from src.telegram_bot.handler.permition_handlers.add_permition_handlers import AddPermitionHandler
from src.telegram_bot.handler.permition_handlers.del_permition_handlers import DelPermitionHandler

from src.telegram_bot.handler.subscription_handlers.create_subscription import CreateSubscriptionHandler
from src.telegram_bot.handler.subscription_handlers.edit_subscription import EditSubscriptionHandler
from src.telegram_bot.handler.subscription_handlers.del_subscription import DelSubscriptionHandler
from src.telegram_bot.handler.subscription_handlers.get_subscriptions_list import GetSubscriptionsListHandler
from src.telegram_bot.handler.subscription_handlers.get_subscription_by_fee import GetSubscriptionByFeeHandler
from src.telegram_bot.handler.subscription_handlers.get_subscription_by_user import GetSubscriptionByUserHandler

from config import Config
config = Config()
log = setup_logging()


class BalanceBot:

    def __init__(self):
        self.TELEGRAM_TOKEN = config.__getattr__("TELEGRAM_TOKEN")

    @staticmethod
    def _application_add_handler(class_method, command_name):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler(command_name, class_method.start)],
            states={
                class_method.CHOOSING: [
                    MessageHandler(filters.TEXT, class_method.handle_message)
                ],
                class_method.WAITING_FOR_PHOTO: [
                    MessageHandler(filters.ALL, class_method.handle_photo)
                ]
            },
            fallbacks=[CommandHandler('cancel', class_method.cancel)]
        )
        return conv_handler

    def start_bot(self):
        log.info("Started bot process")
        try:
            application = Application.builder().token(self.TELEGRAM_TOKEN).build()

            # Приветственное сообщение
            application.add_handler(self._application_add_handler(StartHandler(), 'start'))

            # Получение списка пользователей
            application.add_handler(self._application_add_handler(GetUsersListHandler(), 'get_users_list'))
            # Изменение пользователя
            application.add_handler(self._application_add_handler(EditUserHandler(), 'edit_user'))
            # Создание пользователя
            application.add_handler(self._application_add_handler(CreateUserHandler(), 'create_user'))
            # Удаление букета
            application.add_handler(self._application_add_handler(DelUserHandler(), 'del_user'))

            # Получение списка категорий сборов
            application.add_handler(self._application_add_handler(GetFeeCategoriesListHandler(), 'get_fee_categories_list'))
            # Создание категории сборов
            application.add_handler(self._application_add_handler(CreateFeeCategoryHandler(), 'create_fee_category'))
            # Изменение категории сборов
            application.add_handler(self._application_add_handler(EditFeeCategoryHandler(), 'edit_fee_category'))
            # Удаление категории сборов
            application.add_handler(self._application_add_handler(DelFeeCategoryHandler(), 'del_fee_category'))

            # Получение списка типов подписок
            application.add_handler(self._application_add_handler(GetSubCategoriesListHandler(), 'get_sub_categories_list'))
            # Создание типа подписок
            application.add_handler(self._application_add_handler(CreateSubCategoryHandler(), 'create_sub_category'))
            # Изменение типа подписок
            application.add_handler(self._application_add_handler(EditSubCategoryHandler(), 'edit_sub_category'))
            # Удаление типа подписок
            application.add_handler(self._application_add_handler(DelSubCategoryHandler(), 'del_sub_category'))

            # Получение списка сборов
            application.add_handler(self._application_add_handler(GetFeesListHandler(), 'get_fees_list'))
            # Создание сборов
            application.add_handler(self._application_add_handler(CreateFeeHandler(), 'create_fee'))
            # Изменение сборов
            application.add_handler(self._application_add_handler(EditFeeHandler(), 'edit_fee'))
            # Удаление сборов
            application.add_handler(self._application_add_handler(DelFeeHandler(), 'del_fee'))

            # Получение списка истории платежей
            application.add_handler(self._application_add_handler(GetHistoryPaymentsListHandler(), 'get_history_payments_list'))
            # Создание истории платежей
            application.add_handler(self._application_add_handler(CreateHistoryPaymentHandler(), 'create_history_payment'))
            # Изменение истории платежей
            application.add_handler(self._application_add_handler(EditHistoryPaymentHandler(), 'edit_history_payment'))
            # Удаление истории платежей
            application.add_handler(self._application_add_handler(DelHistoryPaymentHandler(), 'del_history_payment'))

            # Получение истории платежей по ID сбора
            application.add_handler(self._application_add_handler(GetHistoryPaymentByFeeHandler(), 'get_history_payment_by_fee'))
            # Получение истории платежей по ID сбора и ID пользователя
            application.add_handler(self._application_add_handler(GetHistoryPaymentByFeeUserHandler(), 'get_history_payment_by_fee_user'))
            # Получение истории платежей по ID пользователя
            application.add_handler(self._application_add_handler(GetHistoryPaymentByUserHandler(), 'get_history_payment_by_user'))

            # Загрузка изображения сбора
            application.add_handler(self._application_add_handler(ImageUploadFeeHandler(), 'image_upload_fee'))
            # Удаление изображения сбора
            application.add_handler(self._application_add_handler(ImageDeleteFeeHandler(), 'image_delete_fee'))

            # Добавление администратора
            application.add_handler(self._application_add_handler(AddPermitionHandler(), 'add_permition'))
            # Удаление администратора
            application.add_handler(self._application_add_handler(DelPermitionHandler(), 'del_permition'))

            # Создание подписки
            application.add_handler(self._application_add_handler(CreateSubscriptionHandler(), 'create_subscription'))
            # Изменение подписки
            application.add_handler(self._application_add_handler(EditSubscriptionHandler(), 'edit_subscription'))
            # Удаление подписки
            application.add_handler(self._application_add_handler(DelSubscriptionHandler(), 'del_subscription'))
            # Получение списка подписок
            application.add_handler(self._application_add_handler(GetSubscriptionsListHandler(), 'get_subscriptions_list'))
            # Получение подписки по ID сбора
            application.add_handler(self._application_add_handler(GetSubscriptionByFeeHandler(), 'get_subscription_by_fee'))
            # Получение подписки по ID пользователя
            application.add_handler(self._application_add_handler(GetSubscriptionByUserHandler(), 'get_subscription_by_user'))

            log.info("Bot handler added. Starting polling")
            application.run_polling()
        except Exception as ex:
            log.exception(f"{ex}")
        log.info("Bot startup complete")
