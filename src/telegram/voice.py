import json

from telegram.file import File

#to-do: refactoring code syle
#to-do: add logs
class Voice:
    __id = None
    __file = None
    __mime_type = False

    def __init__(self, values: dict):
        if not self.__isValuesHaveValidFormat(values):
            raise Exception('Telegram Voice Values Have Invalid Format. Values: %s' % json.dumps(values))

        self.__setId(values['file_unique_id'])
        self.__setMimeType(values['mime_type'])
        self.__setFile(values['file_id'])

    def get_id(self) -> str:
        return self.__id

    def getMimeType(self) -> str:
        return self.__mime_type
    
    def getFile(self) -> File:
        return self.__file

    def __setId(self, id: str) -> None:
        self.__id = id

    def __setMimeType(self, mime_type: str) -> None:
        self.__mime_type = mime_type

    def __setFile(self, file_id: str) -> None:
        self.__file = File(file_id)

    def __isValuesHaveValidFormat(self, values: dict) -> bool:
        return 'file_id' in values and 'file_unique_id' in values and 'mime_type' in values
