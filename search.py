import requests


class Search:
    __data = []

    @property
    def data(self):
        return self.__data

    @property
    def size(self):
        return len(self.__data)

    def __init__(self):
        self.__data = []

    def __len__(self):
        return self.size

    def search_id(self, term: str, type: str) -> None:
        url = f"https://ruz.hse.ru/api/search?term={term}&type={type}"
        response = requests.get(url)
        self.__data = response.json()