import multilangual as ml

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

    def __init__(self, telegram_id='', language="ru"):
        self.__telegram_id = telegram_id
        self.language = language
        self.__ruz_id = 0
        self.__stage = 0
        self.__mode = 0
        self.__show_empty_days = [True]*6 + [False]

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
        then language pack is en
        :param lang:
        '''
        if lang in ml.languages:
            self.__language = lang
        else:
            self.__language = "en"

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

    @property
    def stage(self):
        return self.__stage

    @stage.setter
    def stage(self, value):
        self.__stage = value

    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, value):
        self.__mode = value

    @staticmethod
    def load_from_dict(d: dict):
        u = User()
        u.__telegram_id = d['telegram_id']
        u.__language = d['language']
        u.__ruz_id = d['ruz_id']
        u.__stage = d['stage']
        u.__mode = d['mode']
        u.__show_empty_days = d['show_empty_days']
        return u

    def __eq__(self, other):
        if not isinstance(other, (User, str)):
            raise TypeError("Right operand must be <class 'User'> or str")
        tid = other if isinstance(other, str) else other.__telegram_id
        return self.__telegram_id == tid

    def to_dict(self):
        return {
            'telegram_id': self.__telegram_id,
            'ruz_id': self.__ruz_id,
            'language': self.__language,
            'stage': self.__stage,
            'mode': self.__mode,
            'show_empty_days': self.__show_empty_days
        }

    def get_show_empty_day(self, day: int):
        return self.__show_empty_days[day]

    def set_show_empty_day(self, day: int, mode=True):
        self.__show_empty_days[day] = mode

    def change_show_empty_day(self, day: int):
        self.__show_empty_days[day] = not self.__show_empty_days[day]


def get_str_for_user(user: User, msg: str) -> str:
    lang = user.language
    return ml.language_packs[lang][msg]
