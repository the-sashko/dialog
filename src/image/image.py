from typing import Union
from image.dalee import Dalee
from image.stable_diffusion import StableDiffusion

#to-do: refactoring code syle
#to-do: add logs
class Image:
    __dalee = None
    __stable_diffusion = None

    def __init__(self):
        self.__dalee = Dalee()
        self.__stable_diffusion = StableDiffusion()

    def create_image(self, prompt: str) -> Union[str, None]:
        file_path = self.__stable_diffusion.create_image(
            prompt
        )

        if file_path == None:
            file_path = self.__dalee.create_image(
                prompt
            )

        return file_path
