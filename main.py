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
import random

from pyrogram import Client, filters, enums
from pyrogram.handlers import MessageHandler
from pyrogram import types

from terminaltexteffects.effects.effect_rain import Rain
from terminaltexteffects.effects.effect_decrypt import Decrypt, DecryptConfig
import requests

import pyfiglet

from pyrogram.enums import ParseMode
from platform import python_version
from packaging import version as __version

from loads import Data
from handling_plugins import handling_plugins, handle_plugin
from __init__ import __version__ as this_version

logging.basicConfig(filename='script.log', level=logging.WARN)

# Чистка логов
if os.path.getsize('script.log') >= 1_048_576:
    with open('script.log', 'w') as f:
        pass

handling_plugins()

registers = {"classes": {}, "funcs": {}}

try:
    file = open("config.ini", "r").read()
    api_id = re.search('api_id\s*=\s*(\d+)', file)
    api_hash = re.search('api_hash\s*=\s*[\'"](.*?)[\'"]', file)
    send_msg_onstart_up = re.search('send_message\s*=\s*(true|false)', file)

    if send_msg_onstart_up is not None:
        send_msg_onstart_up = {'true': True, 'false': False}[send_msg_onstart_up.group(1)]
    else:
        send_msg_onstart_up = False

    phone_number = re.search('phone_number\s*=\s*(\d+)', file)
    password = re.search('password\s*=\s*[\'"](.*?)[\'"]', file)
except Exception as e:
    pass

there_is_update = False

app = Client(
            'db', api_id=api_id.group(1) if api_id is not None else None, api_hash=api_hash.group(1) if api_hash is not None else None,
            phone_number=phone_number.group(1) if phone_number is not None else None,
            password=password.group(1) if password is not None else None, max_concurrent_transmissions=20, workers=8
            )

def check_updates():
    global there_is_update
    # Ссылка на официальный источник, так что вирусов не должно быть, нужно детально проверять ссылку(так же самое и в плагинах)
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
        if not send_msg_onstart_up:
            DecryptConfig(1)

            effect = Decrypt('Доступно новое обновление!Введите в чате /update для обновления.')
            with effect.terminal_output() as terminal:
                for frame in effect:
                    terminal.print(frame)
        else:
            there_is_update = True
    
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

print(pyfiglet.figlet_format("ModuFlex", font=random.choice(pyfiglet.FigletFont.getFonts())))

def handling_updates():
    updates: dict = Data.cache

    with ThreadPoolExecutor(max_workers=10) as executor:
        for func in Data.initializations:
            executor.submit(func, app)

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

handling_updates()

@app.on_message(filters.command('help', ['.', '/', '!']) & filters.me)
async def help(_, msg: types.Message):
    help_text = ''

    await app.delete_messages(msg.chat.id, msg.id)

    if len(msg.text.split()) == 1:
        help_text = 'Список плагинов:\n'

        for indx, plugin in enumerate(Data.description):
            help_text += f'{indx+1}) <code>{plugin}</code>\n'

            if indx >= 30:
                break
        
        pages = len(Data.description)/30

        if pages > int(pages): pages = int(pages) + 1
        
        help_text += f'\n<b>Страница: 1/{pages}</b>' + '\n●Чтобы узнать о функции плагина, введите: /help {имя плагина}\n●Чтобы скачать плагин, введите: /dwlmd {ссылка на гит хаб зип файл}\n●Чтобы удалить плагин, введите: /rmmd {имя плагина}\n●Чтобы обновить скрипт, введите: /update\n●Чтобы переходить на страницу, введите: для плагинов: /help 2, для команд: /help имя_плагина 1'
    elif len(msg.text.split()) == 2 and msg.text.split()[1].isdigit():
        help_text = 'Список плагинов:\n'

        try:
            page = int(msg.text.split()[1])
        except ValueError as e:
            return await msg.edit('Неверный номер страницы')

        pages = len(Data.description)/30

        if pages > int(pages): pages = int(pages) + 1

        if page > pages:
            return await app.send_message(msg.chat.id, 'Кол-во заданных страниц выходит за границы доступного.')

        for indx, plugin in enumerate(Data.description):
            if indx < (page-1)*30:
                continue

            help_text += f'{indx+1}) <code>{plugin}</code>\n'

            if indx >= page*30:
                break
        
        help_text += f'\n<b>Страница: {page}/{pages}</b>' + '\n●Чтобы узнать о функции плагина, введите: /help {имя плагина}\n●Чтобы скачать плагин, введите: /dwlmd {ссылка на гит хаб зип файл}\n●Чтобы удалить плагин, введите: /rmmd {имя плагина}\n●Чтобы обновить скрипт, введите: /update\n●Чтобы переходить на страницу, введите: для плагинов: /help 2, для команд: /help имя_плагина 1'
    elif len(msg.text.split()) == 2:
        plugin = msg.text.split()[1]
        try:
            help_text = f'Описание плагина <code>{plugin}</code>:\n{dict(Data.description[plugin].__dict__)["main_description"].description}\n\nСписок функций плагина:\n'
        except KeyError:
            help_text = 'Плагин не найден'

        try:
            funcs = dict(Data.description[plugin].__dict__.items())['args_description']
        except KeyError:
            help_text = 'Плагин не найден'

        pages = len(funcs)/25

        if pages > int(pages): pages = int(pages) + 1

        i = 1
        try:
            for func in funcs:
                parameters = " ".join([" {" + parameter + "}" for parameter in func.parameters]) if func.parameters else ''
                help_text += f'<i>{i})</i> ' + '<b>{' + f'{", ".join(func.prefixes)}' + '}</b>' + f'<code>{func.command}</code>{parameters}{func.hyphen}{func.description}\n'
                i += 1

                if i == 25:
                    break
        except KeyError:
            help_text = 'Плагин не найден'
        
        help_text += f'\n<b>Страница: 1/{pages}</b>' + '\n●Чтобы переходить на страницу, введите: для плагинов: /help 2, для команд: /help имя_плагина 1\n<b>{...}</b> - доступные префиксы'
    elif len(msg.text.split()) == 3 and msg.text.split()[2].isdigit():
        plugin = msg.text.split()[1]
        try:
            help_text = f'Описание плагина <code>{plugin}</code>:\n{dict(Data.description[plugin].__dict__)["main_description"].description}\n\nСписок функций плагина:\n'
        except KeyError:
            help_text = 'Плагин не найден'

        try:
            page = int(msg.text.split()[2])
        except ValueError as e:
            return await msg.edit('Неверный номер страницы')
        
        try:
            funcs = dict(Data.description[plugin].__dict__.items())['args_description']

            pages = len(funcs)/25

            if pages > int(pages): pages = int(pages) + 1

            if page > pages:
                return await app.send_message(msg.chat.id, 'Кол-во заданных страниц выходит за границы доступного.')
        except KeyError:
            help_text = 'Плагин не найден'
            pages = 0

        i = 1
        try:
            for func in funcs:
                if i < (page-1)*25:
                    i += 1
                    continue

                parameters = " ".join([" {" + parameter + "}" for parameter in func.parameters]) if func.parameters else ''
                help_text += f'<i>{i})</i> ' + '<b>{' + f'{", ".join(func.prefixes)}' + '}</b>' + f'<code>{func.command}</code>{parameters}{func.hyphen}{func.description}\n'
                i += 1
                if i == page*25:
                    break
        except KeyError:
            help_text = 'Плагин не найден'
        
        help_text += f'\n<b>Страница: {page}/{pages}' + '</b>\n●Чтобы переходить на страницу, введите: для плагинов: /help 2, для команд: /help имя_плагина 1\n<b>{...}</b> - доступные префиксы'

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

    handle_plugin(file_name)

    await app.edit_message_text(msg.chat.id, msg.id, 'Плагин успешно установлен')

