from typing import Union
from logger.logger import Logger
from telegram.telegram import Telegram
from telegram.message import Message as Telegram_Message
from gpt.gpt import Gpt
from tts.tts import Tts
from image.image import Image
from storage.storage import Storage

class Script:
    TEST_SCRIPT = 'test'
    HELLO_SCRIPT = 'hello'
    ABOUT_ME_SCRIPT = 'about_me'
    RANDOM_TEXT_SCRIPT = 'random_text'
    RANDOM_VOICE_SCRIPT = 'random_voice'
    RANDOM_IMAGE_SCRIPT = 'random_image'
    NONE_SCRIPT = 'none'

    __logger = None
    __telegram = None
    __gpt = None
    __tts = None
    __image = None
    __storage = None

    def __init__(self):
        self.__logger = Logger()
        self.__telegram = Telegram()
        self.__gpt = Gpt()
        self.__tts = Tts()
        self.__image = Image()
        self.__storage = Storage()

    def run(
        self,
        name: str,
        data: Union[dict, None] = None
    ) -> None:
        self.__logger.log(f'Running {name} script')

        if name == self.TEST_SCRIPT:
            self.__do_test(data)

            return None

        if name == self.HELLO_SCRIPT:
            self.__do_hello(data)

            return None

        if name == self.ABOUT_ME_SCRIPT:
            self.__do_about_me(data)

            return None

        if name == self.RANDOM_TEXT_SCRIPT:
            self.__do_random_text(data)

            return None

        if name == self.RANDOM_VOICE_SCRIPT:
            self.__do_random_voice(data)

            return None

        if name == self.RANDOM_IMAGE_SCRIPT:
            self.__do_random_image(data)

            return None

        if name == self.NONE_SCRIPT:
            self.__do_none(data)

            return None

        raise Exception(f'Unknown script {name}')

    def __do_none(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data or 'reply_to_message_id' not in data:
            self.__logger.log_error('Can not execute none script. Invalid data provided')

            return None

        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': 'None'}
            )

        self.__telegram.send_message(
            'None',
            data['chat_id'],
            data['reply_to_message_id']
        )

    def __do_test(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data or 'reply_to_message_id' not in data:
            self.__logger.log_error('Can not execute test script. Invalid data provided')

            return None

        reply = self.__gpt.paraphrase(
            'Анус собі протестуй. Пес, блядь'#To-Do: to config
        )

        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        self.__telegram.send_message(
            reply,
            data['chat_id'],
            data['reply_to_message_id']
        )

    def __do_hello(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data or 'reply_to_message_id' not in data:
            self.__logger.log_error('Can not execute hello script. Invalid data provided')

            return None

        reply = self.__gpt.paraphrase(
            'Привіт, мудило. Давно не бачилися'#To-Do: to config
        )

        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        self.__telegram.send_message(
            reply,
            data['chat_id'],
            data['reply_to_message_id']
        )

    def __do_about_me(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data or 'reply_to_message_id' not in data:
            self.__logger.log_error('Can not execute about_me script. Invalid data provided')

            return None

        reply = self.__gpt.paraphrase(
            'Хто я? Я коханець твоєї мамки!'#To-Do: to config
        )

        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        self.__telegram.send_message(
            reply,
            data['chat_id'],
            data['reply_to_message_id']
        )

    def __do_random_text(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data:
            self.__logger.log_error('Can not execute random_text script. Invalid data provided')

            return None

        reply = self.__gpt.paraphrase(
            'Агов, як справи, сучки!'#To-Do: implement random
        )

        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        self.__telegram.send_message(
            reply,
            data['chat_id']
        )

    def __do_random_voice(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data:
            self.__logger.log_error('Can not execute random_voice script. Invalid data provided')

            return None

        #reply = self.__gpt.paraphrase(
        reply = 'Увага! Повітряна тривога! Летить пакет із гівноом! Пройдіть в найближче укриття! Увага! Повітряна тривога! Летить пакет із гівноом!'#To-Do: implement random
        #)
        reply = 'Путін - gun done'#To-Do: implement random


        if 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        voice_file_path = self.__tts.text2audio(reply)

        self.__telegram.send_voice(
            data['chat_id'],
            voice_file_path
        )

    def __do_random_image(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data:
            self.__logger.log_error('Can not execute random_image script. Invalid data provided')

            return None
        
        random_image_promt = 'funny meme'#To-Do: implement random

        prompt = [
            {'role': 'system', 'content': 'Imagine image by user prompt. Create description of image. Response should be only description in 128 symbols'},
            {'role': 'user', 'content': random_image_promt}
        ]

        image_promt = self.__gpt.get(prompt)

        if image_promt is None:
            self.__logger.log_error(f'Can not create image description by prompt {random_image_promt}')

            return None

        reply = self.__gpt.paraphrase(
            f'photo of {prompt}'
        )

        if image_promt is not None and 'message' in data and type(data['message']) == Telegram_Message:
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': f'Дивись: {reply}'}
            )

        image_file_path = self.__image.create_image(image_promt)

        self.__telegram.send_photo(
            data['chat_id'],
            None,
            image_file_path
        )
