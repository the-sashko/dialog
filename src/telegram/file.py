import json
from typing import Union
from os import getcwd, path, remove
import requests
from settings.settings import Settings

#to-do: add logs
class File:
    __HTTP_STATUS_OK = 200

    __GET_FILE_URL = 'https://api.telegram.org/bot%s/getFile?file_id=%s'
    __DOWNLOAD_FILE_URL = 'https://api.telegram.org/file/bot%s/%s'

    __FILE_PATH = '%s/data/download/%s'

    __file_path = None

    __token = None

    def __init__(self, file_id: str):
        config = Settings().get_telegram_config()

        self.__token = config['bot_token']

        file = self.__get_file(file_id)

        if file is not None and 'file_path' in file:
            self.__download_file(file['file_path'])

    def get_file_path(self) -> Union[str, None]:
        return self.__file_path

    def __download_file(self, remote_file_path: str) -> None:
        url = self.__DOWNLOAD_FILE_URL % (self.__token, remote_file_path)

        response = requests.get(url)

        file_name = url.split('/')[-1]

        self.__file_path = self.__FILE_PATH % (getcwd(), file_name)

        if path.isfile(self.__file_path):
            remove(self.__file_path)

        if response.status_code != self.__HTTP_STATUS_OK:
            return None

        with open(self.__file_path, 'wb', -1, 'utf-8') as buffer_writer:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    buffer_writer.write(chunk)

        return None

    def __get_file(self, file_id: str) -> Union[dict, None]:
        url = self.__GET_FILE_URL % (self.__token, file_id)

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

    def __is_response_has_valid_format(self, response: dict) -> bool:
        return (
            'ok' in response and
            'result' in response and
            isinstance(response['result'], dict)
        )
