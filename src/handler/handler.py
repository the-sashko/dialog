#!/usr/bin/python3

import re
from typing import Union
from telegram.telegram import Telegram
from telegram.message import Message as Telegram_Message
from markov.markov import Markov
from gpt.gpt import Gpt
from storage.storage import Storage
from settings.settings import Settings
from tts.tts import Tts
from analyser.analyser import Analyser
from chance.chance import Chance
from command.parser import Parser as Command_Parser
from command.handler import Handler as Command_Handler
from logger.logger import Logger
from trigger.trigger import Trigger

#to-do: refactoring code syle
#to-do: add logs
class Handler:
    #TO-DO fit chances
    __CHANCE_TO_MODIFY_MARKOV_REPLY = 5
    __CHANCE_TO_REPLY_IN_PUBLIC_CHAT = 2
    __CHANCE_TO_REPLY_IN_AUDIO = 0

    __telegram = None
    __markov = None
    __gpt = None
    __storage = None
    __tts = None
    __analyser = None
    __chance = None
    __command_parser = None
    __command_handler = None
    __logger = None
    __trigger = None

    __telegram_bot_id = None
    __telegram_log_chat_id = None
    __bot_name = None

    def __init__(self) -> None:
        self.__telegram = Telegram()
        self.__markov = Markov()
        self.__gpt = Gpt()
        self.__storage = Storage()
        self.__tts = Tts()
        self.__analyser = Analyser()
        self.__chance = Chance()
        self.__command_parser = Command_Parser()
        self.__command_handler = Command_Handler()
        self.__logger = Logger()
        self.__trigger = Trigger()

        telegram_config = Settings().get_telegram_config()
        bot_config = Settings().get_bot_config()

        self.__telegram_log_chat_id = telegram_config['log_chat_id']

        self.__telegram_bot_id = telegram_config['bot_id']
        self.__bot_name = bot_config['name']

    def do_handle(self, message: Telegram_Message) -> None:
        if message.get_text() == None:
            return None
        
        if not message.get_chat().is_supported():
            return None

        if message.get_user().get_id() == self.__telegram_bot_id:
            return None

        reply_to_message_id = message.get_id()

        if (message.get_chat().is_private_type()):
            reply_to_message_id = None

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {"role": "user", "content": message.get_text()}
        )

        if self.__is_ignore(message):
            return None

        self.__logger.log('Start retrieving trigger from Telegram message')

        trigger_name = self.__analyser.get_trigger(message)

        if trigger_name is not None:
            self.__logger.log('Found %s trigger' % trigger_name)

        self.__logger.log('End retrieving trigger from Telegram message')

        if trigger_name is not None:
            return self.__trigger.fire(
                trigger_name,
                {
                    'chat_id': message.get_chat().get_id(),
                    'reply_to_message_id': reply_to_message_id,
                    'message': message
                }
            )

        self.__logger.log('Start retrieving command from Telegram message')

        command = self.__analyser.get_command(message)

        if command is not None:
            self.__logger.log('Found %s command' % command.get_type())

        self.__logger.log('End retrieving command from Telegram message')

        if command is not None:
            return self.__command_handler.do_handle(
                command,
                message,
                reply_to_message_id
            )

        self.__logger.log('Start retrieving mood from Telegram message')

        mood = self.__analyser.get_mood(message.get_text())

        self.__logger.log('Found %s mood' % mood)

        self.__logger.log('End retrieving mood from Telegram message')

        reply = self.__get_reply(message, mood)
        reply = self.__post_process(reply)

        if reply == None:
            return None
        
        if self.__is_reply_in_audio(message):
            audio_file_path = self.__tts.text2audio(reply)

            self.__telegram.send_voice(
                message.get_chat().get_id(),
                audio_file_path,
                reply_to_message_id
            )

            return None

        self.__telegram.send_message(
            reply,
            message.get_chat().get_id(),
            reply_to_message_id
        )

    def __get_reply(
        self,
        message: Telegram_Message,
        mood: str = 'neutral'
    ) -> Union[str, None]:
        if message.get_text() is None:
            return None

        reply = self.__markov.get_reply(message.get_text())

        if reply is None:
            return self.__gpt.get_reply(message, mood)

        if self.__chance.has(self.__CHANCE_TO_MODIFY_MARKOV_REPLY):
            reply = self.__gpt.paraphrase(reply, mood)

        return reply

    def __is_ignore(self, message: Telegram_Message) -> bool:        
        if message.get_chat().get_id() == self.__telegram_log_chat_id:
            return True

        if message.get_chat().is_private_type() or message.is_reply_to_me():
            return False

        if message.get_voice() is not None:
            return False

        pattern = r'^(.*?)' + re.escape(self.__bot_name) + r'(.*?)$'

        if re.search(pattern, message.get_text(), flags=re.IGNORECASE) is not None:
            return False

        if self.__command_parser.get_command_from_text(message.get_text()) is not None:
            return False

        if self.__chance.has(self.__CHANCE_TO_REPLY_IN_PUBLIC_CHAT):
            return False

        return True

    def __is_reply_in_audio(self, message: Telegram_Message) -> bool:
        if message.get_voice() is not None:
            return True
        
        #TO-DO: parse voice keywords

        if self.__chance.has(self.__CHANCE_TO_REPLY_IN_AUDIO):
            return True

        return False

    def __post_process(
        self,
        text: Union[str, None]
    ) -> Union[str, None]:
        #To-Do
        return text
