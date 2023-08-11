import json

from os import getcwd, path

class Settings:
    __CONFIG_FILE_PATH = '%s/data/config/%s.json'

    __BOT_CONFIG_NAME = 'bot'
    __OPEN_AI_CONFIG_NAME = 'open_ai'
    __TELEGRAM_CONFIG_NAME = 'telegram'
    __STABLE_DIFFUSION_CONFIG_NAME = 'stable_diffusion'
    __REPLIES_CONFIG_NAME = 'replies'

    __data = {}

    def __init__(self):
        self.__set_config(self.__BOT_CONFIG_NAME)
        self.__set_config(self.__OPEN_AI_CONFIG_NAME)
        self.__set_config(self.__TELEGRAM_CONFIG_NAME)
        self.__set_config(self.__STABLE_DIFFUSION_CONFIG_NAME)
        self.__set_config(self.__REPLIES_CONFIG_NAME)

    def get_bot_config(self) -> dict:
        return self.__get_config(self.__BOT_CONFIG_NAME)

    def get_open_ai_config(self) -> dict:
        return self.__get_config(self.__OPEN_AI_CONFIG_NAME)

    def get_telegram_config(self) -> dict:
        return self.__get_config(self.__TELEGRAM_CONFIG_NAME)

    def get_stable_diffusion_config(self) -> dict:
        return self.__get_config(self.__STABLE_DIFFUSION_CONFIG_NAME)

    def get_replies_config(self) -> dict:
        return self.__get_config(self.__REPLIES_CONFIG_NAME)

    def __get_config(self, config_name: str) -> dict:
        if not config_name in self.__data:
            raise Exception(f'Config {config_name} is not exists')

        return self.__data[config_name]

    def __set_config(self, config_name: str):
        config_file_path = self.__get_config_file_path(config_name)

        if not path.exists(config_file_path) or not path.isfile(config_file_path):
            raise Exception(f'Config file {config_name} not found')

        configFile = open(config_file_path, 'r')

        self.__data[config_name] = json.loads(configFile.read())

    def __get_config_file_path(self, config_name: str) -> str:
        return self.__CONFIG_FILE_PATH % (getcwd(), config_name)
