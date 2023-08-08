import json

from os import getcwd, path

#to-do: refactoring code syle
#to-do: add logs
class Settings:
    __CONFIG_FILE_PATH = '%s/data/config/%s.json'

    __MAIN_CONFIG_NAME = 'main'
    __BOT_CONFIG_NAME = 'bot'
    __OPEN_AI_CONFIG_NAME = 'open_ai'
    __TELEGRAM_CONFIG_NAME = 'telegram'
    __STABLE_DIFFUSION_CONFIG_NAME = 'stable_diffusion'

    __data = {}

    def __init__(self):
        self.__setConfig(self.__MAIN_CONFIG_NAME)
        self.__setConfig(self.__BOT_CONFIG_NAME)
        self.__setConfig(self.__OPEN_AI_CONFIG_NAME)
        self.__setConfig(self.__TELEGRAM_CONFIG_NAME)
        self.__setConfig(self.__STABLE_DIFFUSION_CONFIG_NAME)

    def getMainConfig(self) -> dict:
        return self.__getConfig(self.__MAIN_CONFIG_NAME)

    def getBotConfig(self) -> dict:
        return self.__getConfig(self.__BOT_CONFIG_NAME)

    def getOpenAiConfig(self) -> dict:
        return self.__getConfig(self.__OPEN_AI_CONFIG_NAME)

    def getTelegramConfig(self) -> dict:
        return self.__getConfig(self.__TELEGRAM_CONFIG_NAME)

    def getStableDiffusionConfig(self) -> dict:
        return self.__getConfig(self.__STABLE_DIFFUSION_CONFIG_NAME)

    def __getConfig(self, configName: str) -> dict:
        if not configName in self.__data:
            raise Exception('Config %s Is Not Exists' % configName)

        return self.__data[configName]

    def __setConfig(self, configName: str):
        configFilePath = self.__getConfigFilePath(configName)

        if not path.exists(configFilePath) or not path.isfile(configFilePath):
            raise Exception('Config File %s Not Found' % configName)

        configFile = open(configFilePath, "r")

        self.__data[configName] = json.loads(configFile.read())

    def __getConfigFilePath(self, configName: str) -> str:
        return self.__CONFIG_FILE_PATH % (getcwd(), configName)
