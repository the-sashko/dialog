from typing import Union

from script.sctript import Script
from logger.logger import Logger

class Trigger:
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

        if name == Script.TEST_SCRIPT or self.__is_test(data):
            self.__script.run(Script.TEST_SCRIPT, data)

            return None

        if name == Script.HELLO_SCRIPT or self.__is_hello(data):
            self.__script.run(Script.HELLO_SCRIPT, data)

            return None

        if name == Script.ABOUT_ME_SCRIPT or self.__is_about_me(data):
            self.__script.run(Script.ABOUT_ME_SCRIPT, data)

            return None

        if name == Script.RANDOM_TEXT_SCRIPT:
            self.__script.run(Script.RANDOM_TEXT_SCRIPT, data)

            return None

        if name == Script.RANDOM_VOICE_SCRIPT:
            self.__script.run(Script.RANDOM_VOICE_SCRIPT, data)

            return None

        if name == Script.RANDOM_IMAGE_SCRIPT:
            self.__script.run(Script.RANDOM_IMAGE_SCRIPT, data)

            return None

        if name == Script.NONE_SCRIPT:
            self.__script.run(Script.NONE_SCRIPT, data)

            return None
        
        raise Exception('Unknown trigger %s' % name)

    def __is_test(
        self,
        data: Union[dict, None] = None
    ) -> bool:
        #To-Do
        return False

    def __is_hello(
        self,
        data: Union[dict, None] = None
    ) -> bool:
        #To-Do
        return False

    def __is_about_me(
        self,
        data: Union[dict, None] = None
    ) -> bool:
        #To-Do
        return False
