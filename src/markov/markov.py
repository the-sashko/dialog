import numpy
import json
import os

from typing import Union

from markov.dictionary import Dictionary
from markov.formatter import Formatter
from markov.tokenizer import Tokenizer
from logger.logger import Logger
from storage.storage import Storage

#to-do: refactoring code syle
#to-do: add logs
class Markov():
    __MAX_SENTENTCES_COUNT = 10

    __MIN_CHUNK_LENGTH = 2
    __MAX_CHUNK_LENGTH = 10

    __SOURCE_DIR_PATH = '%s/data/sources'
    __SOURCE_FILE_PATH = '%s/data/sources/raw.txt'

    __dictionary = None
    __formatter = None
    __tokenizer = None
    __storage = None
    __logger = None

    def __init__(self):
        self.__dictionary = Dictionary()
        self.__formatter = Formatter()
        self.__tokenizer = Tokenizer()
        self.__storage = Storage()
        self.__logger = Logger()

    def get_reply(self, text: str) -> Union[str, None]:
        self.__logger.log('Start creating markov chain')

        tokenized_text = self.__get_chain_by_text(text)

        if tokenized_text == None:
            self.__logger.log('End creating markov chain with 0 tokens')
            return None

        self.__logger.log('End creating markov chain with ' + str(len(tokenized_text)) + ' tokens')

        self.__logger.log('Start translating tokens')

        for token_index, token in enumerate(tokenized_text) :
            if token == self.__dictionary.get_start_id() :
                tokenized_text[token_index] = ''

            if token == self.__dictionary.get_end_id() :
                tokenized_text[token_index] = '.'

            if token == self.__dictionary.get_stop_id() :
                tokenized_text[token_index] = self.__dictionary.stop

            if token != self.__dictionary.get_start_id() and token != self.__dictionary.get_end_id() and token != self.__dictionary.get_stop_id() :
                tokenized_text[token_index] = self.__dictionary.get_word_by_id(token)

        self.__logger.log('End translating tokens')

        self.__logger.log('Start formatting output text')

        text = self.__formatter.get_formatted_tokenized_text(tokenized_text)

        text = text.split('?')

        if len(text) > 1:
            text = text[0] + '?'
        else:
            text = text[0]

        self.__logger.log('End formatting output text')

        return text

    def do_parse(self):
        try:
            raw_file_path = self.__SOURCE_FILE_PATH % os.getcwd()

            if not os.path.isfile(raw_file_path):
                self.__logger.log('Start merging sources')
                self.__merge_sources()
                self.__logger.log('End merging sources')

            if not os.path.isfile(raw_file_path):
                self.__logger.log('File with raw data is not exists')

                return False

            self.__logger.log('Start parsing text')

            self.__logger.log('Start formatting raw Ttxt')            

            raw_file = open(raw_file_path, 'r')
            raw_text = raw_file.read()

            formatted_text = self.__formatter.get_formatted_raw_text(
                raw_text
            )

            self.__logger.log('End formatting raw text')

            self.__logger.log('Start tokenizing text')

            tokenized_text = self.__tokenizer.get_tokenized_text(
                formatted_text
            )

            self.__logger.log('End tokenizing text')

            chunk_length = self.__MIN_CHUNK_LENGTH

            while chunk_length <= self.__MAX_CHUNK_LENGTH:
                self.__logger.log(
                    'Start splitting text on chunks (length %s )' % str(chunk_length)
                )

                chunk_counts = self.__tokenizer.make_chunked_text(
                    tokenized_text,
                    chunk_length
                )

                self.__logger.log(
                    'End splitting text on %s chunks (%s chunks is New)' % (str(chunk_counts[0]), str(chunk_counts[1]))
                )

                chunk_length += 1

            raw_file_path = self.__SOURCE_FILE_PATH % os.getcwd()

            os.remove(raw_file_path)

            self.__logger.log('End parsing text')
        except Exception as exp:
            self.__logger.log_error(exp)

    def __get_chain_by_text(self, text: str) -> list:
        formatted_text = self.__formatter.get_formatted_raw_text(text)
        formatted_text = self.__tokenizer.get_tokenized_text(formatted_text)
        formatted_text.append(self.__dictionary.get_stop_id())
        formatted_text.append(self.__dictionary.get_start_id())

        return self.__get_chain_by_tokenized_text(formatted_text, [], 0)

    def __get_chunk_by_id(self, id: str) -> Union[list, None]:
        chunk = self.__storage.get_value_from_chunks_by_id(id)

        if chunk == None:
            return None

        return json.loads(chunk)

    def __get_chain_by_tokenized_text(
        self,
        tokenized_text: list,
        chain: list,
        sentence_count: int
    ) -> Union[list, None]:
        chunk = self.__get_chunk_by_tokenized_text(
            tokenized_text
        )

        if chunk == None and len(chain) == 0:
            return None

        if chunk == None and len(tokenized_text) > 1:
            del tokenized_text[0]

            return self.__get_chain_by_tokenized_text(
                tokenized_text,
                chain,
                sentence_count
            )

        if chunk == None:
            return chain

        token = int(numpy.random.choice(chunk))

        if token == self.__dictionary.get_end_id() :
            sentence_count += 1

        chain.append(token)
        tokenized_text.append(token)

        if sentence_count >= self.__MAX_SENTENTCES_COUNT :
            return chain

        return self.__get_chain_by_tokenized_text(
            tokenized_text,
            chain,
            sentence_count
        )

    def __get_chunk_by_tokenized_text(
        self,
        tokenized_text: str
    ) -> Union[list, None]:
        chunk_id = []

        for token in tokenized_text:
            chunk_id.append(str(token))

        chunk_id = ';'.join(chunk_id)

        chunk = self.__get_chunk_by_id(chunk_id)

        return chunk

    def __merge_sources(self) -> None:
        result_file = self.__SOURCE_FILE_PATH % os.getcwd()
        
        source_files = [f for f in os.listdir(self.__SOURCE_DIR_PATH % os.getcwd()) if f.endswith('.txt')]

        with open(result_file, 'w') as output_file:
            for source_file in source_files:
                with open(os.path.join(self.__SOURCE_DIR_PATH % os.getcwd(), source_file), 'r') as input_file:
                    output_file.write(input_file.read())
                    output_file.write('\n')
