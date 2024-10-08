#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Дополнительно к требуемым в заданиях операциям
# перегрузить операцию индексирования [].
# Максимально возможный размер списка задать константой.
# В отдельном поле size должно храниться максимальное для
# данного объекта количество элементов списка;
# реализовать метод size(), возвращающий установленную длину.
# Если количество элементов списка изменяется во время работы,
# определить в классе поле count. Первоначальные значения s
# ize и count устанавливаются конструктором.
# В тех задачах, где возможно, реализовать конструктор инициализации строкой.
# Карточка иностранного слова представляет собой словарейу,
# содержащую иностранное слово и его перевод. Для моделирования
# электронного словаря иностранных слов реализовать класс Dictionary.
# Данный класс имеет поле-название словаря и содержит список
# словарей WordCard, представляющих собой карточки иностранного слова.
# Название словаря задается при создании нового словаря, но должна быть
# предоставлена возможность его изменения во время работы.
# Карточки добавляются в словарь и удаляются из него.
# Реализовать поиск определенного слова как отдельный метод.
# Аргументом операции индексирования должно быть иностранное слово.
# В словаре не должно быть карточек- дублей. Реализовать операции объединения,
# пересечения и вычитания словарей. При реализации должен
# создаваться новый словарь, а исходные словари не должны изменяться.
# При объединении новый словарь должен содержать без повторений все слова,
# содержащиеся в обоих словарях-операндах. При пересечении новый словарь
# должен состоять только из тех слов, которые имеются в обоих
# словарях-операндах. При вычитании новый словарь должен содержать
# слова первого словаря-операнда, отсутствующие во втором.


class WordCard:
    """
    Карточка словаря.
    """

    def __init__(self, foreign_word: str, translation: str):
        self.foreign_word = foreign_word
        self.translation = translation

    def __eq__(self, other: str):
        return self.foreign_word == other

    def __hash__(self):
        return hash(self.foreign_word)

    def __repr__(self):
        return f"{self.foreign_word}: {self.translation}"


class Dictionary:
    """
    Класс словаря.
    """

    MAX_SIZE = 100

    def __init__(self, name: str, init_string: str | None = None):
        self.name = name
        self.cards = set()
        self.count = 0
        self.size = self.MAX_SIZE
        if init_string:
            self.init_from_string(init_string)

    def init_from_string(self, init_string: str):
        pairs = init_string.split(",")
        for pair in pairs:
            foreign_word, translation = pair.split(":")
            self.__setitem__(foreign_word.strip(), translation.strip())

    def rename(self, new_name: str):
        self.name = new_name

    def __add_card(self, word_card: WordCard):
        if self.count < self.size:
            self.cards.add(word_card)
            self.count += 1
        else:
            print(f"Словарь {self.name} переполнен")

    def __remove_card(self, foreign_word: str):
        self.cards.remove(foreign_word)
        self.count -= 1

    def __find_word(self, foreign_word: str) -> WordCard | None:
        for card in self.cards:
            if card.foreign_word == foreign_word:
                return card
        return None

    def __getitem__(self, foreign_word: str):
        return self.__find_word(foreign_word)

    def __setitem__(self, foreign_word: str, translation: str):
        card = self.__find_word(foreign_word)
        if card:
            card.translation = translation
        else:
            self.__add_card(WordCard(foreign_word, translation))

    def __delitem__(self, foreign_word: str):
        card = self.__find_word(foreign_word)
        if card:
            self.__remove_card(foreign_word)
        else:
            print(f"Перевод слова {foreign_word} не найден")

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        return f"Словарь '{self.name}': {list(self.cards)}"

    def __len__(self):
        return self.count

    def size(self):
        return self.size


class DictUtils:
    """
    Класс для работы с словарями.
    """

    @staticmethod
    def union(first: Dictionary, second: Dictionary) -> Dictionary:
        new_dict = Dictionary(f"{first.name} |(или) {second.name}")
        new_dict.cards = first.cards | second.cards
        return new_dict

    @staticmethod
    def intersection(first: Dictionary, second: Dictionary) -> Dictionary:
        new_dict = Dictionary(f"{first.name} &(и) {second.name}")
        new_dict.cards = first.cards & second.cards
        return new_dict

    @staticmethod
    def difference(first: Dictionary, second: Dictionary) -> Dictionary:
        new_dict = Dictionary(f"{first.name} -(минус) {second.name}")
        new_dict.cards = first.cards - second.cards
        return new_dict


if __name__ == "__main__":
    dict1 = Dictionary("Словарь 1")
    dict1["cat"] = "кот"
    dict1["dog"] = "собака"
    dict1["bird"] = "птица"

    dict2 = Dictionary("Словарь 2")
    dict2["cat"] = "кот"
    dict2["mouse"] = "мышь"
    print(dict1)
    del dict1["dog"]
    print(dict1)
    print(dict1["dog"])
    # Объединение
    ut = DictUtils
    union_dict = ut.union(dict1, dict2)
    print(union_dict)

    # Пересечение
    intersection_dict = ut.intersection(dict1, dict2)
    print(intersection_dict)

    # Вычитание
    difference_dict = ut.difference(dict1, dict2)
    print(difference_dict)

    for card in dict1:
        print(card)

    dict3 = Dictionary(
        "Словарь 3", "car:машина, ship:корабль, airplane:самолет"
    )
    print(dict3)
    dict3.rename("Новый словарь 3")
    print(dict3)
    print(f"Количество карточек в словаре {dict3.name}: {len(dict3)}")
