class WrongLanguage(Exception):
    '''
    The Wrong Language exception is called when the wrong language pack
    is selected.

    Attributes
    ----------
    telegram_id : int
        id of the user who tried to change the language
    language : str
        the language that the attempt was made to change the settings to
    '''

    telegram_id = 0
    language = ''


