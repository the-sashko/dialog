from typing import Union

#to-do: refactoring code syle
#to-do: add logs
class Script:
    TEST_SCRIPT = 'test'
    HELLO_SCRIPT = 'hello'
    ABOUT_ME_SCRIPT = 'about_me'
    RANDOM_TEXT_SCRIPT = 'random_text'
    RANDOM_VOICE_SCRIPT = 'random_voice'
    RANDOM_IMAGE_SCRIPT = 'random_image'
    NONE_SCRIPT = 'none'

    def run(
        name: str,
        data: Union[dict, None] = None
    ) -> None:
        #TO-Do
        return None
