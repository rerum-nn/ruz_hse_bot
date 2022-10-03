import os.path
import re
import json
from user import User


class DatabaseOfUsers:

    __users = []
    __count_of_users = 0
    __path_to_database = ''

    def __init__(self, path: str):
        self.__users = []
        self.__count_of_users = 0

        if not os.path.exists(path):
            spl = re.split('\\/', path)
            dirs = '/'.join(spl[:-1])
            os.makedirs(dirs, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as file:
                pass
        else:
            with open(path, 'r', encoding='utf-8') as file:
                self.__users = [User.load_from_dict(item) for item in json.load(file)]

            self.__count_of_users = len(self.__users)
        self.__path_to_database = path

    def get_user_information_by_id(self, tg_id: str) -> User:
        i = self.__users.index(tg_id)
        return self.__users[i]

    def add_new_user(self, user: User) -> None:
        if user not in self.__users:
            self.__users.append(user)
            self.__count_of_users += 1
        else:
            self.__users[self.__users.index(user)].language = user.language
            self.__users[self.__users.index(user)].stage = 0

    def delete_user(self, user: (User, str)) -> None:
        if user in self.__users:
            self.__users.remove(user)
            self.__count_of_users -= 1

    def dump(self):
        with open(self.__path_to_database, 'w', encoding='utf-8') as file:
            json.dump([user.to_dict() for user in self.__users], file, ensure_ascii=False, indent=4)

    def __getitem__(self, item):
        if isinstance(item, int):
            item = str(item)
        if not isinstance(item, (str, User)):
            raise TypeError("Argument must be str or <class 'User'>")

        return self.__users[self.__users.index(item)]

