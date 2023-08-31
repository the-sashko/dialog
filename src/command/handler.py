#!/usr/bin/python3

import re
import os
from typing import Union
from telegram.telegram import Telegram
from telegram.message import Message as TelegramMessage
from gpt.gpt import Gpt
from storage.storage import Storage
from tts.tts import Tts
from image.image import Image
from command.command import Command
from ascii.ascii import Ascii
from logger.logger import Logger
from notification.notification import Notification
from settings.settings import Settings

#to-do: add logs
class Handler:
    __telegram = None
    __gpt = None
    __storage = None
    __tts = None
    __image = None
    __ascii = None
    __logger = None
    __notification = None

    __main_chat_id = None

    def __init__(self) -> None:
        self.__telegram = Telegram()
        self.__gpt = Gpt()
        self.__storage = Storage()
        self.__tts = Tts()
        self.__image = Image()
        self.__ascii = Ascii()
        self.__logger = Logger()
        self.__notification = Notification()

        telegram_config = Settings().get_telegram_config()

        self.__main_chat_id = telegram_config['main_chat_id']

    def do_handle(
        self,
        command: Command,
        message: TelegramMessage,
        reply_to_message_id: Union[int, None]
    ) -> None:
        self.__logger.log('Start handling commands')

        if command.get_type() == Command.IMAGE:
            self.__logger.log(f'Start handling {Command.IMAGE} command')
            self.__do_command_image(command, message, reply_to_message_id)
            self.__logger.log(f'End handling {Command.IMAGE} command')

        if command.get_type() == Command.VOICE:
            self.__logger.log(f'Start handling {Command.VOICE} command')
            self.__do_command_voice(command, message, reply_to_message_id)
            self.__logger.log(f'End handling {Command.VOICE} command')

        if command.get_type() == Command.ASCII:
            self.__logger.log(f'Start handling {Command.ASCII} command')
            self.__do_command_ascii(command, message, reply_to_message_id)
            self.__logger.log(f'End handling {Command.ASCII} command')

        if command.get_type() == Command.SAY:
            self.__logger.log(f'Start handling {Command.SAY} command')
            self.__do_command_say(command, message)
            self.__logger.log(f'End handling {Command.SAY} command')

        if command.get_type() == Command.SAY_ALL:
            self.__logger.log(f'Start handling {Command.SAY_ALL} command')
            self.__do_command_say_all(command, message)
            self.__logger.log(f'End handling {Command.SAY_ALL} command')

        if command.get_type() == Command.VERSION:
            self.__logger.log(f'Start handling {Command.VERSION} command')
            self.__do_command_version(command, message, reply_to_message_id)
            self.__logger.log(f'End handling {Command.VERSION} command')

        self.__logger.log('End handling commands')

    def __do_command_version(
            self,
            command: Command,
            message: TelegramMessage,
            reply_to_message_id: Union[int, None]
    ) -> None:
        self.__logger.log('Start sending version message')

        app_version = os.getenv('DIALOG_APP_VERSION')

        self.__telegram.send_message(
            app_version,
            message.get_chat().get_id(),
            reply_to_message_id
        )

        self.__logger.log('End sending version message')

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {'role': 'assistant', 'content': command.get_value()}
        )

        return None

    def __do_command_voice(
            self,
            command: Command,
            message: TelegramMessage,
            reply_to_message_id: Union[int, None]
    ) -> None:
        if command.get_value() is None:
            self.__logger.log(f'Command {Command.VOICE} does not have value')

            reply = self.__gpt.paraphrase('Я не буду це казати', 'angry')#TO-DO: to const

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

            return None

        self.__logger.log('Start generating voice message')
        audio_file_path = self.__tts.text2audio(command.get_value())
        self.__logger.log('End generating voice message')

        self.__logger.log('Start sending voice message')
        self.__telegram.send_voice(
            message.get_chat().get_id(),
            audio_file_path,
            reply_to_message_id
        )
        self.__logger.log('End sending voice message')

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {'role': 'assistant', 'content': command.get_value()}
        )

        return None

    def __do_command_image(
        self,
        command: Command,
        message: TelegramMessage,
        reply_to_message_id: Union[int, None]
    ) -> None:
        if command.get_value() is None:
            self.__logger.log(f'Command {Command.IMAGE} does not have value')

            reply = self.__gpt.paraphrase('Я не буду це малювати', 'angry')#TO-DO: to const

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

            return None

        self.__logger.log('Start generating image')
        image_path = self.__image.create_image(command.get_value())
        self.__logger.log('End generating image')

        if image_path is None:
            self.__logger.log('Image generating is failed')

            reply = self.__gpt.paraphrase(
                'Вибач, братан, але я не зміг це намалювати. Може спрбуємо намалювати щось інше?',
                'apologies'
            )#TO-DO: to const

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

            return None

        self.__logger.log('Start sending image')
        self.__telegram.send_photo(
            message.get_chat().get_id(),
            None,
            image_path,
            reply_to_message_id
        )
        self.__logger.log('End sending image')

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {'role': 'assistant', 'content': 'Надіслав тобі зображення'}
        )

        return None

