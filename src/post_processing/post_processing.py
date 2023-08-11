#!/usr/bin/python3

import re
import random
from typing import Union
from markov.markov import Markov
from gpt.gpt import Gpt
from settings.settings import Settings
from chance.chance import Chance
from logger.logger import Logger

#to-do: refactoring code syle
#to-do: add logs
class Post_Processing:
    __CHANCE_TO_SMILE_FILTER = 5

    __markov = None
    __gpt = None
    __chance = None
    __logger = None

    __general_reject = None
    __rejects = None
    __audio_rejects = None

    def __init__(self) -> None:
        self.__markov = Markov()
        self.__gpt = Gpt()
        self.__chance = Chance()
        self.__logger = Logger()

        replies_config = Settings().get_replies_config()

        self.__general_reject = replies_config['general_reject']
        self.__rejects = replies_config['rejects']
        self.__audio_rejects = replies_config['audio_rejects']

    def do_handle(
        self,
        text: Union[str, None],
        is_mandatory_return: bool,
        is_voice: bool = False,
        is_reply_audio: bool = False
    ) -> Union[str, None]:
        if self.__is_reject(text):
            text = None

        if text is None and not is_mandatory_return:
            return None

        if text is None and is_mandatory_return:
            text = self.__get_reject(is_voice, True)

        if text is None and is_mandatory_return:
            text = self.__get_reject(is_voice, False)

        if text is None and is_mandatory_return:
            text = self.__markov.get_random_text()

        if text is None and is_mandatory_return:
            text = self.__general_reject

        text_with_post_filters = self.__post_filters(
            text,
            is_reply_audio
        )

        if text_with_post_filters is not None:
            text = text_with_post_filters

        return text

    def __is_reject(self, text: Union[str, None]) -> bool:
        if text is None:
            return True

        text = text.lower()

        text = re.sub(r'\s+', r' ', text)
        text = re.sub(r'((^\s+)|(\s+$))', r'', text)

        #To-Do: move reject patterns to config

        pattern = r'^(.*?)не можу(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            return True

        pattern = r'^(.*?)не проти(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            return True

        pattern = r'^(.*?)не категорично(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            return True

        pattern = r'^(.*?)дискримінац(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            return True
        
        pattern = r'^(.*?)не підтримую(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            return True

        return False

    def __get_reject(
        self,
        is_voice: bool,
        is_modify: bool
    ) -> Union[str, None]:
        reject = None

        try:
            if is_voice:
                reject = random.choice(self.__audio_rejects)

            if not is_voice:
                reject = random.choice(self.__rejects)

            if reject is not None and is_modify:
                reject = self.__gpt.paraphrase(reject)
        except Exception as exp:
            self.__logger.log_error(exp)

            reject = None

        if reject is None:
            return None

        if not is_modify:
            return reject

        if self.__is_reject(reject):
            return None

        return reject

    def __post_filters(
        self,
        text: Union[str, None],
        is_reply_audio: bool = False
    ) -> Union[str, None]:
        if text is None:
            return None

        text = self.__smile_post_filter(text, is_reply_audio)

        if self.__is_reject(text):
            return None

        return text

    def __smile_post_filter(
        self,
        text: Union[str, None],
        is_reply_audio: bool = False
    ) -> Union[str, None]:
        if is_reply_audio:
            return text

        if text is None:
            return None

        if not self.__chance.get(self.__CHANCE_TO_SMILE_FILTER):
            return text

        prompt = [
            {'role': 'system', 'content': 'Replace 10% words in text to emoji'},
            {'role': 'user', 'content': text}
        ]

        return self.__gpt.get(prompt)

    def __misspelling_post_filter(
        self,
        text: Union[str, None],
        is_reply_audio: bool = False
    ) -> Union[str, None]:
        if is_reply_audio:
            return text

        if text is None:
            return None

        prompt = [
            {'role': 'system', 'content': 'Fix all misspellings in text'},
            {'role': 'user', 'content': text}
        ]

        return self.__gpt.get(prompt)
 