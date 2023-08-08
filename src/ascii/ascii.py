import re
from typing import Union
from gpt.gpt import Gpt

class Ascii:
    __gpt = None

    def __init__(self):
        self.__gpt = Gpt()

    def create(self, prompt: str) -> Union[str,None]:
        #TO-DO: improve ascii for telegram format
        #TO-DO: improve error handling
        prompt = [
            {'role': 'system', 'content': 'You are a ASCII generator'},
            {'role': 'system', 'content': 'Generate ASCII visual representation of user prompt. If it is impossible return FALSE string'},
            {'role': 'user', 'content': prompt}
        ]

        ascii_message = self.__gpt.get(
            prompt,
            self.__gpt.GPT_3_MODEL
        )

        if ascii_message is None:
            return None

        response = ascii_message.lower()
        response = re.sub(r'([^a-z]+)', r'', ascii_message)

        if response == 'false':
            return None

        return ascii_message
