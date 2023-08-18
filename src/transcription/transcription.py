import openai
from typing import Union
from settings.settings import Settings

#to-do: add logs
class Transcription:
    __WHISPER_1_MODEL = 'whisper-1'

    def __init__(self):
        config = Settings().get_open_ai_config()

        openai.api_key = config['api_key']

    def transcribe(self, audio_file_path: str) -> Union[str, None]:
        audio_file = open(audio_file_path, 'rb', -1, 'utf-8')

        transcript = openai.Audio.transcribe(
            self.__WHISPER_1_MODEL,
            audio_file
        )

        if 'text' in transcript:
            return transcript['text']

        return None