#    def __do_command_say(
#        self,
#        command: Command,
#        message: TelegramMessage
#    ) -> None:
#        if not message.get_chat().is_admin_chat():
#            self.__logger.log_error(f'Command {Command.SAY} can be executed only by admin')

#            return None

#        if command.get_value() is None:
#            self.__logger.log(f'Command {Command.SAY} does not have value')

#            return None

#        message_text = command.get_value()

#        chat_id = self.__main_chat_id

#        pattern = r'^(\d+)(.*?)$'

#        if (re.search(pattern, message_text, flags=re.IGNORECASE) is not None):
#            chat_id = re.sub(pattern, r'\g<1>', message_text, 0, re.IGNORECASE)
#            chat_id = re.sub(r'\s+', r' ', chat_id)
#            chat_id = re.sub(r'((^\s+)|(\s+$))', r'', chat_id)
#            chat_id = int(chat_id)

#            message_text = re.sub(pattern, r'\g<2>', message_text, 0, re.IGNORECASE)
#            message_text = re.sub(r'\s+', r' ', message_text)
#            message_text = re.sub(r'((^\s+)|(\s+$))', r'', message_text)

#        if message_text is None or message_text == '':
#            message_text = None

#        if chat_id is None or chat_id < 1:
#            chat_id = None

#        if message_text is None:
#            self.__logger.log('Nothing to say')

#            return None

#        if chat_id is None:
#            self.__logger.log('Invalid chat_id')

#            return None

#        self.__storage.save_message(
#            message.get_user().get_id(),
#            message.get_chat().get_id(),
#            message.get_user().get_name(),
#            message.get_chat().get_title(),
#            {'role': 'assistant', 'content': message_text}
#        )

#        self.__notification.send(message_text, chat_id)

    def __do_command_say_all(
        self,
        command: Command,
        message: TelegramMessage
    ) -> None:
        if not message.get_chat().is_admin_chat():
            self.__logger.log_error(f'Command {Command.SAY_ALL} can be executed only by admin')

            return None

        if command.get_value() is None:
            self.__logger.log(f'Command {Command.SAY_ALL} does not have value')

            return None

        self.__notification.send_all(command.get_value())

    def __do_command_say(
        self,
        command: Command,
        message: TelegramMessage
    ) -> None:
        if not message.get_chat().is_admin_chat():
            self.__logger.log_error(f'Command {Command.SAY} can be executed only by admin')

            return None

        if command.get_value() is None:
            self.__logger.log(f'Command {Command.SAY} does not have value')

            return None

        self.__notification.send(
            command.get_value(),
            self.__main_chat_id
        )

    def __do_command_ascii(
        self,
        command: Command,
        message: TelegramMessage,
        reply_to_message_id: Union[int, None]
    ) -> None:
        if command.get_value() is None:
            self.__logger.log(f'Command {Command.ASCII} does not have value')

            reply = self.__gpt.paraphrase('Я не буду цього робити', 'angry')#TO-DO: to const

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

            return None

        self.__logger.log('Start generating ASCII')
        ascii_image = self.__ascii.create(command.get_value())
        self.__logger.log('End generating ASCII')

        if ascii_image is None:
            self.__logger.log('Generating ASCII is failed')

            reply = self.__gpt.paraphrase(
                'Вибач, братан, але я не зміг це зробити. Може спрбуємо намалювати щось інше?',
                'apologies'
            )#TO-DO: to const

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

            return None

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {'role': 'assistant', 'content': 'Надіслав тобі ASCII зображення'}
        )

        self.__logger.log('Start sending ASCII')
        self.__telegram.send_message(
            '`' + ascii_image + '`',
            message.get_chat().get_id(),
            reply_to_message_id,
            True
        )
        self.__logger.log('End sending ASCII')

        return None