@app.on_message(filters.command('rmmd', ['.', '/', '!']) & filters.me)
async def remove_plugin(_, msg: types.Message):
    try:
        plugin_name = msg.text.split()[1]
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /rmmd {имя плагина}')
    
    if plugin_name not in Data.description:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Плагин не найден')

    if plugin_name in ['StartedPack', 'AnimationPack']:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Этот плагин не может быть удалён')
    
    os.remove(f'plugins/{plugin_name}')
    
    for plugin in Data.cache['funcs']:
        if Data.cache['funcs'][plugin]['PackName'] == plugin_name:
            Data.cache['funcs'].pop(plugin)
    
    Data.description.pop(plugin_name)

    await app.edit_message_text(msg.chat.id, msg.id, 'Плагин успешно удалён, перезапустите скрипт, чтобы он исчез окончательно')

@app.on_message(filters.command('update', ['.', '/', '!']) & filters.me)
async def update_script(_, msg: types.Message):
    await msg.edit('Проверка обновлений...')
    
    # Ссылка на официальный источник, так что вирусов не должно быть, нужно детально проверять ссылку(так же самое и в плагинах)
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

        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        for fl_name in _file_name:
            if fl_name == 'config.ini':
                continue

            if fl_name == 'plugins':
                shutil.copytree(f'temp/{file_name}/{fl_name}', os.path.join(script_dir, fl_name), dirs_exist_ok=True)
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

@app.on_message(filters.command('version', ['.', '/', '!']) & filters.me)
async def send_version(_, msg: types.Message):
    await app.send_message(msg.chat.id, f'Обновление: {"Есть" if there_is_update else "Нету"}\nТекущая версия: {this_version}')

@app.on_message()
async def all_messages(app: Client, message: types.Message):
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _func, value in Data.cache['funcs'].items():
            match value['type']:
                case 'default':
                    continue
                case 'private':
                    if str(message.chat.type) == "ChatType.PRIVATE":
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
                    if str(message.chat.type) == "ChatType.CHANNEL":
                        if inspect.iscoroutinefunction(value['func']):
                            asyncio.create_task(value['func'](app, message))
                        else:
                            executor.submit(value['func'], app, message)
                case 'all':
                    if inspect.iscoroutinefunction(value['func']):
                        asyncio.create_task(value['func'](app, message))
                    else:
                        executor.submit(value['func'], app, message)

async def main():
    if send_msg_onstart_up:
        await app.start()
        if there_is_update:
            await app.send_message('me', '👍Доступно новое обновление!', entities=[types.MessageEntity(type=enums.MessageEntityType.CUSTOM_EMOJI, offset=0, length=2, custom_emoji_id=6327717992268301521)])
        # Увы, юзерам такое отправлять нельзя(
        msg = await app.send_message('me', '👍Юзер бот запущен', entities=[types.MessageEntity(type=enums.MessageEntityType.CUSTOM_EMOJI, offset=0, length=2, custom_emoji_id=random.choice([
            6204226842010847828,
            6325468301283558870,
            6203811806436132645,
            6206350076273494131,
            5384064740479747298,
            5456188142006575553,
            5456254812783910040,
            5244469322583120930
        ]))])
    
    await asyncio.sleep(30)

    try:
        await msg.delete()
    except:
        pass

    await asyncio.Event().wait()

if __name__ == '__main__':
    if not send_msg_onstart_up:
        effect = Rain('Скрипт запущен, подождите 5 секунд\nПриятного использования!')
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)
    
    app.run(main())
