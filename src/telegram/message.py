import json

from os import getcwd, path
from typing import Union

from telegram.user import User
from telegram.chat import Chat
from telegram.voice import Voice

from settings.settings import Settings

from transcription.transcription import Transcription

#to-do: refactoring code syle
#to-do: add logs
class Message:
    __LAST_UPDATE_ID_FILE_PATH = '%s/data/telegram_last_update_id.txt'

    __id = None
    __update_id = None
    __text = None
    __voice = None
    __date = None
    __user = None
    __chat = None
    __parent = None

    __transcription = None

    __bot_id = None

    def __init__(self, values: dict):
        self.__transcription = Transcription()

        telegram_config = Settings().get_telegram_config()

        self.__bot_id = telegram_config['bot_id']

        self.__map_message_values(values)

        self.__transcribe_voice()

        if (self.getUpdateId() != None):
            self.__save_last_update_id(self.getUpdateId())

    def __map_message_values(self, values: dict):
        # if message index is missing but result exists (in case when it is respose after sending message)
        if 'message' not in values and 'message_id' in values:
            values = dict({'message': values})

        if not self.__is_values_have_valid_message_format(values):
            raise Exception('Telegram message values have invalid format. Values: %s' % json.dumps(values))

        self.__set_id(int(values['message']['message_id']))
        self.__set_date(int(values['message']['date']))
        self.__set_user(values['message']['from'])
        self.__set_chat(values['message']['chat'])

        if self.getUser().isBot() and self.getUser().getName() == 'Group':
            self.getUser().setName(self.getChat().getTitle())

        if 'text' in values['message']:
            self.__set_text(str(values['message']['text']))

        if 'voice' in values['message']:
            self.__set_voice(values['message']['voice'])

        if 'reply_to_message' in values['message']:
            self.__set_parent(values['message']['reply_to_message'])

        if 'update_id' in values:
            self.__set_update_id(int(values['update_id']))

    def get_id(self) -> int:
        return self.__id

    def getUpdateId(self) -> Union[int, None]:
        return self.__update_id

    def getText(self) -> Union[str, None]:
        return self.__text

    def getDate(self) -> int:
        return self.__date

    def getUser(self) -> User:
        return self.__user

    def getChat(self) -> Chat:
        return self.__chat

    def getVoice(self) -> Union[None, Voice]:
        return self.__voice

    def getParent(self) -> Union[None, any]:#TO-DO: change any
        return self.__parent

    def isReplyToMe(self) -> bool:
        if self.__parent is None:
            return False

        try:
            return self.__parent.getUser().get_id() == self.__bot_id
        except:
            return False

    @staticmethod
    def getLastUpdateId() -> int:
        lastUpdateIdFilePath = Message.__get_last_update_id_file_path()

        if not path.exists(lastUpdateIdFilePath) or not path.isfile(lastUpdateIdFilePath):
            return 0

        lastUpdateIdFile = open(lastUpdateIdFilePath, 'r')

        lastUpdateId = lastUpdateIdFile.read()

        lastUpdateIdFile.close()

        if lastUpdateId == '':
            return 0

        return int(lastUpdateId)

    def __save_last_update_id(self, last_update_id: int) -> None:
        last_update_id_file_path = self.__get_last_update_id_file_path()

        last_update_id_from_file = self.getLastUpdateId()

        if last_update_id_from_file > last_update_id:
            return None

        lastUpdateIdFile = open(last_update_id_file_path, 'w')
        lastUpdateIdFile.write(str(last_update_id))
        lastUpdateIdFile.close()

    def __set_id(self, id: int) -> None:
        self.__id = id

    def __set_update_id(self, update_id: int) -> None:
        self.__update_id = update_id

    def __set_text(self, text: str) -> None:
        self.__text = text

    def __set_date(self, date: int) -> None:
        self.__date = date

    def __set_user(self, values: dict) -> None:
        self.__user = User(values)

    def __set_chat(self, values: dict) -> None:
        self.__chat = Chat(values)

    def __set_voice(self, values: dict) -> None:
        self.__voice = Voice(values)

    def __set_parent(self, values: dict) -> None:
        self.__parent = Message(values)

    def __transcribe_voice(self) -> None:
        voice = self.getVoice()

        if voice == None:
            return None
        
        file_path = voice.getFile().getFilePath()

        if file_path == None:
            return None
        
        text = self.__transcription.transcribe(file_path)

        if text == None:
            return None

        self.__set_text(text)

    def __is_values_have_valid_message_format(self, values: dict) -> bool:
        return (
            'message' in values and
            type(values['message']) == dict and
            'message_id' in values['message'] and
            'date' in values['message'] and
            'from' in values['message'] and
            'chat' in values['message'] and
            type(values['message']['from']) == dict and
            type(values['message']['chat']) == dict
        )

    @staticmethod
    def __get_last_update_id_file_path() -> str:
        return Message.__LAST_UPDATE_ID_FILE_PATH % getcwd()
