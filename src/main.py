# -*- coding: utf-8 -*-

"""Пример реализации ООП без классов.
"""
import importlib
from typing import Callable


def importer_conventional() -> None:
    """Импортировать имена для классического подхода.
    """
    module = importlib.import_module('conventional')
    globals()['Parrot'] = module.Parrot
    globals()['Cat'] = module.Cat
    globals()['Animal'] = module.Animal


def importer_classless() -> None:
    """Импортировать имена для бесклассового подхода.
    """
    module = importlib.import_module('classless')
    globals()['Parrot'] = module.Parrot
    globals()['Cat'] = module.Cat
    globals()['Animal'] = module.Animal
    globals()['isinstance'] = module.isinstance
    globals()['type'] = module.type


def execute(title: str, importer: Callable) -> None:
    """Исполнить пользовательский код.
    """
    importer()
    parrot = Parrot(name='Poppy')
    cat = Cat(name='Whiskers')

    print('-' * 79)
    print(title)
    print(">>> parrot = Parrot(name='Poppy')")
    print(">>> cat = Cat(name='Whiskers')")

    print('>>> parrot.legs')
    print(repr(parrot.legs))

    print('>>> cat.legs')
    print(repr(cat.legs))

    print('>>> cat.say()')
    print(repr(cat.say()))

    print('>>> parrot.say()')
    print(repr(parrot.say()))

    print('>>> isinstance(parrot, Animal)')
    print(repr(isinstance(parrot, Animal)))

    print('>>> isinstance(parrot, Cat)')
    print(repr(isinstance(parrot, Cat)))

    print(">>> cat.call('Bobby')")
    print(repr(cat.call('Bobby')))

    print(">>> cat.call('Whiskers')")
    print(repr(cat.call('Whiskers')))

    print('>>> type(parrot)')
    print(type(parrot))

    print('>>> type(Parrot)')
    print(type(Parrot))


def main() -> None:
    """Точка входа.
    """
    sequence = [
        ('Классическая реализация:', importer_conventional),
        ('Бесклассовая реализация:', importer_classless),
    ]

    for title, importer in sequence:
        execute(title, importer)


if __name__ == '__main__':
    main()
