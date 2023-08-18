import json
from typing import Union
import requests
from telegram.message import Message
from settings.settings import Settings

#to-do: add logs
class Telegram:
    __HTTP_STATUS_OK = 200

    __GET_MESSAGES_LIMIT = 100

    __GET_MESSAGES_URL = 'https://api.telegram.org/bot%s/getUpdates?offset=%d&limit=%d&allowed_updates=["message"]'
    __SEND_MESSAGE_URL = 'https://api.telegram.org/bot%s/sendMessage?%schat_id=%s&text=%s%s'
    __SEND_PHOTO_URL = 'https://api.telegram.org/bot%s/sendPhoto?parse_mode=markdown%s'
    __SEND_VOICE_URL = 'https://api.telegram.org/bot%s/sendVoice?parse_mode=markdown%s'

    __log_chat_id = None
    __admin_chat_id = None
    __token     = None

    def __init__(self):
        config = Settings().get_telegram_config()

        self.__token     = config['bot_token']
        self.__log_chat_id = config['log_chat_id']
        self.__admin_chat_id = config['admin_chat_id']

    def send_message(
        self,
        message: str,
        chat_id: int,
        replay_to_message_id: Union[str, None] = None,
        is_markdown: bool = False
    ) -> bool:
        return self.__send(
            chat_id,
            message,
            replay_to_message_id,
            is_markdown
        )

    def send_message_to_log_chat(self, message: str) -> bool:
        return self.__send(self.__log_chat_id, message)

    def send_message_to_admin_chat(self, message: str) -> bool:
        return self.__send(self.__admin_chat_id, message)

    def get_messages(self) -> list:
        response_rows = self.__get()

        if response_rows is None :
            return []

        messages = list(map(lambda response_row : Message(response_row), response_rows))

        return messages

    def send_photo(
        self,
        chat_id: str,
        caption: Union[str, None],
        file_path: str,
        replay_to_message_id: Union[int, None] = None
    ) -> Union[Message, None]:
        data = {'chat_id': chat_id}

        if caption is not None:
            data = {'chat_id': chat_id, 'caption': caption}

        replay_to_message_id_param = ''

        if replay_to_message_id is not None:
            replay_to_message_id_param = f'&reply_to_message_id={replay_to_message_id}'

        url = self.__SEND_PHOTO_URL % (self.__token, replay_to_message_id_param)

        with open(file_path, 'rb', -1, 'utf-8') as image_file:
            response = requests.post(url, data=data, files={'photo': image_file})

        if response.status_code != self.__HTTP_STATUS_OK:
            return None

        response = json.loads(response.content)

        if not self.__is_response_has_valid_format(response) :
            raise Exception(f'Telegram respose has invalid format. Respose: {json.dumps(response)}')

        response = response['result']

        if len(response) > 0 :
            return Message(response)

        return None

    def send_voice(
        self,
        chat_id: str,
        file_path: str,
        replay_to_message_id: Union[int, None] = None
    ) -> Union[Message, None]:
        data = {'chat_id': chat_id}

        replay_to_message_id_param = ''

        if replay_to_message_id is not None:
            replay_to_message_id_param = f'&reply_to_message_id={replay_to_message_id}'

        url = self.__SEND_VOICE_URL % (self.__token, replay_to_message_id_param)

        with open(file_path, 'rb', -1, 'utf-8') as voice_file:
            response = requests.post(url, data=data, files={'voice': voice_file})

        if response.status_code != self.__HTTP_STATUS_OK:
            return None

        response = json.loads(response.content)

        if not self.__is_response_has_valid_format(response) :
            raise Exception(f'Telegram respose has invalid format. Respose: {json.dumps(response)}')

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

        if not self.__is_response_has_valid_format(response) :
            raise Exception(f'Telegram respose has invalid format. Respose: {json.dumps(response)}')

        response = response['result']

        if len(response) > 0 :
            return response

        return None

    def __send(
        self,
        chat_id: str,
        message: str,
        replay_to_message_id: Union[str, None] = None,
        is_markdown: bool = False
    ) -> Union[Message, None]:
        markdown_url_param = ''
        replay_to_message_id_param = ''

        if is_markdown:
            markdown_url_param = 'parse_mode=markdown&'

        if replay_to_message_id is not None:
            replay_to_message_id_param = f'&reply_to_message_id={replay_to_message_id}'

        url = self.__SEND_MESSAGE_URL % (self.__token, markdown_url_param, chat_id, message, replay_to_message_id_param)

        response = requests.get(url)

        if response.status_code != self.__HTTP_STATUS_OK :
            return None

        response = json.loads(response.content)

        if not self.__is_response_has_valid_format(response) :
            raise Exception(f'Telegram respose has invalid format. Respose: {json.dumps(response)}')

        response = response['result']

        if len(response) > 0 :
            return Message(response)

        return None

    def __is_response_has_valid_format(self, response: dict) -> bool:
        return (
            'ok' in response and
            'result' in response and
            isinstance(response['result'], (dict, list))
        )
