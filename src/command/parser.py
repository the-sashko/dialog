import re
from typing import Union
from command.command import Command

class Parser:
    def get_command_from_text(self, text: str) -> Union[Command, None]:
        command = self.__get_command_by_type(text, Command.IMAGE)

        if command is not None:
            return command

        command = self.__get_command_by_type(text, Command.VOICE)

        if command is not None:
            return command

        command = self.__get_command_by_type(text, Command.ASCII)

        if command is not None:
            return command

        command = self.__get_command_by_type(text, Command.SAY)

        if command is not None:
            return command

        command = self.__get_command_by_type(text, Command.SAY_ALL)

        if command is not None:
            return command

        return None

    def __get_command_by_type(
        self,
        text: str,
        command_type: str
    ) -> Union[Command, None]:
        pattern = r'^' + re.escape(command_type) + r'(.*?)$'

        if (re.search(pattern, text, flags=re.IGNORECASE) is not None):
            value = re.sub(pattern, r'\g<1>', text, 0, re.IGNORECASE)
            value = re.sub(r'\s+', r' ', value)
            value = re.sub(r'((^\s+)|(\s+$))', r'', value)

            if value == '':
                value = None

            return Command(command_type, value)

        return None
