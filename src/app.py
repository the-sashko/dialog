#!/usr/bin/python3

import time
from telegram.telegram import Telegram
from telegram.message import Message as Telegram_Message
from handler.handler import Handler
from logger.logger import Logger

class App:
    __LOOP_DELAY = 0.5

    __telegram = None
    __handler = None
    __logger = None

    def __init__(self) -> None:
        self.__telegram = Telegram()
        self.__handler = Handler()
        self.__logger = Logger()

    def run(self) -> None:
        self.__logger.log('Strating...')

        while True:
            self.__loop()

    def __loop(self) -> None:
        time.sleep(self.__LOOP_DELAY)

        try:
            self.__handle_messages(self.__telegram.get_messages())
        except Exception as exp:
            self.__logger.log_error(exp)

    def __handle_messages(self, messages: list) -> None:
        for message in messages:
            self.__handle_message(message)

    def __handle_message(self, message: Telegram_Message) -> None:
        self.__logger.log('Start handling message from Telegram')
        self.__handler.do_handle(message)
        self.__logger.log('End handling message from Telegram')


if __name__ == '__main__':
    App().run()
