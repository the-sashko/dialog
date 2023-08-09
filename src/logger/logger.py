from os import getcwd, path, remove, mkdir, chmod

import datetime
import sys

from telegram.telegram import Telegram

class Logger:
    __LOG_DIR_PATH  = '%s/data/logs/%s'
    __LOG_FILE_PATH = '%s/%s.log'

    __DEFAULT_LOG_TYPE = 'info'

    __LOG_MESSAGE_FORMAT = '[%s] %s\n'

    __telegram = None

    def __init__(self):
        self.__telegram = Telegram()

    def log(self, message: str, log_type: str = 'info') -> bool:
        if len(log_type) < 1:
            return False

        if len(log_type) < 1:
            log_type = self.__DEFAULT_LOG_TYPE

        print('[%s] %s\n' % (log_type.upper(), message))

        log_type = log_type.lower()

        log_file_path = self.__get_log_file_path(log_type)

        self.__create_log_dir(log_type)
        self.__create_log_file(log_file_path)
        self.__remove_old_log_file(log_type)

        current_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        message = self.__LOG_MESSAGE_FORMAT % (current_time, message)

        log_file = open(log_file_path, 'a')

        log_file.write(message)
        log_file.close()

        return True

    def log_error(self, exp: Exception):
        try:
            if hasattr(exp, 'message'):
                error_message = exp.message
            else:
                error_message = str(exp)

            self.log(error_message, 'error')

            self.__telegram.send_message_to_log_chat('[ERROR] %s' % error_message)
        except Exception as exp:
            if hasattr(exp, 'message'):
                error_message = exp.message
            else:
                error_message = str(exp)

            print('FATAL ERROR: %s' % error_message)
            sys.exit(1)

    def __get_log_dir_path(self, log_type: str) -> str:
        return self.__LOG_DIR_PATH % (getcwd(), log_type)

    def __create_log_dir(self, log_type: str):
        log_dir_path = self.__get_log_dir_path(log_type)

        if not path.exists(log_dir_path) or not path.isdir(log_dir_path):
            mkdir(log_dir_path)
            chmod(log_dir_path, 0o755)

    def __get_old_log_name(self, log_type: str) -> str:
        old_year = str(int(datetime.datetime.today().strftime('%Y')) - 1)
        month   = datetime.datetime.today().strftime('%m')
        day     = datetime.datetime.today().strftime('%d')

        return '%s-%s-%s-%s' % (log_type, old_year, month, day)

    def __get_old_log_file_path(self, log_type: str) -> str:
        log_dir_path = self.__get_log_dir_path(log_type)
        old_log_name = self.__get_old_log_name(log_type)

        return self.__LOG_FILE_PATH % (log_dir_path, old_log_name)

    def __remove_old_log_file(self, log_type: str):
        old_log_file_path = self.__get_old_log_file_path(log_type)

        if path.exists(old_log_file_path) and path.isfile(old_log_file_path):
            remove(old_log_file_path)

    def __get_log_name(self, log_type: str) -> str:
        year  = datetime.datetime.today().strftime('%Y')
        month = datetime.datetime.today().strftime('%m')
        day   = datetime.datetime.today().strftime('%d')

        return '%s-%s-%s-%s' % (log_type, year, month, day)

    def __get_log_file_path(self, log_type: str) -> str:
        log_dir_path = self.__get_log_dir_path(log_type)
        log_name    = self.__get_log_name(log_type)

        return self.__LOG_FILE_PATH % (log_dir_path, log_name)

    def __create_log_file(self, log_file_path: str):
        if not path.exists(log_file_path) or not path.isfile(log_file_path):
            with open(log_file_path, 'a'):
                pass

        chmod(log_file_path, 0o755)
