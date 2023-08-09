import requests
import json

from telegram.message import Message
from typing import Union
from settings.settings import Settings

#to-do: refactoring code syle
#to-do: add logs
class Telegram:
    __HTTP_STATUS_OK = 200

    __GET_MESSAGES_LIMIT = 100

    __GET_MESSAGES_URL = 'https://api.telegram.org/bot%s/getUpdates?offset=%d&limit=%d&allowed_updates=["message"]'
    __SEND_MESSAGE_URL = 'https://api.telegram.org/bot%s/sendMessage?%schat_id=%s&text=%s%s'
    __SEND_PHOTO_URL = 'https://api.telegram.org/bot%s/sendPhoto?parse_mode=markdown%s'    
    __SEND_VOICE_URL = 'https://api.telegram.org/bot%s/sendVoice?parse_mode=markdown%s'

    __logChatId = None
    __adminChatId = None
    __token     = None

    def __init__(self):
        config = Settings().get_telegram_config()

        self.__token     = config['bot_token']
        self.__logChatId = config['log_chat_id']
        self.__adminChatId = config['log_chat_id']

    def sendMessage(self, message: str, chatId: int, replayToMessageId: Union[str, None] = None, isMarkdown: bool = False) -> bool:
        return self.__send(chatId, message, replayToMessageId, isMarkdown)

    def sendMessageToLogChat(self, message: str) -> bool:
        return self.__send(self.__logChatId, message)

    def sendMessageToAdminChat(self, message: str) -> bool:
        return self.__send(self.__logChatId, message)

    def getMessages(self) -> list:
        responseRows = self.__get()

        if responseRows == None :
            return list()

        messages = list(map(lambda responseRow : Message(responseRow), responseRows))

        return messages

    def sendPhoto(self, idChat: str, caption: Union[str, None], filePath: str, replayToMessageId: Union[int, None] = None) -> Union[Message, None]:
        data = {"chat_id": idChat}

        if caption != None:
            data = {"chat_id": idChat, "caption": caption}

        replayToMessageIdParam = ''

        if replayToMessageId != None:
            replayToMessageIdParam = '&reply_to_message_id=%s' % replayToMessageId
        
        url = self.__SEND_PHOTO_URL % (self.__token, replayToMessageIdParam)

        with open(filePath, "rb") as image_file:
            response = requests.post(url, data=data, files={"photo": image_file})

        if response.status_code != self.__HTTP_STATUS_OK:
            return None

        response = json.loads(response.content)

        if not self.__isResponseHaveValidFormat(response) :
            raise Exception('Telegram Respose Has Invalid Forrmat. Respose: %s' % json.dumps(response))

        response = response['result']

        if len(response) > 0 :
            return Message(response)

        return None
    
    def sendVoice(self, idChat: str, filePath: str, replayToMessageId: Union[int, None] = None) -> Union[Message, None]:
        data = {"chat_id": idChat}

        replayToMessageIdParam = ''

        if replayToMessageId != None:
            replayToMessageIdParam = '&reply_to_message_id=%s' % replayToMessageId
        
        url = self.__SEND_VOICE_URL % (self.__token, replayToMessageIdParam)

        with open(filePath, "rb") as voice_file:
            response = requests.post(url, data=data, files={"voice": voice_file})

        if response.status_code != self.__HTTP_STATUS_OK:
            return None

        response = json.loads(response.content)

        if not self.__isResponseHaveValidFormat(response) :
            raise Exception('Telegram Respose Has Invalid Forrmat. Respose: %s' % json.dumps(response))

        response = response['result']

        if len(response) > 0 :
            return Message(response)

        return None

    def __get(self) -> Union[list, None]:
        url = self.__GET_MESSAGES_URL % (self.__token, Message.get_last_update_id() + 1, self.__GET_MESSAGES_LIMIT)

        response = requests.get(url)

        if response.status_code != self.__HTTP_STATUS_OK :
            return None

        response = json.loads(response.content)

        if not self.__isResponseHaveValidFormat(response) :
            raise Exception('Telegram Respose Has Invalid Forrmat. Respose: %s' % json.dumps(response))

        response = response['result']

        if len(response) > 0 :
            return response

        return None

    def __send(self, idChat: str, message: str, replayToMessageId: Union[str, None] = None, isMarkdown: bool = False) -> Union[Message, None]:
        markdownUrlParam = ''
        replayToMessageIdParam = ''

        if isMarkdown:
            markdownUrlParam = 'parse_mode=markdown&'

        if replayToMessageId != None:
            replayToMessageIdParam = '&reply_to_message_id=%s' % replayToMessageId

        url = self.__SEND_MESSAGE_URL % (self.__token, markdownUrlParam, idChat, message, replayToMessageIdParam)

        response = requests.get(url)

        if response.status_code != self.__HTTP_STATUS_OK :
            return None

        response = json.loads(response.content)

        if not self.__isResponseHaveValidFormat(response) :
            raise Exception('Telegram Respose Has Invalid Forrmat. Respose: %s' % json.dumps(response))

        response = response['result']

        if len(response) > 0 :
            return Message(response)

        return None

    def __isResponseHaveValidFormat(self, response: dict) -> bool:
        return (
            'ok' in response and
            'result' in response and
            (
                type(response['result']) == list or
                type(response['result']) == dict
            )
        )
