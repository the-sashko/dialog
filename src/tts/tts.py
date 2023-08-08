from gtts import gTTS
from os import getcwd
from pydub import AudioSegment

#to-do: constants
#to-do: add logs
class Tts:
    __FILE_PATH = '%s/data/tmp/tts.mp3'
    
    def text2audio(self, text: str) -> str:
        file_path = self.__FILE_PATH % getcwd()

        tts = gTTS(text, 'com.ua', 'uk')

        tts.save(file_path)
 
        sound = AudioSegment.from_file(file_path, format='mp3')

        sample_rate = int(sound.frame_rate * (2.0 ** -0.5))

        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': sample_rate})

        sound = sound.set_frame_rate(44100)
        sound = sound.speedup(1.5, 15, 25)
        sound = sound.normalize(0.1)

        sound.export(file_path, format='mp3')

        return file_path
