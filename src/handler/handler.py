import re
from typing import Union
from telegram.telegram import Telegram
from telegram.message import Message as TelegramMessage
from markov.markov import Markov
from gpt.gpt import Gpt
from storage.storage import Storage
from settings.settings import Settings
from tts.tts import Tts
from analyser.analyser import Analyser
from chance.chance import Chance
from command.parser import Parser as CommandParser
from command.handler import Handler as CommandHandler
from command.command import Command
from logger.logger import Logger
from trigger.trigger import Trigger
from post_processing.post_processing import PostProcessing

#to-do: refactoring code syle
#to-do: add logs
class Handler:
    #TO-DO fit chances
    __CHANCE_TO_MODIFY_MARKOV_REPLY = 5
    __CHANCE_TO_REPLY_IN_PUBLIC_CHAT = 5
    __CHANCE_TO_REPLY_IN_AUDIO = 1
    __CHANCE_TO_RANDOM_TEST = 1
    __CHANCE_TO_RANDOM_VOICE = 1
    __CHANCE_TO_RANDOM_IMAGE = 2

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
    __post_processing = None

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
        self.__command_parser = CommandParser()
        self.__command_handler = CommandHandler()
        self.__logger = Logger()
        self.__trigger = Trigger()
        self.__post_processing = PostProcessing()

        telegram_config = Settings().get_telegram_config()
        bot_config = Settings().get_bot_config()

        self.__telegram_log_chat_id = telegram_config['log_chat_id']

        self.__telegram_bot_id = telegram_config['bot_id']
        self.__bot_name = bot_config['name']

    def do_handle(self, message: TelegramMessage) -> None:
        #if (
        #    not message.get_chat().is_admin_chat() and
        #    not message.get_chat().is_main_chat()
        #):
        #    return self.do_simple_handle(message)

        try:
            if message.get_text() is None:
                self.__logger.log('Message text is empty. Skip')
                return None

            self.__logger.log(f'Message text is {message.get_text()}')

            if not message.get_chat().is_supported():
                self.__logger.log(f'Chat type is not supproted. Skip')
                return None

            if message.get_user().get_id() == self.__telegram_bot_id:
                self.__logger.log(f'This is my message. Skip')
                return None

            if message.get_chat().get_id() == self.__telegram_log_chat_id:
                self.__logger.log(f'This is log chat. Skip')
                return None

            reply_to_message_id = message.get_id()

            if message.get_chat().is_private_type():
                reply_to_message_id = None

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {"role": "user", "content": message.get_text()}
            )

            is_ignore = self.__is_ignore(message)
            trigger_name = None

            if is_ignore:
                trigger_name = self.__get_random_trigger(message)

            if is_ignore and trigger_name is None:
                self.__logger.log(f'This message should be ignored. Skip')
                return None

            self.__logger.log('Start retrieving trigger from Telegram message')

            if trigger_name is None:
                trigger_name = self.__analyser.get_trigger(message)

            if trigger_name is not None:
                self.__logger.log(f'Found {trigger_name} trigger')

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
                self.__logger.log(f'Found {command.get_type()} command')

            self.__logger.log('End retrieving command from Telegram message')

            if command is not None:
                return self.__command_handler.do_handle(
                    command,
                    message,
                    reply_to_message_id
                )

            self.__logger.log('Start retrieving mood from Telegram message')

            mood = self.__analyser.get_mood(message.get_text())

            self.__logger.log(f'Found {mood} mood')

            self.__logger.log('End retrieving mood from Telegram message')

            is_reply_in_audio = self.__is_reply_in_audio(message)

            reply = self.__get_reply(message, mood)
            reply = self.__post_process(reply, message, is_reply_in_audio)

            if reply is None:
                return None

            try:
                if is_reply_in_audio:
                    audio_file_path = self.__tts.text2audio(reply)

                    self.__telegram.send_voice(
                        message.get_chat().get_id(),
                        audio_file_path,
                        reply_to_message_id
                    )

                    return None
            except Exception as exp:
                self.__logger.log_error(exp)

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )
        except Exception as exp:
            self.__logger.log_error(exp)

            if not self.__is_mandatory_reply(message):
                return None

            self.__trigger.fire(
                self.__trigger.NONE_TRIGGER,
                {
                    'chat_id': message.get_chat().get_id(),
                    'reply_to_message_id': reply_to_message_id,
                    'message': message
                }
            )

        return None

    def do_simple_handle(self, message: TelegramMessage) -> None:
        try:
            if message.get_text() is None:
                return None

            if not message.get_chat().is_supported():
                return None

            if message.get_user().get_id() == self.__telegram_bot_id:
                return None

            if message.get_chat().get_id() == self.__telegram_log_chat_id:
                return None
        
            if message.get_voice() is not None:
                return None

            reply_to_message_id = message.get_id()

            if message.get_chat().is_private_type():
                reply_to_message_id = None

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {"role": "user", "content": message.get_text()}
            )

            is_ignore = self.__is_ignore(message)
            trigger_name = None

            if is_ignore:
                trigger_name = self.__get_random_trigger(message)

            if trigger_name != self.__trigger.RANDOM_TEXT_TRIGGER:
                trigger_name = None

            if is_ignore and trigger_name is None:
                return None

            if trigger_name is not None:
                return self.__trigger.fire(
                    trigger_name,
                    {
                        'chat_id': message.get_chat().get_id(),
                        'reply_to_message_id': reply_to_message_id,
                        'message': message
                    }
                )

            reply = self.__get_reply(message)
            reply = self.__post_process(reply, message, False)

            if reply is None:
                return None

            self.__telegram.send_message(
                reply,
                message.get_chat().get_id(),
                reply_to_message_id
            )

        except Exception as exp:
            self.__logger.log_error(exp)

            if not self.__is_mandatory_reply(message):
                return None

            self.__trigger.fire(
                self.__trigger.NONE_TRIGGER,
                {
                    'chat_id': message.get_chat().get_id(),
                    'reply_to_message_id': reply_to_message_id,
                    'message': message
                }
            )

        return None

    def __post_process(
        self,
        text: Union[str, None],
        message: TelegramMessage,
        is_reply_in_audio: bool
    ) -> Union[str, None]:
        return self.__post_processing.do_handle(
            text,
            self.__is_mandatory_reply(message),
            message.get_voice() is not None,
            is_reply_in_audio
        )

    def __get_reply(
        self,
        message: TelegramMessage,
        mood: str = 'neutral'
    ) -> Union[str, None]:
        if message.get_text() is None:
            return None

        reply = self.__markov.get_reply(message.get_text())

        if reply is None:
            return self.__gpt.get_reply(message, mood)

        if self.__chance.get(self.__CHANCE_TO_MODIFY_MARKOV_REPLY):
            reply = self.__gpt.paraphrase(reply, mood)

        return reply

    def __is_ignore(self, message: TelegramMessage) -> bool:
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

        if self.__chance.get(self.__CHANCE_TO_REPLY_IN_PUBLIC_CHAT):
            return False

        return True

    def __is_mandatory_reply(self, message: TelegramMessage) -> bool:
        return message.get_chat().is_private_type() or message.is_reply_to_me()

    def __is_reply_in_audio(self, message: TelegramMessage) -> bool:
        if message.get_voice() is not None:
            return True

        if self.__chance.get(self.__CHANCE_TO_REPLY_IN_AUDIO):
            return True

        return False

    def __get_random_trigger(self, message: TelegramMessage) -> Union[str, None]:
        if message.get_text() == Command.IMAGE:
            return self.__trigger.RANDOM_IMAGE_TRIGGER

        if message.get_text() == Command.VOICE:
            return self.__trigger.RANDOM_VOICE_TRIGGER

        if (
            message.get_chat().get_id() == self.__telegram_log_chat_id or
            not message.get_chat().is_group_type() or
            message.is_reply_to_me()
        ):
            return None

        if self.__chance.get(self.__CHANCE_TO_RANDOM_IMAGE):
            return self.__trigger.RANDOM_IMAGE_TRIGGER

        if self.__chance.get(self.__CHANCE_TO_RANDOM_VOICE):
            return self.__trigger.RANDOM_VOICE_TRIGGER

        if self.__chance.get(self.__CHANCE_TO_RANDOM_TEST):
            return self.__trigger.RANDOM_TEXT_TRIGGER

        return None
