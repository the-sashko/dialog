#!/usr/bin/python3

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

#to-do: add logs
class Handler:
    __telegram = None
    __gpt = None
    __storage = None
    __tts = None
    __image = None
    __ascii = None
    __logger = None

    def __init__(self) -> None:
        self.__telegram = Telegram()
        self.__gpt = Gpt()
        self.__storage = Storage()
        self.__tts = Tts()
        self.__image = Image()
        self.__ascii = Ascii()
        self.__logger = Logger()

    def do_handle(
        self,
        command: Command,
        message: TelegramMessage,
        reply_to_message_id: Union[int, None]
    ) -> None:
        self.__logger.log('Start handling commands')

        if command.get_type() == Command.IMAGE:
            self.__logger.log('Start handling %s command' % Command.IMAGE)
            self.__do_command_image(command, message, reply_to_message_id)
            self.__logger.log('End handling %s command' % Command.IMAGE)

        if command.get_type() == Command.VOICE:
            self.__logger.log('Start handling %s command' % Command.VOICE)
            self.__do_command_voice(command, message, reply_to_message_id)
            self.__logger.log('End handling %s command' % Command.VOICE)

        if command.get_type() == Command.ASCII:
            self.__logger.log('Start handling %s command' % Command.ASCII)
            self.__do_command_ascii(command, message, reply_to_message_id)
            self.__logger.log('End handling %s command' % Command.ASCII)

        self.__logger.log('End handling commands')

        return None

    def __do_command_voice(
            self,
            command: Command,
            message: TelegramMessage,
            reply_to_message_id: Union[int, None]
    ) -> None:
        if command.get_value() == None:
            self.__logger.log('Command %s does not have value' % Command.VOICE)

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
        self.__telegram.sendVoice(
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
        if command.get_value() == None:
            self.__logger.log('Command %s does not have value' % Command.IMAGE)

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

            reply = self.__gpt.paraphrase('Вибач, братан, але я не зміг це намалювати. Може спрбуємо намалювати щось інше?', 'apologies')#TO-DO: to const

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

    def __do_command_ascii(
        self,
        command: Command,
        message: TelegramMessage,
        reply_to_message_id: Union[int, None]
    ) -> None:
        if command.get_value() == None:
            self.__logger.log('Command %s does not have value' % Command.ASCII)

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

            reply = self.__gpt.paraphrase('Вибач, братан, але я не зміг це зробити. Може спрбуємо намалювати щось інше?', 'apologies')#TO-DO: to const

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
