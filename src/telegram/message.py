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

        self.__mapMessageValues(values)

        self.__transcribeVoice()

        if (self.getUpdateId() != None):
            self.__saveLastUpdateId(self.getUpdateId())

    def __mapMessageValues(self, values: dict):
        # if message index is missing but result exists (in case when it is respose after sending message)
        if 'message' not in values and 'message_id' in values:
            values = dict({'message': values})

        if not self.__isValuesHaveValidMessageFormat(values):
            raise Exception('Telegram Message Values Have Invalid Format. Values: %s' % json.dumps(values))

        self.__setId(int(values['message']['message_id']))
        self.__setDate(int(values['message']['date']))
        self.__setUser(values['message']['from'])
        self.__setChat(values['message']['chat'])

        if self.getUser().isBot() and self.getUser().getName() == 'Group':
            self.getUser().setName(self.getChat().getTitle())

        if 'text' in values['message']:
            self.__setText(str(values['message']['text']))

        if 'voice' in values['message']:
            self.__setVoice(values['message']['voice'])

        if 'reply_to_message' in values['message']:
            self.__setParent(values['message']['reply_to_message'])

        if 'update_id' in values:
            self.__setUpdateId(int(values['update_id']))

    def getId(self) -> int:
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
            return self.__parent.getUser().getId() == self.__bot_id
        except:
            return False

    @staticmethod
    def getLastUpdateId() -> int:
        lastUpdateIdFilePath = Message.__getLastUpdateIdFilePath()

        if not path.exists(lastUpdateIdFilePath) or not path.isfile(lastUpdateIdFilePath):
            return 0

        lastUpdateIdFile = open(lastUpdateIdFilePath, 'r')

        lastUpdateId = lastUpdateIdFile.read()

        lastUpdateIdFile.close()

        if lastUpdateId == '':
            return 0

        return int(lastUpdateId)

    def __saveLastUpdateId(self, lastUpdateId: int) -> None:
        lastUpdateIdFilePath = self.__getLastUpdateIdFilePath()

        lastUpdateIdFromFile = self.getLastUpdateId()

        if lastUpdateIdFromFile > lastUpdateId:
            return

        lastUpdateIdFile = open(lastUpdateIdFilePath, 'w')
        lastUpdateIdFile.write(str(lastUpdateId))
        lastUpdateIdFile.close()

    def __setId(self, id: int) -> None:
        self.__id = id

    def __setUpdateId(self, updateId: int) -> None:
        self.__update_id = updateId

    def __setText(self, text: str) -> None:
        self.__text = text

    def __setDate(self, date: int) -> None:
        self.__date = date

    def __setUser(self, values: dict) -> None:
        self.__user = User(values)

    def __setChat(self, values: dict) -> None:
        self.__chat = Chat(values)

    def __setVoice(self, values: dict) -> None:
        self.__voice = Voice(values)

    def __setParent(self, values: dict) -> None:
        self.__parent = Message(values)

    def __transcribeVoice(self) -> None:
        voice = self.getVoice()

        if voice == None:
            return None
        
        file_path = voice.getFile().getFilePath()

        if file_path == None:
            return None
        
        text = self.__transcription.transcribe(file_path)

        if text == None:
            return None

        self.__setText(text)

    def __isValuesHaveValidMessageFormat(self, values: dict) -> bool:
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
    def __getLastUpdateIdFilePath() -> str:
        return Message.__LAST_UPDATE_ID_FILE_PATH % getcwd()
