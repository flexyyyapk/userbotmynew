import subprocess
import importlib
from alive_progress import alive_it, styles

for module in alive_it(['pyrogram', 'terminaltexteffects'], title='Проверка модулей', spinner=styles.SPINNERS['pulse'], theme='smooth'):
    if importlib.util.find_spec(module) is not None:
        continue
    subprocess.run(f'pip install {module}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram import types
import asyncio
from loads import Data
from handling_plugins import handling_plugins
from terminaltexteffects.effects.effect_rain import Rain
import requests
import zipfile
import shutil
import os
import re
from __init__ import __version__ as this_version
from pyrogram.enums import ParseMode

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

app = Client('db', api_id=api_id.group(1), api_hash=api_hash.group(1), phone_number=phone_number.group(1) if phone_number is not None else None, password=password.group(1) if password is not None else None)

async def handling_updates():
    modules = Data.modules
    for module in modules:
        if importlib.util.find_spec(module) is None:
            subprocess.run(f'pip install {module}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    while True:
        updates: dict = Data.cache

        for update in updates['classes']:
            if update in registers['classes']:
                _method_name = updates['classes'][update][0]['method_name']
                command = updates['classes'][update]['command']
                for _methods in registers['classes'][update]['methods']:
                    if _methods['method_name'] == _method_name:
                        break
                else:
                    registers['classes'][update]['methods'].append({"method_name": _method_name, "command": command})
                    continue

            _class = updates['classes'][update]['class']
            _method_name = updates['classes'][update]['method_name']
            command = updates['classes'][update]['command']

            _handle = getattr(_class, _method_name, None)
            if _handle is not None:
                registers['classes'].update(updates['classes'])
                app.add_handler(MessageHandler(_handle, filters.command(command)))

        for update in updates['funcs']:
            if update in registers['funcs']:
                continue
            
            registers['funcs'].update(updates['funcs'][update])
            app.add_handler(MessageHandler(updates['funcs'][update]['func'], updates['funcs'][update]['filters']))
        
        if modules != Data.modules:
            modules = Data.modules
            for module in modules:
                if importlib.util.find_spec(module) is None:
                    subprocess.run(f'pip install {module}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        await asyncio.sleep(1)

asyncio.get_event_loop().create_task(handling_updates())

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
        
        help_text += '\nЧтобы узнать о функций плагина, введите: /help {имя плагина}\nЧтобы скачать плагин, введите: /dwlmd {ссылка на гит хаб зип файл}\nЧтобы удалить плагин, введите: /rmmd {имя плагина}'
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
    _file_name = os.listdir(f'plugins/temp/{file_name}')

    for fl_name in _file_name:
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
    
    #Ссылка на оффициальный источник, так что вирусов не должно быть, нужно детально проверять ссылку(так же самое и в плагинах)
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

    version = __import__(f'temp.{file_name}.__init__', fromlist=['__version__'])
    
    try:
        if version.__version__ != this_version:
            await msg.edit('Доступное обновление найдено, установка...')
    
            for fl_name in _file_name:
                if fl_name == 'config.ini':
                    continue
            
                if fl_name == 'plugins':
                    continue
    
                shutil.move(f'temp/{file_name}/{fl_name}', f'{fl_name}')
            
            os.remove('temp/main.zip')
            os.remove('temp/'+file_name)
            os.remove('temp/temp')
    
            await msg.edit('Обновление успешно установлено')
        else:
            await msg.edit('Обновление не найдено')
    except Exception as e:
        await msg.edit(f'Обновление успешно установлено\n{version.__news__}', parse_mode=ParseMode.HTML)

effect = Rain('Скрипт запущен\nПриятного использования!')
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)

app.run()
