import openai
from typing import Union
from settings.settings import Settings
from telegram.message import Message as TelegramMessage
from storage.storage import Storage
from logger.logger import Logger

class Gpt:
    GPT_3_MODEL = 'gpt-3.5-turbo'
    GPT_3_MODEL_16K = 'gpt-3.5-turbo-16k'
    GPT_4_MODEL = 'gpt-4'
    #Will be able in future
    GPT_4_MODEL_32K = 'gpt-4-32k'

    __INITAL_PROMPT = 'Ти %s якого зовуть %s і який веде бесіду з юзером %s'

    __DEFAULT_PROMPT = [
        {'role': 'user', 'content': 'Привіт'},
        {'role': 'assistant', 'content': 'Привіт'}
    ]

    __storage = None
    __logger = None

    __bot_description = None
    __bot_name = None

    def __init__(self):
        open_api_config = Settings().get_open_ai_config()
        bot_config = Settings().get_bot_config()

        openai.api_key = open_api_config['api_key']

        self.__bot_description = bot_config['description']
        self.__bot_name = bot_config['name']

        self.__storage = Storage()
        self.__logger = Logger()

    def get_reply(
        self,
        message: TelegramMessage,
        mood: str = 'neutral'
    ) -> Union[str, None]:
        context = self.__storage.get_context(
            message.get_user().get_id(),
            message.get_chat().get_id()
        )

        parent_text = None

        prompt = self.__get_prompt(
            message.get_user().get_name(),
            message.get_text(),
            parent_text,#To-Do fix
            context,
            mood
        )

        reply = self.get(prompt)

        if reply == None:
            return reply

        self.__storage.save_message(
            message.get_user().get_id(),
            message.get_chat().get_id(),
            message.get_user().get_name(),
            message.get_chat().get_title(),
            {'role': 'assistant', 'content': reply}
        )

        return reply

    def paraphrase(
        self,
        text: str,
        mood: str = 'neutral',
        user_name: Union[str, None] = None
    ) -> Union[str, None]:
        if user_name is None:
            user_name = 'Юзер'

        prompt = [
            {'role': 'system', 'content': self.__INITAL_PROMPT}
        ]

        prompt[0]['content'] = prompt[0]['content'] % user_name        

        prompt.append({'role': 'system', 'content': 'Rewrite this text: %s' % text})

        if mood != 'neutral':
            prompt.append({'role': 'system', 'content': 'Give ansver is %s style' % mood})

        text = self.get(
            prompt,
            self.GPT_3_MODEL
        )

        if text == None:
            return None

        return text

    def get(
        self,
        prompt: list,
        model: Union[str, None] = None
    ) -> Union[str, None]:
        if model is None:
            model = self.__get_default_model()

            return self.get(prompt, model)

        self.__logger.log('Start sending prompt to ChatGPT')

        try: # To-Do: add validator
            response = openai.ChatCompletion.create(
                model=model,
                messages=prompt
            )

            self.__logger.log('End sending prompt to ChatGPT')

            return response.choices[0].message.content
        except Exception as exp:#To-Do: refactor, move to hadle error method
            self.__logger.log_error(exp)

            if model == self.GPT_3_MODEL:
                return None

            if model == self.GPT_3_MODEL_16K:
                self.__logger.log('Fallback to %s model' % self.GPT_3_MODEL)
                return self.get(prompt, self.GPT_3_MODEL)

            if model == self.GPT_4_MODEL:
                self.__logger.log('Fallback to %s model' % self.GPT_3_MODEL_16K)
                return self.get(prompt, self.GPT_3_MODEL_16K)

            if model == self.GPT_4_MODEL_32K:
                self.__logger.log('Fallback to %s model' % self.GPT_4_MODEL)
                return self.get(prompt, self.GPT_4_MODEL)

    def __get_prompt(
            self,
            user_name: str,
            message: str,
            parrent_message: Union[list, None],
            context: Union[list, None] = None,
            mood: str = 'neutral'
    ) -> list:
        prompt = [
            {'role': 'system', 'content': self.__INITAL_PROMPT}
        ]

        prompt[0]['content'] = prompt[0]['content'] % (self.__bot_description, self.__bot_name, user_name)

        if context == None:
           context = self.__DEFAULT_PROMPT

        for context_message in context:
            prompt.append(context_message)

        last_prompt_reply = prompt[-1]

        if parrent_message != None and last_prompt_reply['content'] == parrent_message:
            #To-Do move current message to last
            prompt.append({'role': 'assistant', 'content': parrent_message}) #To-Do: fix role (parent message can be from bot and user)

        last_prompt_reply = prompt[-1]

        if mood != 'neutral':
            prompt.append({'role': 'system', 'content': 'Give ansver is %s style' % mood})

        if last_prompt_reply['role'] == 'user' and last_prompt_reply['content'] == message:
            return prompt

        prompt.append({'role': 'user', 'content': message})

        return prompt

    def __get_default_model(self) -> str:
        mode = 'dev'#To-Do

        if mode == 'dev':
            return self.GPT_3_MODEL

        return self.GPT_4_MODEL # switch to GPT_4_MODEL_32K in future
