from typing import Union

class Command:
    VOICE = '[voice]'
    IMAGE = '[image]'
    ASCII = '[ascii]'
    SAY = '[say]'
    SAY_ALL = '[say_all]'
    VERSION = '[version]'

    __type = None

    __value = None

    def __init__(self, commant_type: Union[str, None], value: Union[str, None]):
        self.__type = commant_type #to-do: add validation
        self.__value = value 

    def get_type(self) -> Union[str, None]:
        return self.__type

    def get_value(self) -> Union[str, None]:
        return self.__value
