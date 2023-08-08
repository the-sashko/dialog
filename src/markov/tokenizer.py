import json
from markov import store, dictionary

#to-do: refactoring code syle
#to-do: add logs
class Tokenizer():
    __dictionary = None
    __store = None

    def __init__(self):
        self.__dictionary = dictionary.Dictionary()
        self.__store = store.Store()

    def getTokenizedText(self, text: str) -> list:
        tokenizedText = text.split(' ')

        for tokenIndex, token in enumerate(tokenizedText) :
            tokenizedText[tokenIndex] = self.__dictionary.getIdByWord(token)

        return tokenizedText

    def makeChunkedText(self, tokenizedText: list, chunkLength: int) -> list:
        chunkedText = {}

        chunksCount = 0
        newChunksCount = 0

        for chunk in self.__getChunks(tokenizedText, chunkLength):
            if chunk[0] in chunkedText.keys():
                chunkedText[chunk[0]].append(chunk[1])
            else:
                chunkedText[chunk[0]] = [chunk[1]]

        for chunkId in chunkedText:
            chunkValue = chunkedText[chunkId]
            chunkValueFromStore = self.__store.getValueFromCunksById(chunkId)

            if chunkValueFromStore == None :
                self.__store.insertRowToChunks(chunkId, json.dumps(chunkValue))
                newChunksCount += 1
            else:
                chunkValue = chunkValue + json.loads(chunkValueFromStore)
                self.__store.updateChunksById(chunkId, json.dumps(chunkValue))

            chunksCount += 1

        return (chunksCount, newChunksCount)


    def __getChunks(self, tokens, length) -> dict:
        for i in range(len(tokens) - (length -1)) :
            chunk = {}
            for j in range(length) :
                chunk[j] = str(tokens[i + j])

            chunkValue = chunk[len(chunk) - 1]

            del chunk[len(chunk) - 1]

            chunkId = ';'.join(chunk.values())

            yield {
                0: chunkId,
                1: int(chunkValue)
            }
