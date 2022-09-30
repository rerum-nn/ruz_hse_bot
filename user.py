from multilangual import languages
from ruz_exceptions import WrongLanguage


class User:
    '''
    The User class is intended for storing data about the bot user.

    Properties
    -------
    telegram_id : str
        user`s telegram id
    language : str
        user`s language pack
    ruz_id : str
        current user`s ruz id
    '''

    __telegram_id = ''
    __language = ""
    __ruz_id = ''

    @property
    def telegram_id(self) -> str:
        '''
        Return user`s telegram id
        '''
        return self.__telegram_id

    @property
    def language(self) -> str:
        '''
        Returns user`s language pack
        '''
        return self.__language

    @language.setter
    def language(self, lang: str) -> None:
        '''
        Changes the language pack for the user, if there is no language pack,
        then raise the WrongLanguage exception
        :param lang:
        '''
        if lang in languages:
            self.__language = lang
        else:
            wl = WrongLanguage
            wl.language = lang
            wl.telegram_id = self.__telegram_id
            raise wl

    @property
    def ruz_id(self) -> str:
        '''
        Return current user`s ruz_id
        '''
        return self.__ruz_id

    @ruz_id.setter
    def ruz_id(self, value: str) -> None:
        '''
        Change current user`s ruz_id
        '''
        self.__ruz_id = value

    def __init__(self, telegram_id, language):
        self.__telegram_id = telegram_id
        self.__language = language

    def __eq__(self, other):
        if isinstance(other, (User, str)):
            raise TypeError("Right operand must be <class 'User'> or str")
        tid = other if isinstance(other, int) else other.__telegram_id
        return self.__telegram_id == tid

