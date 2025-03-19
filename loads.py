from typing import Type, Callable, Union
import inspect
from pyrogram import filters
from pyrogram.filters import command
import os
import importlib.util
import subprocess

__all__ = [
    'Data',
    'func',
    'private_func',
    'chat_func',
    'channel_func',
    'all_func',
    'set_modules',
    'MainDescription',
    'FuncDescription',
    'Description'
]

# client = redis.Redis()

# def cls(cls: Type) -> None:
#     clses: dict = json.loads(client.get('handlers'))
#     clses['classes'].update({cls.__name__: {"class": cls, "methods": []}})
#     client.set('handlers', str(clses))

# def func(func: Callable[..., Any]) -> Callable:
#     def wrapper(command: str):
#         funcs: dict = json.loads(client.get('handlers'))

#         if inspect.isfunction(func):
#             funcs['funcs'].update({func.__name__: {"func": func, "command": command}})
#             client.set('handlers', json.dumps(funcs))
#         elif inspect.ismethod(func):
#             class_name = func.__self__.__class__
#             funcs['classes'][class_name]['methods'].append({"method_name": func.__name__, "command": command})
#             client.set('handlers', json.dumps(funcs))
#     return wrapper

class Data:
    cache = {
        "funcs": {},
        "classes": {}
    }

    description = {}

    modules = []

    initializations = []

    @classmethod
    def get_name_plugins() -> list[str]:
        return list(Data.description.keys())

def func(_filters: filters) -> Callable:
    """
    Декоратор для обработки сообщений.
    :param _filters: фильтры pyrogram`a
    :return: Callable
    """
    def reg(_func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not a function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename
        
        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        Data.cache['funcs'].update({_func.__name__: {"func": _func, "filters": _filters, "PackName": pack_name, "type": "default"}})
    return reg

def private_func() -> Callable:
    """
    Декоратор для обработки сообщений в личном чате.
    Не имеет параметров.
    :return: Callable
    """
    def reg(func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not a function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename

        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        Data.cache['funcs'].update({func.__name__: {"func": func, "PackName": pack_name, "type": "private"}})
    return reg

def chat_func() -> Callable:
    """
    Декоратор для обработки сообщений в чате.
    Не имеет параметров.
    :return: Callable
    """
    def reg(func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not a function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename

        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        Data.cache['funcs'].update({func.__name__: {"func": func, "PackName": pack_name, "type": "chat"}})
    return reg

def channel_func() -> Callable:
    """
    Декоратор для обработки сообщений в канале чате.
    Не имеет параметров.
    :return: Callable
    """
    def reg(func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not a function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename

        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        Data.cache['funcs'].update({func.__name__: {"func": func, "PackName": pack_name, "type": "channel"}})
    return reg

def all_func() -> Callable:
    """
    Декоратор для обработки сообщений по всему чату.
    Не имеет параметров.
    :return: Callable
    """
    def reg(func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not a function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename

        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        Data.cache['funcs'].update({func.__name__: {"func": func, "PackName": pack_name, "type": "all"}})
    return reg

def set_modules(modules: list) -> None:
    """
    Функция для указания сторонних библиотек.
    Вызывать перед импортами сторонних библиотек.
    :param modules: список сторонних библиотек
    :return: None
    """

    for indx, module in enumerate(modules.copy()):
        if module in Data.modules:
            try:
                modules.pop(indx)
            except IndexError:
                pass

    for module in modules:
        if importlib.util.find_spec(module) is None:
            subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    Data.modules.extend(modules)

class MainDescription:
    """
    Класс для описания плагина.
    """
    def __init__(self, description: str) -> None:
        self.description = description

class FuncDescription:
    """
    Класс для описания функций плагина.
    """
    def __init__(self, command: str, description: str, hyphen: str=' - ', prefixes: Union[tuple, list]=['/'], parameters: Union[tuple, list]=[]) -> None:
        """
        `command`: команда(без префикса)
        `description`: описание команды
        `hyphen`: символы между команды и описания
        `prefixes`: префиксы команды(по умолчанию /)
        `parameters`: параметры команды
        """
        self.command = command
        self.description = description
        self.hyphen = hyphen
        self.prefixes = prefixes
        self.parameters = parameters

class Description:
    """
    Класс для описания плагина и его функций.
    """
    def __init__(self, main_description: MainDescription, *args: FuncDescription):
        self.main_description = main_description
        self.args_description = args