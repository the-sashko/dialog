import random
from typing import Union
from logger.logger import Logger
from telegram.telegram import Telegram
from telegram.message import Message as Telegram_Message #to-do: refactor to Pascal case
from gpt.gpt import Gpt
from tts.tts import Tts
from image.image import Image
from storage.storage import Storage
from settings.settings import Settings
from chance.chance import Chance
from markov.markov import Markov
from post_processing.post_processing import PostProcessing

class Script:
    TEST_SCRIPT = 'test'
    HELLO_SCRIPT = 'hello'
    ABOUT_ME_SCRIPT = 'about_me'
    RANDOM_TEXT_SCRIPT = 'random_text'
    RANDOM_VOICE_SCRIPT = 'random_voice'
    RANDOM_IMAGE_SCRIPT = 'random_image'
    NONE_SCRIPT = 'none'

    __CHANCE_TO_PARAPHRASE_VOICE_MESSAGE = 20
    __CHANCE_TO_PARAPHRASE_TEXT_MESSAGE = 85

    __logger = None
    __telegram = None
    __gpt = None
    __tts = None
    __image = None
    __storage = None
    __chance = None
    __markov = None
    __post_processing = None

    __random_image_prompts = None
    __random_voice_prompts = None
    __random_text_prompts = None
    __random_test_prompts = None
    __random_hello_prompts = None
    __random_about_me_prompts = None

    def __init__(self):
        self.__logger = Logger()
        self.__telegram = Telegram()
        self.__gpt = Gpt()
        self.__tts = Tts()
        self.__image = Image()
        self.__storage = Storage()
        self.__chance = Chance()
        self.__markov = Markov()
        self.__post_processing = PostProcessing()

        settings = Settings()

        replies_config = settings.get_replies_config()

        self.__random_image_prompts = replies_config['random_images']
        self.__random_voice_prompts = replies_config['random_voices']
        self.__random_text_prompts = replies_config['random_texts']
        self.__random_test_prompts = replies_config['random_tests']
        self.__random_hello_prompts = replies_config['random_hello']
        self.__random_about_me_prompts = replies_config['random_about_me']

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
            random.choice(self.__random_test_prompts)
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
            random.choice(self.__random_hello_prompts)
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
            random.choice(self.__random_about_me_prompts)
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

    def __get_random_text(self) -> Union[str, None]:
        random_text = random.choice(self.__random_text_prompts)

        if random_text == 'random':
            random_text = self.__markov.get_random_text()

        if random_text is None:
            self.__logger.log_error('Random text generation failed')

        return random_text

    def __do_random_text(self, data: Union[dict, None] = None) -> None:
        if data is None or 'chat_id' not in data:
            self.__logger.log_error('Can not execute random_text script. Invalid data provided')

            return None

        reply = self.__get_random_text()

        reply = self.__post_processing.do_handle(
            reply,
            False,
            False,
            False
        )

        if reply is None:
            return None

        if self.__chance.get(self.__CHANCE_TO_PARAPHRASE_TEXT_MESSAGE):
            reply = self.__gpt.paraphrase(reply)

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

        reply = random.choice(self.__random_voice_prompts)

        if reply == 'random':
            reply = self.__get_random_text()

        if reply is None:
            return None

        reply = self.__post_processing.do_handle(
            reply,
            False,
            False,
            True
        )

        if reply is None:
            return None

        if self.__chance.get(self.__CHANCE_TO_PARAPHRASE_VOICE_MESSAGE):
            reply = self.__gpt.paraphrase(reply)

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

        random_image_promt = random.choice(self.__random_image_prompts)

        prompt = [
            {'role': 'system', 'content': 'Imagine image by user prompt. Create description of image. Response should be only description in 128 symbols'},
            {'role': 'user', 'content': random_image_promt}
        ]

        image_promt = self.__gpt.get(prompt)

        if image_promt is None:
            self.__logger.log_error(f'Can not create image description by prompt {random_image_promt}')

            return None

        reply = self.__gpt.paraphrase(
            f'Look at this photo of {prompt}'
        )

        if (
            image_promt is not None and
            'message' in data and
            isinstance(data['message'], Telegram_Message)
        ):
            message = data['message']

            self.__storage.save_message(
                message.get_user().get_id(),
                message.get_chat().get_id(),
                message.get_user().get_name(),
                message.get_chat().get_title(),
                {'role': 'assistant', 'content': reply}
            )

        image_file_path = self.__image.create_image(image_promt)

        self.__telegram.send_photo(
            data['chat_id'],
            None,
            image_file_path
        )
