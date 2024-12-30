# import redis
# import json
from typing import Type, Callable, Any, List
import inspect
from pyrogram import filters

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

def func(_filters: filters) -> None:
    def reg(func: Callable) -> None:
        if not inspect.isfunction(func):
            raise ValueError('Is not function')

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_filename = caller_frame.f_code.co_filename

        Data.cache['funcs'].update({func.__name__: {"func": func, "filters": _filters, "PackName": caller_filename.split('\\')[-2]}})
    return reg

class MainDescription:
    """
    Класс для описания плагина
    """
    def __init__(self, description: str) -> None:
        self.description = description

class FuncDescription:
    """
    Класс для описания функций плагина
    """
    def __init__(self, command: str, description: str) -> None:
        self.command = command
        self.description = description

class Description:
    """
    Класс для описания плагина и его функций
    """
    def __init__(self, main_description: MainDescription, *args: FuncDescription):
        self.main_description = main_description
        self.args_description = args