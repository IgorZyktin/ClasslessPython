# -*- coding: utf-8 -*-

"""Реализация ООП традиционным способом.
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    """Базовый класс для всех животных.
    """
    legs: int

    def __init__(self, name: str) -> None:
        """Инициализировать экземпляр.
        """
        self.name = name

    @abstractmethod
    def say(self) -> str:
        """Издать звук.
        """

    def call(self, given_name: str) -> str:
        """Попытаться позвать животное.

        Животное отзовётся, если его зовут по имени.
        """
        if given_name == self.name:
            return self.say()
        return 'no reaction'


class Parrot(Animal):
    """Класс попугая.
    """
    legs = 2

    def say(self) -> str:
        """Издать звук.
        """
        return 'Ara! ara!'


class Cat(Animal):
    """Класс кота.
    """
    legs = 4

    def say(self) -> str:
        """Издать звук.
        """
        return 'Meow!'
