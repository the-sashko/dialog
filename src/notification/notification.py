from telegram.telegram import Telegram
from storage.storage import Storage
from logger.logger import Logger

class Notification:
    def __init__(self):
        self.__telegram = Telegram()
        self.__storage = Storage()
        self.__logger = Logger()

    def send(
        self,
        message: str,
        chat_id: int
    ) -> None:
        self.__logger.log(
            f'Start sending notification to chat (ID: {chat_id})'
        )

        self.__telegram.send_message(
            message,
            chat_id,
            None,
            True
        )

        self.__logger.log(
            f'End sending notification to chat (ID: {chat_id})'
        )

    def send_all(
        self,
        message: str
    ) -> None:
        chat_ids = self.__storage.get_all_chat_ids()

        if chat_ids is None:
            return None

        self.__logger.log(
            f'Start sending notification to all {len(chat_ids)} chats'
        )

        for chat_id in chat_ids:
            self.send(
                message,
                chat_id
            )

        self.__logger.log(
            f'End sending notification to all chats'
        )
