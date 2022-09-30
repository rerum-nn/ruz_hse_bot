import os.path
import re
import json
from user import User

class DatabaseOfUsers:

    __users = []
    __count_of_users = 0
    __path_to_database = ''

    def __init__(self, path: str):
        if not os.path.exists(path):
            spl = re.split('\\/', path)
            dirs = '/'.join(spl[:-1])
            os.makedirs(dirs)
            with open(path, 'w', encoding='utf-8') as file:
                pass

        with open(path, 'r', encoding='utf-8') as file:
            self.__users = json.load(file)

        self.__count_of_users = len(self.__users)
        self.__path_to_database = path

    def add_new_user(self, user: User) -> None:
        self.__users.append(user)


