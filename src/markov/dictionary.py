from typing import Union

from storage.storage import Storage

#to-do: refactoring code syle
#to-do: add logs
class Dictionary():
    __START_ID = -3;
    __END_ID = -2;
    __STOP_ID = -1;

    start = '<START>'
    end = '<END>'
    stop = '<STOP>'

    __storage = None

    def __init__(self):
        self.__storage = Storage()

    def get_word_by_id(self, id: int) -> str:
        if id == self.__START_ID :
            return self.start

        if id == self.__END_ID :
            return self.end

        return self.__get_word_from_store_by_id(id)

    def get_id_by_word(self, word: str) -> int:
        if word == self.start :
            return self.__START_ID

        if word == self.end :
            return self.__END_ID

        if word == self.stop :
            return self.__STOP_ID

        id = self.__get_id_from_store_by_word(word)

        if id != None :
            return id

        return self.__save_word_to_store(word)

    def get_start_id(self) -> int:
        return self.__START_ID

    def get_end_id(self) -> int:
        return self.__END_ID

    def get_stop_id(self) -> int:
        return self.__STOP_ID

    def __get_word_from_store_by_id(self, id: int) -> Union[str, None]:
        return self.__storage.get_word_from_dictionary_by_id(id)

    def __get_id_from_store_by_word(self, word: str) -> Union[int, None]:
        return self.__storage.get_id_from_dictionary_by_word(word)

    def __save_word_to_store(self, word: str) -> int:
        return self.__storage.insert_row_to_dictionary(word)
