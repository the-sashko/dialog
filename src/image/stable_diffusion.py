import os
import io
from typing import Union
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from settings.settings import Settings
from logger.logger import Logger

class StableDiffusion:
    __STEPS = 150
    __IMAGE_WIDTH = 1024
    __IMAGE_HEIGHT = 1024
    __IMAGE_FILE_PATH = '%s/data/tmp/image.png'
    __HOST = 'grpc.stability.ai:443'
    __CFG_SCALE = 8.0

    __logger = None

    def __init__(self):
        config = Settings().get_stable_diffusion_config()

        os.environ['STABILITY_KEY'] = config['api_key']
        os.environ['STABILITY_HOST'] = self.__HOST

        self.__logger = Logger()

    def create_image(self, prompt: str) -> Union[str, None]:
        try:
            file_path = None

            stability_api = client.StabilityInference(
                key = os.environ['STABILITY_KEY'],
                verbose = True,
                engine = "stable-diffusion-xl-1024-v1-0",
            )

            answers = stability_api.generate(
                prompt = prompt,
                steps = self.__STEPS,
                cfg_scale = self.__CFG_SCALE,
                width = self.__IMAGE_WIDTH,
                height = self.__IMAGE_HEIGHT,
                samples = 1,
                sampler = generation.SAMPLER_K_DPMPP_2M
            )

            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        continue

                    if artifact.type == generation.ARTIFACT_IMAGE:
                        file_path = self.__IMAGE_FILE_PATH % os.getcwd()

                        if os.path.isfile(file_path):
                            os.remove(file_path)

                        Image.open(io.BytesIO(artifact.binary)).save(file_path)

            return file_path
        except Exception as exp:
            self.__logger.log_error(exp)

            None
