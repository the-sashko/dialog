import json

from telegram.file import File

class Voice:
    __id = None
    __file = None
    __mime_type = False

    def __init__(self, values: dict):
        if not self.__is_values_have_valid_format(values):
            raise Exception(f'Telegram voice values have invalid format. Values: {json.dumps(values)}')

        self.__set_id(values['file_unique_id'])
        self.__set_mime_type(values['mime_type'])
        self.__set_file(values['file_id'])

    def get_id(self) -> str:
        return self.__id

    def get_mime_type(self) -> str:
        return self.__mime_type
    
    def get_file(self) -> File:
        return self.__file

    def __set_id(self, id: str) -> None:
        self.__id = id

    def __set_mime_type(self, mime_type: str) -> None:
        self.__mime_type = mime_type

    def __set_file(self, file_id: str) -> None:
        self.__file = File(file_id)

    def __is_values_have_valid_format(self, values: dict) -> bool:
        return 'file_id' in values and 'file_unique_id' in values and 'mime_type' in values
