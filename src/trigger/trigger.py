from typing import Union

from script.script import Script
from logger.logger import Logger

class Trigger:
    TEST_TRIGGER = 'test'
    HELLO_TRIGGER = 'hello'
    ABOUT_ME_TRIGGER = 'about_me'
    RANDOM_TEXT_TRIGGER = 'random_text'
    RANDOM_VOICE_TRIGGER = 'random_voice'
    RANDOM_IMAGE_TRIGGER = 'random_image'
    NONE_TRIGGER = 'none'

    __script = None
    __logger = None

    def __init__(self):
        self.__script = Script()
        self.__logger = Logger()

    def fire(
        self,
        name: Union[str, None],
        data: Union[dict, None] = None
    ) -> None:
        if name is not None:
            self.__logger.log(
                'Fired %s trigger' % name
            )

        if name == self.TEST_TRIGGER:
            self.__script.run(Script.TEST_SCRIPT, data)

            return None

        if name == self.HELLO_TRIGGER:
            self.__script.run(Script.HELLO_SCRIPT, data)

            return None

        if name == self.ABOUT_ME_TRIGGER:
            self.__script.run(Script.ABOUT_ME_SCRIPT, data)

            return None

        if name == self.RANDOM_TEXT_TRIGGER:
            self.__script.run(Script.RANDOM_TEXT_SCRIPT, data)

            return None

        if name == self.RANDOM_VOICE_TRIGGER:
            self.__script.run(Script.RANDOM_VOICE_SCRIPT, data)

            return None

        if name == self.RANDOM_IMAGE_TRIGGER:
            self.__script.run(Script.RANDOM_IMAGE_SCRIPT, data)

            return None

        if name == self.NONE_TRIGGER:
            self.__script.run(Script.NONE_SCRIPT, data)

            return None
        
        raise Exception('Unknown trigger %s' % name)
