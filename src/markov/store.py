import sqlite3

from os import path, getcwd, chmod

from typing import Union

#to-do: refactoring code syle
#to-do: add logs
class Store:
    __DB_FILE_PATH = '%s/data/markov.sqlite3'

    __CREATE_DICTIONARY_TABLE = '''
        CREATE TABLE dictionary (
            id   integer PRIMARY KEY,
            word text,

            UNIQUE (word) ON CONFLICT REPLACE
        );
    '''

    __CREATE_CHUNKS_TABLE = '''
        CREATE TABLE chunks (
            id    text,
            value text,

            UNIQUE (id) ON CONFLICT REPLACE
        );
    '''

    __INSERT_TO_DICTIONARY_SQL = '''
        INSERT INTO dictionary
        VALUES (:id, :word);
    '''

    __INSERT_TO_CHUNKS_SQL = '''
        INSERT INTO chunks
        VALUES (:id, :value);
    '''

    __UPDATE_CHUNKS_BY_ID_SQL = '''
        UPDATE chunks
        SET value = :value
        WHERE id = :id
    '''

    __SELECT_WORD_FROM_DICTIONARY_BY_ID_SQL = '''
        SELECT word
        FROM dictionary
        WHERE id = :id;
    '''

    __SELECT_MAX_ID_FROM_DICTIONARY_BY_ID_SQL = '''
        SELECT MAX(id)
        FROM dictionary;
    '''

    __SELECT_ID_FROM_DICTIONARY_BY_WORD_SQL = '''
        SELECT id
        FROM dictionary
        WHERE word = :word;
    '''

    __SELECT_VALUE_FROM_CUNKS_BY_ID_SQL = '''
        SELECT value
        FROM chunks
        WHERE id = :id;
    '''

    __dbConnection = None

    def __init__(self):
        dbFilePath = self.__getDBFilePath()

        if not path.exists(dbFilePath) or not path.isfile(dbFilePath):
            self.__initStore()
            chmod(dbFilePath, 0o755)

    def getWordFromDictionaryById(self, id: int) -> Union[str, None]:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__SELECT_WORD_FROM_DICTIONARY_BY_ID_SQL, {'id': id})

        row = cursor.fetchone()

        if row == None or row[0] == None:
            return None

        return row[0]

    def getIdFromDictionaryByWord(self, word: str) -> Union[int, None]:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__SELECT_ID_FROM_DICTIONARY_BY_WORD_SQL, {'word': word})

        row = cursor.fetchone()

        if row == None or row[0] == None:
            return None

        return row[0]

    def getValueFromCunksById(self, id: str) -> Union[str, None]:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__SELECT_VALUE_FROM_CUNKS_BY_ID_SQL, {'id': id})

        row = cursor.fetchone()

        if row == None or row[0] == None:
            return None

        return row[0]

    def insertRowToDictionary(self, word: str) -> int:
        self.__getDictionaryMaxId()

        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        row = {
            'id': self.__getDictionaryMaxId() + 1,
            'word': word
        }

        cursor.execute(self.__INSERT_TO_DICTIONARY_SQL, row)

        self.__dbConnection.commit()

        return self.__getDictionaryMaxId()

    def insertRowToChunks(self, id: str, value: str) -> bool:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        row = {
            'id':    id,
            'value': value
        }

        cursor.execute(self.__INSERT_TO_CHUNKS_SQL, row)

        self.__dbConnection.commit()

        return True


    def updateChunksById(self, id: str, value: str) -> bool:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        row = {
            'id':    id,
            'value': value
        }

        cursor.execute(self.__UPDATE_CHUNKS_BY_ID_SQL, row)

        self.__dbConnection.commit()

        return True

    def close(self):
        if self.__dbConnection is not None:
            self.__dbConnection.close()
            self.__dbConnection = None

    def __getDictionaryMaxId(self) -> int:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__SELECT_MAX_ID_FROM_DICTIONARY_BY_ID_SQL)

        row = cursor.fetchone()

        if row == None :
            return 0

        id = row[0]

        if id == None or id < 0:
            return 0

        return id

    def __connect(self):
        dbFilePath = self.__getDBFilePath()

        self.__dbConnection = sqlite3.connect(dbFilePath)

    def __getDBFilePath(self) -> str:
        return self.__DB_FILE_PATH % getcwd()

    def __initStore(self) -> str:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__CREATE_DICTIONARY_TABLE)
        cursor.execute(self.__CREATE_CHUNKS_TABLE)

        self.__dbConnection.commit()
