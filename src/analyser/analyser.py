import re
from typing import Union
from command.command import Command
from command.parser import Parser
from gpt.gpt import Gpt
from telegram.message import Message as Telegram_Message
from logger.logger import Logger
from trigger.trigger import Trigger

class Analyser:
    __parser = None
    __gpt = None
    __logger = None

    def __init__(self):
        self.__parser = Parser()
        self.__gpt = Gpt()
        self.__logger = Logger()

    def get_command(self, message: Telegram_Message) -> Union[Command, None]:
        command = self.__parser.get_command_from_text(message.get_text())

        if command is not None:
            return command

        self.__logger.log('Check voice command')
        if (self.__is_voice_command(message)):
            type = Command.VOICE
            value = self.__retrieve_voice_command_value(message)

            return Command(type, value)

        self.__logger.log('Check image command')
        if (self.__is_image_command(message)):
            type = Command.IMAGE
            value = self.__retrieve_image_command_value(message)

            return Command(type, value)

        return None

    def get_mood(self, text: str) -> str:
        mood = self.__retrieve_mood_from_text(text)

        if mood is None:
            return 'neutral'

        #TO-DO: refactoring
        if mood == 'offensive':
            return 'angry'

        if mood == 'inappropriate':
            return 'angry'

        return mood

    def get_trigger(self, message: Telegram_Message) -> Union[str, None]:
        if message.get_text().lower() == 'test':
            return Trigger.TEST_TRIGGER

    def __is_voice_command(self, message: Telegram_Message) -> bool:
        return self.__is_command('say something', message)

    def __is_image_command(self, message: Telegram_Message) -> bool:
        return self.__is_command('draw somethig', message)

    def __is_command(self, command_prompt: str, message: Telegram_Message) -> bool:
        prompt = [
            {'role': 'system', 'content': 'You are a text parser'}
        ]

        prompt.append({'role': 'system', 'content': 'Analyse is user ask for %s. Result should be just true or false' % command_prompt})
        prompt.append({'role': 'user', 'content': message.get_text()})

        response = self.__gpt.get(
            prompt,
            self.__gpt.GPT_3_MODEL
        )

        if response is None:
            return None

        return response.lower().strip() == 'true'

    def __retrieve_voice_command_value(self, message: Telegram_Message) -> Union[str, None]:
        return False # fix 'User asked to say ...'

        prompt = [
            {'role': 'system', 'content': 'You are a text parser'}
        ]

        #To-Do: fix analyze with context

        prompt.append({'role': 'user', 'content': message.get_text()})
        prompt.append({'role': 'system', 'content': 'Analyse what user asked to say. Result should be just subject of ask'})

        response = self.__gpt.get(
            prompt,
            self.__gpt.GPT_3_MODEL
        )

        if response is None:
            return None

        response = re.sub(r'\s+', r' ', response)
        response = re.sub(r'((^\s+)|(\s+$))', r'', response)

        if response == '':
            return None

        return response

    def __retrieve_image_command_value(self, message: Telegram_Message) -> Union[str, None]:
        prompt = [
            {'role': 'system', 'content': 'You are a text parser'}
        ]

        #To-Do: add context to analyze
 
        prompt.append({'role': 'user', 'content': message.get_text()})
        prompt.append({'role': 'system', 'content': 'Analyse what user asked to draw. Result should be just subject of ask in English'})

        response = self.__gpt.get(
            prompt,
            self.__gpt.GPT_3_MODEL
        )

        if prompt is None:
            return None

        response = response.lower()
        response = re.sub(r'([^a-z]+)', r' ', response)
        response = re.sub(r'\s+', r' ', response)
        response = re.sub(r'((^\s+)|(\s+$))', r'', response)
        response = response.replace('draw a', '')
        response = response.replace('draw', '')
        response = re.sub(r'\s+', r' ', response)
        response = re.sub(r'((^\s+)|(\s+$))', r'', response)

        if response == '':
            return None

        return response

    def __retrieve_mood_from_text(self, text: str) -> Union[str, None]:
        prompt = [
            {'role': 'system', 'content': 'You are a text analyser'},
            {'role': 'system', 'content': 'Analyse what mood of this test. Result should be only one world in English'},
            {'role': 'user', 'content': text}
        ]

        response = self.__gpt.get(
            prompt,
            self.__gpt.GPT_3_MODEL
        )

        if response is None:
            return None

        response = response.lower()
        response = re.sub(r'([^a-z]+)', r'', response)
        response = re.sub(r'\s+', r'', response)

        if response == '':
            return None

        return response
