import numpy
import json
import os

from typing import Union

from markov.dictionary import Dictionary
from markov.formatter import Formatter
from markov.tokenizer import Tokenizer
from markov.store import Store
from logger.logger import Logger

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
    __store = None
    __logger = None

    def __init__(self):
        self.__dictionary = Dictionary()
        self.__formatter = Formatter()
        self.__tokenizer = Tokenizer()
        self.__store = Store()
        self.__logger = Logger()

    def getReply(self, text: str) -> Union[str, None]:
        self.__logger.log('Start Creating Markov Chain')

        tokenizedText = self.__getChainByText(text)

        if tokenizedText == None:
            self.__logger.log('End Creating Markov Chain With 0 Tokens')
            return None

        self.__logger.log('End Creating Markov Chain With ' + str(len(tokenizedText)) + ' Tokens')

        self.__logger.log('Start Translating Tokens')

        for tokenIndex, token in enumerate(tokenizedText) :
            if token == self.__dictionary.getStartId() :
                tokenizedText[tokenIndex] = ''
    
            if token == self.__dictionary.getEndId() :
                tokenizedText[tokenIndex] = '.'

            if token == self.__dictionary.getStopId() :
                tokenizedText[tokenIndex] = self.__dictionary.stop

            if token != self.__dictionary.getStartId() and token != self.__dictionary.getEndId() and token != self.__dictionary.getStopId() :
                tokenizedText[tokenIndex] = self.__dictionary.getWordById(token)

        self.__logger.log('End Translating Tokens')

        self.__logger.log('Start Formatting Output Text')

        text = self.__formatter.getFormattedTokenizedText(tokenizedText)

        text = text.split('?')
        
        if len(text) > 1:
            text = text[0] + '?'
        else:
            text = text[0]

        self.__logger.log('End Formatting Output Text')

        return text

    def do_parse(self):
        try:
            rawFilePath = self.__SOURCE_FILE_PATH % os.getcwd()

            if not os.path.isfile(rawFilePath):
                self.__logger.log('Start Merging Sources')
                self.__merge_sources()
                self.__logger.log('End Merging Sources')

            if not os.path.isfile(rawFilePath):
                self.__logger.log('File With RAW Data Is Not Exists')

                return False

            self.__logger.log('Start Parsing Text')

            self.__logger.log('Start Formatting Raw Text')
            

            rawFilePath = self.__SOURCE_FILE_PATH % os.getcwd()
            rawFile = open(rawFilePath, 'r')
            rawText = rawFile.read()

            formattedText = self.__formatter.getFormattedRawText(
                rawText
            )

            self.__logger.log('End Formatting Raw Text')

            self.__logger.log('Start Tokenizing Text')
            tokenizedText = self.__tokenizer.getTokenizedText(formattedText)
            self.__logger.log('End Tokenizing Text')

            chunkLength = self.__MIN_CHUNK_LENGTH

            while chunkLength <= self.__MAX_CHUNK_LENGTH:
                self.__logger.log('Start Splitting Text On Chunks (Length ' +
                    str(chunkLength) + ')')

                chunkCounts = self.__tokenizer.makeChunkedText(
                    tokenizedText,
                    chunkLength
                )

                self.__logger.log('End Splitting Text On ' +
                    str(chunkCounts[0]) + ' Chunks (' + 
                    str(chunkCounts[1]) + ' Chunks Is New)')

                chunkLength += 1

            rawFilePath = self.__SOURCE_FILE_PATH % os.getcwd()

            os.remove(rawFilePath)
            self.__logger.log('End Parsing Text')
        except Exception as exp:
            self.__logger.log_error(exp)

    def __getChainByText(self, text: str) -> list:
        formattedText = self.__formatter.getFormattedRawText(text)
        tokenizedText = self.__tokenizer.getTokenizedText(formattedText)
        tokenizedText.append(self.__dictionary.getStopId())
        tokenizedText.append(self.__dictionary.getStartId())

        return self.__getChainByTokenizedText(tokenizedText, [], 0)

    def __getChunkById(self, id: str) -> Union[list, None]:
        chunk = self.__store.getValueFromCunksById(id)

        if chunk == None:
            return None

        return json.loads(chunk)

    def __getChainByTokenizedText(self, tokenizedText: list, chain: list, sentenceCount: int) -> Union[list, None]:
        chunk = self.__getChunkByTokenizedText(tokenizedText)

        if chunk == None and len(chain) == 0:
            return None

        if chunk == None and len(tokenizedText) > 1:
            del tokenizedText[0]

            return self.__getChainByTokenizedText(tokenizedText, chain, sentenceCount)

        if chunk == None:
            return chain

        token = int(numpy.random.choice(chunk))

        if token == self.__dictionary.getEndId() :
            sentenceCount += 1

        chain.append(token)
        tokenizedText.append(token)

        if sentenceCount >= self.__MAX_SENTENTCES_COUNT :
            return chain

        return self.__getChainByTokenizedText(tokenizedText, chain, sentenceCount)


    def __getChunkByTokenizedText(self, tokenizedText: str) -> Union[list, None]:
        chunkId = []

        for token in tokenizedText:
            chunkId.append(str(token))

        chunkId = ';'.join(chunkId)

        chunk = self.__getChunkById(chunkId)

        return chunk

    def __merge_sources(self) -> None :
        result_file = self.__SOURCE_FILE_PATH % os.getcwd()
        
        source_files = [f for f in os.listdir(self.__SOURCE_DIR_PATH % os.getcwd()) if f.endswith('.txt')]

        with open(result_file, 'w') as outfile:
            for source_file in source_files:
                with open(os.path.join(self.__SOURCE_DIR_PATH % os.getcwd(), source_file), 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')
