import json
from settings.settings import Settings

class Chat:
    __TYPE_PRIVATE = 'private'
    __TYPE_GROUP = 'group'
    __TYPE_UNSUPPORTED = 'unsupported'

    __REMOTE_TYPE_PRIVATE = 'private'
    __REMOTE_TYPE_GROUP = 'supergroup'

    __id = None
    __title = None
    __type = __TYPE_UNSUPPORTED

    __admin_chat_id = None
    __main_chat_id = None

    def __init__(self, values: dict):
        if not self.__is_values_have_valid_format(values):
            raise Exception(f'Telegram chat values have invalid Format. Values: {json.dumps(values)}')

        self.__set_id(int(values['id']))
        self.__set_title(values)
        self.__set_type(str(values['type']))

        telegram_config = Settings().get_telegram_config()

        self.__admin_chat_id = telegram_config['admin_chat_id']
        self.__main_chat_id = telegram_config['main_chat_id']

    def get_id(self) -> int:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_type(self) -> str:
        return self.__type

    def is_private_type(self) -> str:
        return self.__type == self.__TYPE_PRIVATE

    def is_group_type(self) -> str:
        return self.__type == self.__TYPE_GROUP

    def is_supported(self) -> bool:
        return self.__type != self.__TYPE_UNSUPPORTED

    def is_admin_chat(self) -> bool:
        return self.__admin_chat_id == self.__id

    def is_main_chat(self) -> bool:
        return self.__main_chat_id == self.__id

    def __set_id(self, id: int) -> None:
        self.__id = id

    def __set_title(self, values: dict) -> None:
        id = values['id']

        self.__title = f'chat_{id}'

        if 'title' in values:
            self.__title = str(values['title'])

    def __set_type(self, type: str) -> None:
        if type == self.__REMOTE_TYPE_PRIVATE:
            self.__type = self.__TYPE_PRIVATE

        if type == self.__REMOTE_TYPE_GROUP:
            self.__type = self.__TYPE_GROUP

    def __is_values_have_valid_format(self, values: dict) -> bool:
        return 'id' in values and 'type' in values
