# -*- coding: utf-8 -*-

"""Реализация ООП архаичным способом.
"""
from functools import partial
from typing import Any


def __my_getattr__(self, name: str) -> Any:
    """Получить атрибут объекта (если он не найден).
    """
    # если атрибут есть у экземпляра, просто возвращаем его
    if name in self['__my_dict__']:
        return self['__my_dict__'][name]

    # проходимся по перечню всех наших предков в
    # поисках требуемого атрибута
    for base_type in [
        self['__my_type__'],
        *self['__my_type__']['__my_bases__']
    ]:
        if name in base_type['__my_dict__']:
            attr = base_type['__my_dict__'][name]
            break
    else:
        raise AttributeError(f'У объекта нет атрибута {name}')

    # на этом этапе мы явно получили атрибут из класса (нашего или
    # родительского). в настоящем интерпретаторе тут будет работать
    # магия дескрипторов с возвратом экземпляра bound method
    # здесь мы просто применим partial и положим self первым аргументом
    # тут можно было бы включить в работу собственные варианты
    # декораторов staticmethod и classmethod
    if callable(attr):
        attr = partial(attr, self)

    return attr


def __my_call__(self, *args, **kwargs):
    """Вызов объекта.

    Для классов их вызов означает создание экземпляра объекта.
    Классы по своей сути это функторы.
    """
    return __my_new__(self, *args, **kwargs)


def __my_new__(cls, *args, **kwargs):
    """Создание экземпляра объекта.
    """
    # создаём пустой объект, который знает только одно - свой класс
    inst = CustomDict(
        __my_type__=cls,
        __my_dict__={},
    )

    # проходимся по перечню наших предков и вызываем __my_init__ если такой
    # метод есть хотя бы у одного из них
    for base_type in [cls, *cls['__my_bases__']]:
        if '__my_init__' in base_type['__my_dict__']:
            init = base_type['__my_dict__']['__my_init__']
            init(inst, *args, **kwargs)
            break

    # настоящий интерпретатор ещё проверяет, что __new__ вернул экземпляр
    # того же класса, что и изначально планировался. в противном случае
    # __init__ вызываться не будет

    return inst


# тут приходится применять небольшое читерство т.к. иначе не получится
# реализовать вызовы вида obj.attr. По факту это кастомный класс словаря,
# но т.к. проект подразумевался без применения ключевого  слова class,
# даже он тут создаётся странным образом :)
# настоящий словарь использовать нелья - не получится переопределить методы
# на этом этапе мы ещё пользуемся настоящим type, но скоро от него избавимся
CustomDict = type(
    'CustomDict',
    (dict,),
    {
        '__getattr__': __my_getattr__,
        '__call__': __my_call__,
    }
)


# noinspection PyShadowingBuiltins
def type(*args):
    """Собственная реализация type для вывода типа аргумента.

    Как и настоящий, возвращает существующий тип при одном
    аргументе и новый тип при трёх аргументах.
    """
    if len(args) == 1:
        return show_type(args[0])
    return make_type(*args)


def show_type(something):
    """Собственная реализация type для вывода типа аргумента.

    Немного отличается от настоящей. Тут надо бы вернуть класс, а не его имя,
    но у меня классы реализованы как словари, поэтому на экране будет
    всё его содерживое, что не очень удобно.
    """
    if '__my_name__' in something:
        return 'class ' + something['__my_name__']
    return 'inst of ' + something['__my_type__']['__my_name__']


def make_type(name: str, bases=None, attrs=None):
    """Собственный аналог type для создания экземпляра.

    Как и настоящий, принимает три аргумента: имя класса,
    перечень его родителей и набор его атрибутов.
    """
    return CustomDict(
        __my_name__=name,
        __my_bases__=bases or [],
        __my_dict__=attrs or {},
    )


# noinspection PyShadowingBuiltins
def isinstance(something: Any, some_type: CustomDict) -> bool:
    """Собственная реализация isinstance для проверки родства.
    """
    target_name = some_type['__my_name__']

    # возвращаем True если имя нашего класса совпадает с целевым
    if something['__my_type__']['__my_name__'] == target_name:
        return True

    # возвращаем True если целевое имя класса есть в наших предках
    # здесь не реализовано множественное наследование, поэтому
    # можно решить задачу простым перебором
    for base_class in something['__my_type__']['__my_bases__']:
        if target_name == base_class['__my_name__']:
            return True

    return False


# Выше находится внутренний код интерпретатора
# =============================================================================
# Ниже находится пользовательский код


def __my_init__(self, name: str) -> None:
    """Инициализировать экземпляр Animal.

    В данном случае мы присваиваем имя животного в собственный словарь.
    """
    self['__my_dict__']['name'] = name


def call(self, given_name: str) -> str:
    """Попытаться позвать животное.

    Животное отзовётся, если его зовут по имени.
    """
    if given_name == self['__my_dict__']['name']:
        return self.say()
    return 'no reaction'


# Базовый класс животного
# Не имеет ног, зато умеет реагировать если его позвать
# знает как обработать присвоение имени
Animal = type(
    'Animal',
    (),
    {
        '__my_init__': __my_init__,
        'call': call
    }
)

# Класс попугая
# Наследуется от Animal, имеет две ноги, кричит "Ара ара!"
Parrot = type(
    'Parrot',
    (Animal,),
    {
        'legs': 2,
        'say': lambda self: 'Ara! ara!',
    }
)

# Класс кота
# Наследуется от Animal, имеет четыре ноги, мяукает
Cat = type(
    'Cat',
    (Animal,),
    {
        'legs': 4,
        'say': lambda self: 'Meow!',
    }
)
