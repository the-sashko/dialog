import json
from markov import dictionary
from storage.storage import Storage

#to-do: refactoring code syle
#to-do: add logs
class Tokenizer():
    __dictionary = None
    __storage = None

    def __init__(self):
        self.__dictionary = dictionary.Dictionary()
        self.__storage = Storage()

    def get_tokenized_text(self, text: str) -> list:
        tokenized_text = text.split(' ')

        for token_index, token in enumerate(tokenized_text) :
            tokenized_text[token_index] = self.__dictionary.get_id_by_word(token)

        return tokenized_text

    def make_chunked_text(
        self,
        tokenized_text: list,
        chunk_length: int
    ) -> list:
        chunked_text = {}

        chunks_count = 0
        new_chunks_count = 0

        for chunk in self.__get_chunks(tokenized_text, chunk_length):
            if chunk[0] in chunked_text.keys():
                chunked_text[chunk[0]].append(chunk[1])
            else:
                chunked_text[chunk[0]] = [chunk[1]]

        for chunk_id in chunked_text:
            chunk_value = chunked_text[chunk_id]

            chunk_value_from_store = self.__storage.get_value_from_chunks_by_id(
                chunk_id
            )

            if chunk_value_from_store is None :
                self.__storage.insert_row_to_chunks(chunk_id, json.dumps(chunk_value))
                new_chunks_count += 1
            else:
                chunk_value = chunk_value + json.loads(chunk_value_from_store)
                self.__storage.update_chunks_by_id(chunk_id, json.dumps(chunk_value))

            chunks_count += 1

        return (chunks_count, new_chunks_count)

    def __get_chunks(self, tokens, length) -> dict:
        for i in range(len(tokens) - (length -1)) :
            chunk = {}
            for j in range(length) :
                chunk[j] = str(tokens[i + j])

            chunk_value = chunk[len(chunk) - 1]

            del chunk[len(chunk) - 1]

            chunk_id = ';'.join(chunk.values())

            yield {
                0: chunk_id,
                1: int(chunk_value)
            }
