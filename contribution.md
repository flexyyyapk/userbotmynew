На данный момент проект ещё сырой, но он полон надежд и успехов

## Начало

Начнём с того, что создадим папку в файле plugins, название любое.

Создаём файл \_\_init\_\_.py (без \\)

И можем начать писать плагин!

## Регистрация

```python
from loads import func
#Декоратор для регистрации функции
from pyrogram import filters

@func(filters.command('start'))
async def test(client, message):
	#client: объект класса pyrogram.Client
	#message: объект класса pyrogram.types.Message
	await client.send_message(message.chat.id, 'test')
```

В теории можно делать и синхронные функции(но это в теории...)

Также можно указать несколько фильтров как и в pyrogram

```python
from loads import func
#Декоратор для регистрации функции
from pyrogram import filters

@func(filters.command('start') & filters.me)
async def test(client, message):
	#client: объект класса pyrogram.Client
	#message: объект класса pyrogram.types.Message
	await client.send_message(message.chat.id, 'test')
```

## Описания и модули

Чтобы пользователь смог изучить и использовать команды, нужно описать плагин:

```python
from loads import func, Description, MainDescription, FuncDescription

__description__ = Description(
	MainDescription('Описания плагина'),
	FuncDescription('команда', 'описание команды'),
	FuncDescription('...', '...')
)

#MainDescription используется для описания плагина
#FuncDescription используется чтобы описать команду
```

Также, если вы делаете плагин с другими сторонними модулями(библиотеками), скорее всего у пользователя его не будет, по этому, чтобы обойти ошибки/баги стороной, нужно написать список:

```python-repl
__modules__ = ['модуль1', 'модуль2']
```

## Скачивания плагина и запуск

Чтобы скачать плагин, вам нужно __запустить юзер бота, т.е файл main.py.__

Затем в каком то из чатов написать /dwlmd {ссылка на зип файл из гит хаба}
