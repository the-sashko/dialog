import re
import sqlite3
import json
from typing import Union
from os import getcwd, path

#to-do: refactoring code syle
#to-do: add logs
class Storage:
    __MAX_THREAD_LENGTH = 20

    __DATA_BASE_FILE_PATH = '%s/data/db.sqlite3'
    __SOURCES_DIR_PATH = '%s/data/sources'

    __connection = None

    def __init__(self):
        if not path.isfile(self.__DATA_BASE_FILE_PATH % getcwd()):
            self.__create_db()

    def __del__(self):
        self.__close()

    def get_context(
        self,
        user_id: int,
        chat_id: int
    ) -> Union[list, None]:
        #thread = self.__get_thread_by_user_id_and_chat_id(
        #    user_id,
        #    chat_id
        #)

        thread = self.__get_thread_by_chat_id(chat_id)

        #if thread is None:
        #    thread = self.__get_thread_by_chat_id(chat_id)

        if thread is None:
            thread = self.__get_thread_by_user_id(user_id)

        return thread

    def save_message(
        self,
        user_id: int,
        chat_id: int,
        user_name: str,
        chat_name: str,
        message: dict
    ) -> None:
        if (
            'content' not in message or
            not isinstance(message['content'], str) or
            message['content'] == ''
        ):
            return None

        if chat_id > 0:
            self.__save_message_to_sources(
                chat_id,
                message['content']
            )

        self.__save_message_to_chat(
            chat_id,
            chat_name,
            message
        )

        self.__save_message_to_user(
            user_id,
            user_name,
            message
        )

        thread_id = self.__get_thread_id(user_id, chat_id)

        thread = self.__get_thread_by_id(thread_id)

        if thread is None:
            thread = []
            thread.append(message)

            self.__insert_thead(
                thread_id,
                user_id,
                chat_id,
                user_name,
                chat_name,
                thread
            )

            return None

        thread.append(message)

        self.__update_thead(
            thread_id,
            thread
        )

        return None

    def get_all_chat_ids(self) -> Union[list, None]:
        chat_ids = []

        sql = '''
            SELECT DISTINCT chat_id
            FROM threads
            WHERE chat_id != 0;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        if rows is None or len(rows) < 1:
            return None

        for row in rows:
            chat_ids.append(int(row[0]))

        if len(chat_ids) < 1:
            return None

        return chat_ids

    def update_chunks_by_id(
        self,
        chunk_id: str,
        value: str
    ) -> None:
        sql = '''
            UPDATE chunks
            SET value = :value
            WHERE id = :id
        '''

        row = {
            'id': chunk_id,
            'value': value
        }

        cursor = self.__get_cursor()

        cursor.execute(sql, row)

        self.__commit()

    def get_word_from_dictionary_by_id(
        self,
        dictionary_id: int
    ) -> Union[str, None]:
        sql = '''
            SELECT word
            FROM dictionary
            WHERE id = :id;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql, {'id': dictionary_id})

        row = cursor.fetchone()

        if row is None or row[0] is None:
            return None

        return row[0]

    def get_id_from_dictionary_by_word(
        self,
        word: str
    ) -> Union[int, None]:
        sql = '''
            SELECT id
            FROM dictionary
            WHERE word = :word;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql, {'word': word})

        row = cursor.fetchone()

        if row is None or row[0] is None:
            return None

        return row[0]

    def get_value_from_chunks_by_id(
        self,
        chunk_id: str
    ) -> Union[str, None]:
        sql = '''
            SELECT value
            FROM chunks
            WHERE id = :id;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql, {'id': chunk_id})

        row = cursor.fetchone()

        if row is None or row[0] is None:
            return None

        return row[0]

    def insert_row_to_dictionary(self, word: str) -> int:
        sql = '''
            INSERT INTO dictionary
            VALUES (:id, :word);
        '''

        cursor = self.__get_cursor()

        row = {
            'id': self.__get_dictionary_max_id() + 1,
            'word': word
        }

        cursor.execute(sql, row)

        self.__commit()

        return self.__get_dictionary_max_id()

    def insert_row_to_chunks(
        self,
        chunk_id: str,
        value: str
    ) -> None:
        sql = '''
            INSERT INTO chunks
            VALUES (:id, :value);
        '''

        cursor = self.__get_cursor()

        row = {
            'id': chunk_id,
            'value': value
        }

        cursor.execute(sql, row)

        self.__commit()

    def __save_message_to_chat(
        self,
        chat_id: int,
        chat_name: int,
        message: dict
    ) -> None:
        thread_id = self.__get_thread_id(0, chat_id)

        thread = self.__get_thread_by_id(thread_id)

        if thread is None:
            thread = []
            thread.append(message)

            self.__insert_thead(
                thread_id,
                0,
                chat_id,
                '',
                chat_name,
                thread
            )

            return None

        thread.append(message)

        self.__update_thead(
            thread_id,
            thread
        )

        return None

    def __save_message_to_user(
        self,
        user_id: int,
        user_name: str,
        message: dict
    ) -> None:
        thread_id = self.__get_thread_id(user_id, 0)

        thread = self.__get_thread_by_id(thread_id)

        if thread is None:
            thread = []
            thread.append(message)

            self.__insert_thead(
                thread_id,
                user_id,
                0,
                user_name,
                '',
                thread
            )

            return None

        thread.append(message)

        self.__update_thead(
            thread_id,
            thread
        )

        return None

    def __get_thread_by_chat_id(
        self,
        chat_id: int
    ) -> Union[list, None]:
        thread_id = self.__get_thread_id(0, chat_id)

        return self.__get_thread_by_id(thread_id)

    def __get_thread_by_user_id(
        self,
        user_id: int
    ) -> Union[list, None]:
        thread_id = self.__get_thread_id(user_id, 0)

        return self.__get_thread_by_id(thread_id)

    def __get_thread_by_user_id_and_chat_id(
        self,
        user_id: int,
        chat_id: int
    ) -> Union[list, None]:
        thread_id = self.__get_thread_id(user_id, chat_id)

        return self.__get_thread_by_id(thread_id)

    def __create_db(self) -> None:
        cursor = self.__get_cursor()

        cursor.execute('''
            CREATE TABLE threads(
                id TEXT PRIMARY KEY,
                chat_id INTEGER,
                user_id INTEGER,
                user_name TEXT,
                chat_name TEXT,
                thread TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE dictionary (
                id INTEGER PRIMARY KEY,
                word TEXT,
                UNIQUE (word) ON CONFLICT REPLACE
            );
        ''')

        cursor.execute('''
            CREATE TABLE chunks (
                id TEXT,
                value TEXT,
                UNIQUE (id) ON CONFLICT REPLACE
            );
        ''')

        self.__commit()

        cursor.execute('''
            CREATE INDEX threads_chat_id ON threads(chat_id);
        ''')

        self.__commit()

        cursor.execute('''
            CREATE INDEX threads_user_id ON threads(user_id);
        ''')

        self.__commit()

        cursor.execute('''
            CREATE UNIQUE INDEX threads_chat_id_user_id
                ON threads(chat_id, user_id);
        ''')

        self.__commit()

    def __set_connection(self) -> None:
        if self.__connection is None:
            self.__connection = sqlite3.connect(
                self.__DATA_BASE_FILE_PATH % getcwd()
            )

    def __get_cursor(self) -> sqlite3.Cursor:
        if self.__connection is None:
            self.__set_connection()

        return self.__connection.cursor()

    def __commit(self) -> None:
        if self.__connection is not None:
            self.__connection.commit()

    def __close(self) -> None:
        if self.__connection is not None:
            self.__connection.close()

    def __get_thread_id(self, user_id: int, chat_id: int) -> str:
        if user_id == 0:
            user_id = 'x'

        if chat_id == 0:
            chat_id = 'x'

        return f'{user_id}_{chat_id}'

    def __get_thread_by_id(self, thread_id: str) -> Union [list, None]:
        sql = '''
            SELECT thread
            FROM threads
            WHERE id = ?
            LIMIT 1;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql, (thread_id,))

        rows = cursor.fetchall()

        if len(rows) < 1:
            return None

        row = rows[0]

        if len(row) < 1:
            return None

        thread = row[0]

        if len(thread) < 1:
            return None

        try:
            return json.loads(thread)
        except Exception:
            return None

    def __insert_thead(
        self,
        thread_id: str,
        user_id: int,
        chat_id: int,
        user_name: str,
        chat_name: str,
        thread: list
    ) -> None:
        sql = '''
            INSERT INTO threads (
                id,
                user_id,
                chat_id,
                user_name,
                chat_name,
                thread
            )
            VALUES (?, ?, ?, ?, ?, ?);
        '''

        self.__get_cursor().execute(
            sql,
            (thread_id, user_id, chat_id, user_name, chat_name, json.dumps(thread),)
        )

        self.__commit()

    def __update_thead(
        self,
        thread_id: str,
        thread: list
    ) -> None:
        sql = '''
            UPDATE threads
            SET thread = ?
            WHERE id = ?;
        '''

        if len(thread) > self.__MAX_THREAD_LENGTH:
            thread.pop(0)

        self.__get_cursor().execute(sql, (json.dumps(thread), thread_id,))
        self.__commit()

    def __get_dictionary_max_id(self) -> int:
        sql = '''
            SELECT MAX(id)
            FROM dictionary;
        '''

        cursor = self.__get_cursor()

        cursor.execute(sql)

        row = cursor.fetchone()

        if row is None :
            return 0

        max_id = row[0]

        if max_id is None or max_id < 0:
            return 0

        return max_id

    def __save_message_to_sources(
        self,
        chat_id: int,
        message: str
    ) -> None:
        message = re.sub(r'\s+', r' ', message)
        message = re.sub(r'((^\s+)|(\s+$))', r'', message)
        #message = re.sub(r'(\[([^\[\]])+\])', r'', message)
        message = re.sub(r'\s+', r' ', message)
        message = re.sub(r'((^\s+)|(\s+$))', r'', message)

        if message == '':
            return None

        file_path = self.__SOURCES_DIR_PATH % getcwd()
        file_path = f'{file_path}/chats/{chat_id}.txt'

        if path.isfile(file_path):
            message = f'\n{message}'

        with open(file_path, 'a+', -1, 'utf-8') as file_pointer:
            file_pointer.write(message)
            file_pointer.close()
