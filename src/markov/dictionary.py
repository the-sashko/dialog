from typing import Union

from markov import store

#to-do: refactoring code syle
#to-do: add logs
class Dictionary():
    __store = None

    __START_ID = -3;
    __END_ID = -2;
    __STOP_ID = -1;

    start = '<START>'
    end = '<END>'
    stop = '<STOP>'

    def __init__(self):
        self.__store = store.Store()

    def getWordById(self, id: int) -> str:
        if id == self.__START_ID :
            return self.start

        if id == self.__END_ID :
            return self.end

        return self.__getWordFromStoreById(id)

    def getIdByWord(self, word: str) -> int:
        if word == self.start :
            return self.__START_ID

        if word == self.end :
            return self.__END_ID

        if word == self.stop :
            return self.__STOP_ID

        id = self.__getIdFromStoreByWord(word)

        if id != None :
            return id

        return self.__saveWordToStore(word)

    def getStartId(self) -> int:
        return self.__START_ID

    def getEndId(self) -> int:
        return self.__END_ID

    def getStopId(self) -> int:
        return self.__STOP_ID

    def __getWordFromStoreById(self, id: int) -> Union[str, None]:
        return self.__store.getWordFromDictionaryById(id)

    def __getIdFromStoreByWord(self, word: str) -> Union[int, None]:
        return self.__store.getIdFromDictionaryByWord(word)

    def __saveWordToStore(self, word: str) -> int:
        return self.__store.insertRowToDictionary(word)
