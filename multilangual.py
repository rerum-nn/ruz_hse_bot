import json

languages =["ru", "en"]

language_packs = {}


def load_language_packs() -> None:
    for language in languages:
        with open(f'language_packs/{language}.json', 'r', encoding='utf-8') as file:
            language_packs[language] = json.load(file)
