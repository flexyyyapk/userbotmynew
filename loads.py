from typing import Type, Callable, Union, Optional, List, Type
import inspect
from pyrogram import filters
import os
import importlib.util
import subprocess
import logging
import traceback

logging.basicConfig(filename='script.log', level=logging.WARN)

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
    'Description',
    'handleMethods'
]

CONFLICTS = [
    filters.all,
    filters.private,
    filters.channel,
    filters.group
]

class Data:
    """
    Центр хранения модулей.
    """

    cache = {

    }

    description = {}

    modules = []

    initializations = []

    @classmethod
    def get_name_plugins() -> list[str]:
        return list(Data.description.keys())

class chatType:
    DEFAULT = "default"
    PRIVATE = "private"
    CHAT = "chat"
    CHANNEL = "channel"
    ALL = "all"

def func(_filters: filters) -> Callable:
    """
    Декоратор для обработки сообщений.
    :param _filters: фильтры pyrogram`a
    :return: Callable
    """
    def reg(_func: Callable) -> None:
        if not inspect.isfunction(_func):
            raise ValueError('Is not a function')

        if __find_conflict__(_filters):
            raise ValueError('Filters has a conflict filter')
        
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename
        
        path_parts = os.path.normpath(caller_filename).split(os.sep)
        pack_name = path_parts[path_parts.index('plugins') + 1]

        prefixes = __find_command__(_filters)

        Data.cache[pack_name]['funcs'].update({_func.__name__: {"func": _func, "filters": _filters, "prefixes": prefixes, "type": "default"}})
    return reg

def private_func() -> Callable:
    """
    Декоратор для обработки сообщений в личном чате.
    Не имеет параметров.
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

        Data.cache[pack_name]['funcs'].update({_func.__name__: {"func": _func, "filters": None, "prefixes": None, "type": "private"}})
    return reg

def chat_func() -> Callable:
    """
    Декоратор для обработки сообщений в чате.
    Не имеет параметров.
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

        Data.cache[pack_name]['funcs'].update({_func.__name__: {"func": _func, "filters": None, "prefixes": None, "type": "chat"}})
    return reg

def channel_func() -> Callable:
    """
    Декоратор для обработки сообщений в канале чате.
    Не имеет параметров.
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

        Data.cache[pack_name]['funcs'].update({_func.__name__: {"func": _func, "filters": None, "prefixes": None, "type": "channel"}})
    return reg

def all_func() -> Callable:
    """
    Декоратор для обработки сообщений по всему чату.
    Не имеет параметров.
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

        Data.cache[pack_name]['funcs'].update({_func.__name__: {"func": _func, "filters": None, "prefixes": None, "type": "all"}})
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

def __find_command__(_filters: filters) -> Optional[List[str]]:
    if type(_filters).__name__ == 'CommandFilter':
        if isinstance(_filters.prefixes, list): return _filters.prefixes
        else: return list(_filters.prefixes)
    
    if type(_filters.__dict__['other']).__name__ == 'CommandFilter':
        if isinstance(_filters.__dict__['other'].prefixes, list): return _filters.__dict__['other'].prefixes
        else: return list(_filters.__dict__['other'].prefixes)
    elif type(_filters.__dict__['base']).__name__ == 'CommandFilter':
        if isinstance(_filters.__dict__['base'].prefixes, list): return _filters.__dict__['other'].prefixes
        else: return list(_filters.__dict__['base'].prefixes)
    elif type(_filters.__dict__['base']).__name__ in ['AndFilter', 'OrFilter']:
        return __find_command__(_filters.__dict__['base'])
    else:
        return None

def __find_conflict__(_filters: filters) -> bool:
    if _filters == None:
        return False
    
    if any(_filters == conflict for conflict in CONFLICTS):
        return True
    elif not dict(_filters.__dict__).get('base', False):
        return False

    if any(_filters.__dict__['base'] == conflict for conflict in CONFLICTS):
        return True
    elif any(_filters.__dict__['other'] == conflict for conflict in CONFLICTS):
        return True
    elif type(_filters.__dict__['base']).__name__ in ['AndFilter', 'OrFilter']:
        return __find_conflict__(_filters.__dict__['base'])
    else:
        return False