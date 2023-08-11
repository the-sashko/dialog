from typing import Union
from image.dalee import Dalee
from image.stable_diffusion import StableDiffusion
from logger.logger import Logger

#to-do: refactoring code syle
#to-do: add logs
class Image:
    __dalee = None
    __stable_diffusion = None
    __logger = None

    def __init__(self):
        self.__dalee = Dalee()
        self.__stable_diffusion = StableDiffusion()
        self.__logger = Logger()

    def create_image(self, prompt: str) -> Union[str, None]:
        self.__logger.log(f'Start creating image by promt "{prompt}"')

        self.__logger.log('Using Stabel Diffusion API')

        file_path = self.__stable_diffusion.create_image(
            prompt
        )

        if file_path == None:
            self.__logger.log('Failed! Fallback to DALL-E API')

            file_path = self.__dalee.create_image(
                prompt
            )

        self.__logger.log(f'End creating image by promt {prompt}')

        return file_path
