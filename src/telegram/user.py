import json

class User:
    __id = None
    __name = None
    __is_bot = False

    def __init__(self, values: dict):
        if not self.__is_values_have_valid_format(values):
            raise Exception(f'Telegram user values have invalid format. Values: {json.dumps(values)}')

        self.__set_id(int(values['id']))
        self.__set_name(values)
        self.__set_is_bot(bool(values['is_bot']))

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def is_bot(self) -> bool:
        return self.__is_bot
    
    def set_name(self, name: str) -> None:
        self.__name = name

    def __set_id(self, id: int) -> None:
        self.__id = id

    def __set_name(self, values: dict) -> None:
        id = values['id']

        self.set_name(f'user_{id}')

        if 'username' in values:
            self.set_name(str(values['username']))

        if 'first_name' in values:
            self.set_name(str(values['first_name']))

        if 'last_name' in values:
            first_name = values['first_name']
            last_name = values['last_name']
            self.set_name(f'{first_name} {last_name}')

        if 'last_name' in values and not 'first_name' in values:
            self.set_name(str(values['last_name']))

    def __set_is_bot(self, isBot: bool) -> None:
        self.__is_bot = isBot

    def __is_values_have_valid_format(self, values: dict) -> bool:
        return 'id' in values and 'is_bot' in values
