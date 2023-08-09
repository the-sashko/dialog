from typing import Union

from script.sctript import Script

#to-do: add logs
class Trigger:
    __script = None

    def __init__(self):
        self.__script = Script()

    def fire(
        self,
        name: str,
        data: Union[dict, None] = None
    ) -> None:
        if name == Script.TEST_SCRIPT or self.__is_test(data):
            self.__script.run(Script.TEST_SCRIPT, data)

        if name == Script.HELLO_SCRIPT or self.__is_hello(data):
            self.__script.run(Script.HELLO_SCRIPT, data)

        if name == Script.ABOUT_ME_SCRIPT or self.__is_about_me(data):
            self.__script.run(Script.ABOUT_ME_SCRIPT, data)

        if name == Script.RANDOM_TEXT_SCRIPT:
            self.__script.run(Script.RANDOM_TEXT_SCRIPT, data)

        if name == Script.RANDOM_VOICE_SCRIPT:
            self.__script.run(Script.RANDOM_VOICE_SCRIPT, data)

        if name == Script.RANDOM_IMAGE_SCRIPT:
            self.__script.run(Script.RANDOM_IMAGE_SCRIPT, data)

        if name == Script.NONE_SCRIPT:
            self.__script.run(Script.NONE_SCRIPT, data)

        return None

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
