import openai
from typing import Union
from settings.settings import Settings

#to-do: refactoring code syle
#to-do: add logs
class Transcription:
    __WHISPER_1_MODEL = 'whisper-1'

    def __init__(self):
        config = Settings().getOpenAiConfig()

        openai.api_key = config['api_key']

    def transcribe(self, audio_file_path: str) -> Union[str, None]:
        audio_file = open(audio_file_path, 'rb')

        transcript = openai.Audio.transcribe(
            self.__WHISPER_1_MODEL,
            audio_file
        )

        if 'text' in transcript:
            return transcript['text']

        return None
