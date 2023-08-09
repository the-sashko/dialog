from typing import Union
from settings.settings import Settings
import os
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

#to-do: refactoring code syle
#to-do: add logs
class StableDiffusion:
    __STEPS = 150
    __IMAGE_WIDTH = 1024
    __IMAGE_HEIGHT = 1024
    __IMAGE_FILE_PATH = '%s/data/tmp/image.png'
    __HOST = 'grpc.stability.ai:443'

    def __init__(self):
        config = Settings().get_stable_diffusion_config()

        os.environ['STABILITY_KEY'] = config['api_key']
        os.environ['STABILITY_HOST'] = self.__HOST

    def create_image(self, prompt: str) -> Union[str, None]:
        try:
            file_path = None

            stability_api = client.StabilityInference(
                key = os.environ['STABILITY_KEY'],
                verbose = True,
                engine = "stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
            # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
            )

            answers = stability_api.generate(
                prompt = prompt,
                steps = self.__STEPS, # Amount of inference steps performed on image generation. Defaults to 30. 
                cfg_scale = 8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
                width = self.__IMAGE_WIDTH, # Generation width, defaults to 512 if not included.
                height = self.__IMAGE_HEIGHT, # Generation height, defaults to 512 if not included.
                samples = 1, # Number of images to generate, defaults to 1 if not included.
                sampler = generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
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
        except:
            None
