import json

#to-do: refactoring code syle
#to-do: add logs
class User:
    __id = None
    __name = None
    __is_bot = False

    def __init__(self, values: dict):
        if not self.__isValuesHaveValidFormat(values):
            raise Exception('Telegram User Values Have Invalid Format. Values: %s' % json.dumps(values))

        self.__setId(int(values['id']))
        self.__setName(values)
        self.__setIsBot(bool(values['is_bot']))

    def get_id(self) -> int:
        return self.__id

    def getName(self) -> str:
        return self.__name

    def isBot(self) -> bool:
        return self.__is_bot
    
    def setName(self, name: str) -> None:
        self.__name = name

    def __setId(self, id: int) -> None:
        self.__id = id

    def __setName(self, values: dict) -> None:
        self.setName('user_%d' % int(values['id']))

        if 'username' in values:
            self.setName(str(values['username']))

        if 'first_name' in values:
            self.setName(str(values['first_name']))

        if 'last_name' in values:
            self.setName('%s %s' % (str(values['first_name']), str(values['last_name'])))

        if 'last_name' in values and not 'first_name' in values:
            self.setName(str(values['last_name']))

    def __setIsBot(self, isBot: bool) -> None:
        self.__is_bot = isBot

    def __isValuesHaveValidFormat(self, values: dict) -> bool:
        return 'id' in values and 'is_bot' in values
