import importlib.util
import subprocess

from __init__ import __modules__, __version__ as _version_

if importlib.util.find_spec('alive_progress') is None:
    subprocess.run(['pip', 'install', 'alive-progress'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from alive_progress import alive_it, styles

for module in alive_it(__modules__, title='Проверка модулей', spinner=styles.SPINNERS['pulse'], theme='smooth'):
    if importlib.util.find_spec(module) is not None:
        continue
    subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import zipfile
import shutil
import os

import re
import inspect
from concurrent.futures import ThreadPoolExecutor

import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram import types

from terminaltexteffects.effects.effect_rain import Rain
from terminaltexteffects.effects.effect_decrypt import Decrypt, DecryptConfig
import requests

from pyrogram.enums import ParseMode
from platform import python_version
from packaging import version as __version

from loads import Data
from handling_plugins import handling_plugins
from __init__ import __version__ as this_version

logging.basicConfig(filename='script.log', level=logging.DEBUG)

handling_plugins()

registers = {"classes": {}, "funcs": {}}
#structure
#registers: {"classes": {{"name": {"class": classObject, "methods": [{"method_name": methodName, "filters": pyrogram.filters}]}}}, "funcs": {"name": {"func": funcObject, "filters": pyrogram.filters}}}

try:
    file = open("config.ini", "r").read()
    api_id = re.search('api_id\s*=\s*(\d+)', file)
    api_hash = re.search('api_hash\s*=\s*[\'"](.*?)[\'"]', file)

    phone_number = re.search('phone_number\s*=\s*(\d+)', file)
    password = re.search('password\s*=\s*[\'"](.*?)[\'"]', file)
except Exception as e:
    pass

app = Client(
            'db', api_id=api_id.group(1), api_hash=api_hash.group(1),
            phone_number=phone_number.group(1) if phone_number is not None else None,
            password=password.group(1) if password is not None else None
            )

def check_updates():
    # Ссылка на оффициальный источник, так что вирусов не должно быть, нужно детально проверять ссылку(так же самое и в плагинах)
    link = 'https://github.com/flexyyyapk/userbotmynew/archive/refs/heads/main.zip'

    with open(f'temp/main.zip', 'wb') as f:
        with requests.get(link, stream=True) as r:
            for chunk in alive_it(r.iter_content(chunk_size=512), title='Проверка обновления', spinner=styles.SPINNERS['pulse'], theme='smooth'):
                f.write(chunk)
    
    with zipfile.ZipFile(f'temp/main.zip', 'r') as zip_ref:
        zip_ref.extractall('temp')
    
    file_name = os.listdir('temp')

    for fil_name in file_name:
        if os.path.isdir('temp/'+fil_name):
            file_name = fil_name
            break
    
    version = __import__(f'temp.{file_name}.__init__', fromlist=['__version__']).__version__

    if version != _version_:
        DecryptConfig(50)

        effect = Decrypt('Доступно новое обновление!Введите в чате /update для обновления.')
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)
    
    for fil_name in os.listdir('temp'):
        try:
            if os.path.isdir('temp/'+fil_name):
                shutil.rmtree('temp/'+fil_name)
                continue

            os.remove('temp/'+fil_name)
        except OSError:
            pass
        
        except Exception as e:
            print(e)

check_updates()

def handling_updates():
    modules = Data.modules
    for module in alive_it(modules, title='Проверка модулей', spinner=styles.SPINNERS['pulse'], theme='smooth'):
        if importlib.util.find_spec(module) is None:
            subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    updates: dict = Data.cache

    # Не работает!
    # for update in updates['classes']:
    #     if update in registers['classes']:
    #         _method_name = updates['classes'][update][0]['method_name']
    #         command = updates['classes'][update]['command']
    #         for _methods in registers['classes'][update]['methods']:
    #             if _methods['method_name'] == _method_name:
    #                 break
    #         else:
    #             registers['classes'][update]['methods'].append({"method_name": _method_name, "command": command})
    #             continue

    #     _class = updates['classes'][update]['class']
    #     _method_name = updates['classes'][update]['method_name']
    #     command = updates['classes'][update]['command']

    #     _handle = getattr(_class, _method_name, None)
    #     if _handle is not None:
    #         registers['classes'].update(updates['classes'])
    #         app.add_handler(MessageHandler(_handle, filters.command(command)))

    for update in updates['funcs']:
        if registers['funcs'].get(update, False):
            continue
        
        registers['funcs'].update({update: updates['funcs'][update]})

        if updates['funcs'][update]['type'] != 'default':
            continue

        app.add_handler(MessageHandler(updates['funcs'][update]['func'], updates['funcs'][update]['filters']))
    
    if modules != Data.modules:
        modules = Data.modules
        for module in alive_it(modules, title='Найден новый модуль', spinner=styles.SPINNERS['pulse'], theme='smooth'):
            if importlib.util.find_spec(module) is None:
                subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

handling_updates()

@app.on_message(filters.command('help', ['.', '/', '!']) & filters.me)
async def help(_, msg: types.Message):
    help_text = ''

    await app.delete_messages(msg.chat.id, msg.id)

    if len(msg.text.split()) == 1:
        help_text = 'Список плагинов:\n'

        i = 1
        for plugin in Data.description:
            help_text += f'{i}) <code>{plugin}</code>\n'
            i += 1
        
        help_text += '\nЧтобы узнать о функции плагина, введите: /help {имя плагина}\nЧтобы скачать плагин, введите: /dwlmd {ссылка на гит хаб зип файл}\nЧтобы удалить плагин, введите: /rmmd {имя плагина}'
    elif len(msg.text.split()) == 2:
        plugin = msg.text.split()[1]
        help_text = f'Описание плагина <code>{plugin}</code>:\n{dict(Data.description[plugin].__dict__)["main_description"].description}\n\nСписок функций плагина:\n'

        i = 1
        try:
            for func in dict(Data.description[plugin].__dict__.items())['args_description']:
                help_text += f'{i}) {func.command} - {func.description}\n'
                i += 1
        except KeyError:
            help_text = 'Плагин не найден'

    while len(help_text) > 4096:
        await app.send_message(msg.chat.id, help_text[:4096])
        help_text = help_text[4096:]

    if help_text:
        await app.send_message(msg.chat.id, help_text)

@app.on_message(filters.command('dwlmd', ['.', '/', '!']) & filters.me)
async def download_module(_, msg: types.Message):
    await app.edit_message_text(msg.chat.id, msg.id, 'Загрузка...')

    try:
        link = msg.text.split()[1]
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /dwlmd {ссылка на зип из гит хаба}')
    
    if 'https://github.com/' not in link or not link.endswith('.zip'):
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /dwlmd {ссылка на зип из гит хаба}')
    
    file_name = link.split("/")[-1][:-4]
    
    with open(f'plugins/{file_name}.zip', 'wb') as f:
        with requests.get(link, stream=True) as r:
            for chunk in alive_it(r.iter_content(chunk_size=512), title='Загрузка модуля', spinner=styles.SPINNERS['pulse'], theme='smooth'):
                f.write(chunk)
    
    os.makedirs('plugins/temp', exist_ok=True)
    
    with zipfile.ZipFile(f'plugins/{file_name}.zip', 'r') as zip_ref:
        zip_ref.extractall('plugins/temp')
    
    file_name = os.listdir('plugins/temp')[0]

    for fl_name in os.listdir(f'plugins/temp/{file_name}'):
        shutil.move(f'plugins/temp/{file_name}/{fl_name}', f'plugins/{fl_name}')

    shutil.rmtree('plugins/temp')

    os.remove(f'plugins/{file_name}.zip')

    await app.edit_message_text(msg.chat.id, msg.id, 'Плагин успешно установлен')

@app.on_message(filters.command('rmmd', ['.', '/', '!']) & filters.me)
async def remove_plugin(_, msg: types.Message):
    try:
        plugin_name = msg.text.split()[1]
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /rmmd {имя плагина}')
    
    if plugin_name not in Data.description:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Плагин не найден')

    if plugin_name == 'StartedPack':
        return await app.edit_message_text(msg.chat.id, msg.id, 'Этот плагин не может быть удалён')
    
    os.remove(f'plugins/{plugin_name}')
    
    for plugin in Data.cache['funcs']:
        if Data.cache['funcs'][plugin]['PackName'] == plugin_name:
            Data.cache['funcs'].pop(plugin)
    
    Data.description.pop(plugin_name)

    await app.edit_message_text(msg.chat.id, msg.id, 'Плагин успешно удалён')

@app.on_message(filters.command('update', ['.', '/', '!']) & filters.me)
async def update_script(_, msg: types.Message):
    await msg.edit('Проверка обновлений...')
    
    # Ссылка на оффициальный источник, так что вирусов не должно быть, нужно детально проверять ссылку(так же самое и в плагинах)
    link = 'https://github.com/flexyyyapk/userbotmynew/archive/refs/heads/main.zip'

    with open(f'temp/main.zip', 'wb') as f:
        with requests.get(link, stream=True) as r:
            for chunk in alive_it(r.iter_content(chunk_size=512), title='Загрузка обновления', spinner=styles.SPINNERS['pulse'], theme='smooth'):
                f.write(chunk)
    
    with zipfile.ZipFile(f'temp/main.zip', 'r') as zip_ref:
        zip_ref.extractall('temp')
    
    file_name = os.listdir('temp')

    for fil_name in file_name:
        if os.path.isdir('temp/'+fil_name):
            file_name = fil_name
            break

    _file_name = os.listdir(f'temp/{file_name}')
    
    if (version := __import__(f'temp.{file_name}.__init__', fromlist=['__version__', '__modules__'])).__version__ != this_version:
        if not __version.parse(python_version()) >= __version.parse('3.8'):
            return await msg.edit('Обновление найдено, но версия интерпретатора не подходит(требуется 3.8 и больше)')

        await msg.edit(f'Обновление найдено, версия: {version.__version__}, установка...')

        await asyncio.sleep(0.5)

        for module in alive_it(version.__modules__, title='Установка модулей', spinner=styles.SPINNERS['pulse'], theme='smooth'):
            if importlib.util.find_spec(module) is not None:
                continue
            subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for fl_name in _file_name:
            if fl_name == 'config.ini':
                continue
        
            if fl_name == 'plugins':
                continue

            shutil.move(f'temp/{file_name}/{fl_name}', f'{fl_name}')

        for fil_name in os.listdir('temp'):
            try:
                if os.path.isdir('temp/'+fil_name):
                    shutil.rmtree('temp/'+fil_name)
                    continue

                os.remove('temp/'+fil_name)
            except OSError:
                pass
            
            except Exception as e:
                print(e)

        await msg.edit(f'Обновление успешно установлено\n{version.__news__}', parse_mode=ParseMode.HTML)
    else:
        await msg.edit('Обновление не найдено')

@app.on_message()
async def all_messages(app: Client, message: types.Message):
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _func, value in Data.cache['funcs'].items():
            match value['type']:
                case 'default':
                    continue
                case 'private':
                    if str(message.chat.type) == 'ChatType.PRIVATE':
                        if inspect.iscoroutinefunction(value['func']):
                            asyncio.create_task(value['func'](app, message))
                        else:
                            executor.submit(value['func'], app, message)
                case 'chat':
                    if str(message.chat.type) in ['ChatType.GROUP', 'ChatType.SUPERGROUP']:
                        if inspect.iscoroutinefunction(value['func']):
                            asyncio.create_task(value['func'](app, message))
                        else:
                            executor.submit(value['func'], app, message)
                case 'channel':
                    if str(message.chat.type) == 'ChatType.CHANNEL':
                        if inspect.iscoroutinefunction(value['func']):
                            asyncio.create_task(value['func'](app, message))
                        else:
                            executor.submit(value['func'], app, message)
                case 'all':
                    if inspect.iscoroutinefunction(value['func']):
                        asyncio.create_task(value['func'](app, message))
                    else:
                        executor.submit(value['func'], app, message)

if __name__ == '__main__':
    effect = Rain('Скрипт запущен, подождите 5 секунд\nПриятного использования!')
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

    app.run()