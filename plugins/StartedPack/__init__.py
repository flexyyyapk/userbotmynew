from loads import func, MainDescription, FuncDescription, Description
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio
import random
import wikipedia
from googletrans import Translator, constants
import json
from gtts import gTTS
from io import BytesIO

wikipedia.set_lang('ru')

__description__ = Description(
    MainDescription("Основной плагин для работы с юзер ботом"),
    FuncDescription('/spam {кол-во} {текст}', 'Спамит текст кол-во раз'),
    FuncDescription('/ispam {интервал} {кол-во} {текст}', 'Спамит текст с интервалом'),
    FuncDescription('/rd {нижняя граница} {верхняя граница}', 'Рандомно выбирает число из диапазона'),
    FuncDescription('/rt {текст},{текст2},{текст3}', 'Рандомно выбирает текст из списка'),
    FuncDescription('/calc {выражение}', 'Вычисляет математическое выражение'),
    FuncDescription('/wiki {текст}', 'Ищет текст в википедии'),
    FuncDescription('/tr {с} {на} {текст}', 'Переводит текст на выбранный язык'),
    FuncDescription('/lg_list', 'Выводит в консоль список языков для перевода'),
    FuncDescription('/tts {текст}', 'Преобразует текст в аудио'),
    FuncDescription('/info', 'Выводит информацию о пользователе или чате'),
    FuncDescription('/love', 'Выводит анимацию с сердечками'),
    FuncDescription('/t {текст}', 'Анимация печатания в чате'),
    FuncDescription('/proc {текст1},{текст2}', 'Анимация загрузки в чате'),
    FuncDescription('/tanos', 'Называет все имена в группе и добавляет к ним слово "изчес"'),
    FuncDescription('/ex', 'Показывает текст "Правда" или "Ложь"'),
    FuncDescription('/dc', 'Выводит случайно "Чист" или "Заражён"'),
    FuncDescription('/ghoul', 'Показывает таблицу где отнимают 7 от 1000'),
    FuncDescription('/ocase {необязательно(кол-во прокрутки)}', 'Анимация прокрутки "кейса" в чате'),
    FuncDescription('/clown', 'Воспроизводит анимацию, которая адресуется тем, кто позер и прочее')
)
#__description__ описывает плагин и его функции

__modules__ = ['wikipedia', 'googletrans', 'gtts']
#__modules__ модули которые нужно установить

@func(filters.command('spam') & filters.me)
async def spam(app: Client, msg: Message):
    try:
        count = int(msg.text.split()[1])
        text = ' '.join(msg.text.split()[2:])
    except (ValueError, IndexError):
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /spam 1 текст')

    for _ in range(count):
        try:
            await app.send_message(msg.chat.id, text)
        except FloodWait as e:
            count += 1
            await asyncio.sleep(e.value)

@func(filters.command('ispam') & filters.me)
async def interval_spam(app: Client, msg: Message):
    try:
        interval = int(msg.text.split()[1])
        count = int(msg.text.split()[2])
        text = ' '.join(msg.text.split()[3:])
    except (ValueError, IndexError):
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /ispam 10 1 текст')

    for _ in range(count):
        try:
            await app.send_message(msg.chat.id, text)
            await asyncio.sleep(interval)
        except FloodWait as e:
            count += 1
            await asyncio.sleep(e.value)

@func(filters.command('rd') & filters.me)
async def random_digits(app: Client, msg: Message):
    try:
        value1 = int(msg.text.split()[1])
        value2 = int(msg.text.split()[2])
    except ValueError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /rd 10 100')
    
    await app.edit_message_text(msg.chat.id, msg.id, str(random.randint(value1, value2)))

@func(filters.command('rt') & filters.me)
async def random_text(app: Client, msg: Message):
    try:
        texts = ' '.join(msg.text.split()[1:]).split(',')
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /rt текст1,текст2,текст3')

    await app.edit_message_text(msg.chat.id, msg.id, random.choice(texts))

@func(filters.command('calc') & filters.me)
async def calculator(app: Client, msg: Message):
    try:
        expression = ' '.join(msg.text.split()[1:])
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /calc 1+1')

    for exp in expression:
        if exp not in '0123456789+-*/() ':
            return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /calc 1+1')

    await app.edit_message_text(msg.chat.id, msg.id, str(eval(expression)))

@func(filters.command('wiki') & filters.me)
async def wikipedia_search(app: Client, msg: Message):
    await app.edit_message_text(msg.chat.id, msg.id, 'Поиск...')

    try:
        query = ' '.join(msg.text.split()[1:])
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /wiki текст')

    try:
        result = wikipedia.summary(query, sentences=4095)
    except wikipedia.exceptions.DisambiguationError as e:
        options = '\n'.join(str(i) + option for i, option in enumerate(e.options, start=1))
        return await app.edit_message_text(msg.chat.id, msg.id, f'Найдено несколько результатов. Выберите один из них:\n{options}')
    except wikipedia.exceptions.PageError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Страница не найдена.')

    await app.edit_message_text(msg.chat.id, msg.id, result)

@func(filters.command('tr') & filters.me)
async def translate(app: Client, msg: Message):
    try:
        dest = msg.text.split()[1]
        src = msg.text.split()[2]
        text = ' '.join(msg.text.split()[3:])
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /tr {с} {на} {текст}')
    except ValueError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели язык.Пример: /tr ru en текст')
    
    trans = Translator()
    result = trans.translate(text, src, dest)
    await app.edit_message_text(msg.chat.id, msg.id, result.text)

@func(filters.command('lg_list') & filters.me)
async def language_list(app: Client, msg: Message):

    await app.edit_message_text(msg.chat.id, msg.id, 'Список языков выведен в терминал')

    print(json.dumps(constants.LANGUAGES, indent=4))

@func(filters.command('tts') & filters.me)
async def text_to_speech(app: Client, msg: Message):
    await app.delete_messages(msg.chat.id, msg.id)
    
    try:
        text = ' '.join(msg.text.split()[1:])
    except IndexError:
        return await app.edit_message_text(msg.chat.id, msg.id, 'Вы не верно ввели параметры.Пример: /tts текст')

    tts = gTTS(text, lang='ru')
    
    audio = BytesIO()
    audio.name = 'audio.ogg'

    tts.write_to_fp(audio)
    audio.seek(0)

    await app.send_audio(msg.chat.id, audio)

@func(filters.command('info') & filters.me)
async def info(app: Client, msg: Message):
    if msg.reply_to_message:
        user = msg.reply_to_message.from_user

        await app.edit_message_text(msg.chat.id, msg.id, f'Информация о пользователе:\nID: {user.id}\nИмя: {user.first_name}\nНикнейм: {user.username}\nАктивность: {user.status}')
    else:
        await app.edit_message_text(msg.chat.id, msg.id, f'Информация о чате:\nID: {msg.chat.id}\nТип: {msg.chat.type}')

@func(filters.command('love') & filters.me)
async def love_animation(_, msg):
   try:
      await msg.edit("""❤️""")
      await asyncio.sleep(0.1)
      await msg.edit("""🧡""")
      await asyncio.sleep(0.1)
      await msg.edit("""💛""")
      await asyncio.sleep(0.1)
      await msg.edit("""💚""")
      await asyncio.sleep(0.1)
      await msg.edit("""💙""")
      await asyncio.sleep(0.1)
      await msg.edit("""💜""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤎""")
      await asyncio.sleep(0.1)
      await msg.edit("""🖤""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤍""")
      await asyncio.sleep(0.1)
      await msg.edit("""❤️❤️
❤️❤️""")
      await asyncio.sleep(0.1)
      await msg.edit("""🧡🧡
🧡🧡""")
      await asyncio.sleep(0.1)
      await msg.edit("""💛💛
💛💛""")
      await asyncio.sleep(0.1)
      await msg.edit("""💚💚
💚💚""")
      await asyncio.sleep(0.1)
      await msg.edit("""💙💙
💙💙""")
      await asyncio.sleep(0.1)
      await msg.edit("""💜💜
💜💜""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤎🤎
🤎🤎""")
      await asyncio.sleep(0.1)
      await msg.edit("""🖤🖤
🖤🖤""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤍🤍
🤍🤍""")
      await asyncio.sleep(0.1)
      await msg.edit("""❤️❤️❤️
❤️❤️❤️
❤️❤️❤️""")
      await asyncio.sleep(0.1)
      await msg.edit("""🧡🧡🧡
🧡🧡🧡
🧡🧡🧡""")
      await asyncio.sleep(0.1)
      await msg.edit("""💛💛💛
💛💛💛
💛💛💛""")
      await asyncio.sleep(0.1)
      await msg.edit("""💚💚💚
💚💚💚
💚💚💚""")
      await asyncio.sleep(0.1)
      await msg.edit("""💙💙💙
💙💙💙
💙💙💙""")
      await asyncio.sleep(0.1)
      await msg.edit("""💜💜💜
💜💜💜
💜💜💜""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤎🤎🤎
🤎🤎🤎
🤎🤎🤎""")
      await asyncio.sleep(0.1)
      await msg.edit("""🖤🖤🖤
🖤🖤🖤
🖤🖤🖤""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤍🤍🤍
🤍🤍🤍
🤍🤍🤍""")
      await asyncio.sleep(0.1)
      await msg.edit("""❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️""")
      await asyncio.sleep(0.1)
      await msg.edit("""🧡🧡🧡🧡🧡🧡
🧡🧡🧡🧡🧡🧡
🧡🧡🧡🧡🧡🧡
🧡🧡🧡🧡🧡🧡
🧡🧡🧡🧡🧡🧡
🧡🧡🧡🧡🧡🧡""")
      await asyncio.sleep(0.1)
      await msg.edit("""💛💛💛💛💛💛
💛💛💛💛💛💛
💛💛💛💛💛💛
💛💛💛💛💛💛
💛💛💛💛💛💛
💛💛💛💛💛💛""")
      await asyncio.sleep(0.1)
      await msg.edit("""💚💚💚💚💚💚
💚💚💚💚💚💚
💚💚💚💚💚💚
💚💚💚💚💚💚
💚💚💚💚💚💚
💚💚💚💚💚💚""")
      await asyncio.sleep(0.1)
      await msg.edit("""💙💙💙💙💙💙
💙💙💙💙💙💙
💙💙💙💙💙💙
💙💙💙💙💙💙
💙💙💙💙💙💙
💙💙💙💙💙💙""")
      await asyncio.sleep(0.1)
      await msg.edit("""💜💜💜💜💜💜
💜💜💜💜💜💜
💜💜💜💜💜💜
💜💜💜💜💜💜
💜💜💜💜💜💜
💜💜💜💜💜💜""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤎🤎🤎🤎🤎🤎
🤎🤎🤎🤎🤎🤎
🤎🤎🤎🤎🤎🤎
🤎🤎🤎🤎🤎🤎
🤎🤎🤎🤎🤎🤎
🤎🤎🤎🤎🤎🤎""")
      await asyncio.sleep(0.1)
      await msg.edit("""🖤🖤🖤🖤🖤🖤
🖤🖤🖤🖤🖤🖤
🖤🖤🖤🖤🖤🖤
🖤🖤🖤🖤🖤🖤
🖤🖤🖤🖤🖤🖤
🖤🖤🖤🖤🖤🖤""")
      await asyncio.sleep(0.1)
      await msg.edit("""🤍🤍🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍""")
   
      for n in range(10):
         output = ''
         for i in range(5):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
      
      for n in range(10):
         output = ''
         for i in range(5):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
         
      for n in range(10):
         output = ''
         for i in range(4):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "❤❤❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
      
      for n in range(10):
         output = ''
         for i in range(3):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "❤❤❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
      
      for n in range(10):
         output = ''
         for i in range(2):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "❤❤❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
      
      for n in range(10):
         output = ''
         for i in range(1):
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(7)]) + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "❤❤❤❤❤❤❤"  + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "❤❤❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "\n"
         
         output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
         await msg.edit(output)
         await asyncio.sleep(0.1)
      
      output = ''
      
      output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(1)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(1)]) + "\n"
      
      output += "❤❤❤❤❤❤❤"  + "\n"
      
      output += "❤❤❤❤❤❤❤"  + "\n"
      
      output += "❤❤❤❤❤❤❤"  + "\n"
         
      output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "❤❤❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(2)]) + "\n"
         
      output += "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)]) + "❤" + "".join([random.choice(["🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]) for j in range(3)])
         
      await msg.edit(output)
   except FloodWait as e:
      await asyncio.sleep(e.value)

@func(filters.command('t') & filters.me)
async def type_text(app: Client, msg: Message):
    original_text=' '.join(msg.text.split()[1:])
   
    if not original_text:
        return await msg.edit("Вы не указали параметр: [текст]")
   
    text = ""
    while (len(original_text) != 0):
        try:
            text += original_text[0]
            
            original_text = original_text[1:]
            
            await msg.edit(text + f"{'|' if len(original_text) % 2 == 0 else ''}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
   
    await msg.edit(text)

@func(filters.command('proc') & filters.me)
async def procents(app: Client, msg: Message):
    try:
        text1 = " ".join(msg.text.split(maxsplit=2)[1:]).split(",")[0]
        text2 = " ".join(msg.text.split(maxsplit=2)[1:]).split(",")[1]
    except IndexError as e:
        return await msg.edit("Вы не верно ввели параметры.Пример: /proc текст1,текст2")
    
    text2 = f"{text2.strip()}"
    
    proc = 0
    
    while (proc < 101):
        try:
            await msg.edit(f"{text1}{proc}%")
            
            await asyncio.sleep(0.2)
            
            proc += random.randint(1, 5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        
    await msg.edit(f"{text2}")

@func(filters.command('tanos') & filters.me)
async def tanos(app: Client, msg: Message):
    if str(msg.chat.type) in ["ChatType.GROUP", "ChatType.SUPERGROUP"]:
        await msg.answer('*Щелчок таноса')

        async for user in app.get_chat_members(msg.chat.id):
            try:
                await msg.answer(f'*{user.user.first_name} исчез')
            except FloodWait as e:
                await asyncio.sleep(e.value)
@func(filters.command('ex') & filters.me)
async def ex(app: Client, msg: Message):
    await msg.edit(random.choice(["Правда", "Ложь"]))

@func(filters.command('dc') & filters.me)
async def doctor(app: Client, msg: Message):
    await msg.edit("👨‍⚕️ Здравствуйте, я доктор Floats, сейчас я возьму у вас кровь для анализа болезни \"Кринжанутый\"💉. Пожалуйста не двигайтесь а то дам подзатылок.")
    
    await asyncio.sleep(7)
    
    proc = 0
    
    while (proc < 101):
        try:
            await msg.edit(f"Набрано крови в шприц...{proc}%")
            
            await asyncio.sleep(0.1)
            
            proc += random.randint(1, 5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
    
    proc = 0
    
    while (proc < 101):
        try:
            await msg.edit(f"ИИ анализирует...{proc}%")
            
            await asyncio.sleep(0.1)
            
            proc += random.randint(1, 5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
    
    await msg.edit(random.choice(["Чист", "Заражён, бегите отсюда"]))

@func(filters.command('ghoul') & filters.me)
async def ghoul_table(app: Client, msg: Message):
    row = 0
    ghoulich = 1000
    output = ''

    while ghoulich >= 0:
        try:
            row += 1
            ghoulich -= 7

            output += f"{ghoulich + 7} - 7 = {ghoulich}\n\n"

            if row == 10:
                await msg.edit(output)
                output = ''
                row = 0
            
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
    
    await msg.edit(output)

@func(filters.command('ocase') & filters.me)
async def open_case(app: Client, msg: Message):
    splited = msg.text.split()
    
    try:
        if int("".join(splited[1])) <= 0:
            return await msg.edit("Нельзя ставить прокрутку меньше 1")
    except Exception as e:
        await spin_case(msg)
    
    try:
        await spin_case(msg, spin=splited[1])
    except:
        pass

async def spin_case(msg, spin=10):
    emojis_in_case = ["⬜", "🟦", "🟧", "🟪", "🟨", "🟥", "⬛", "💟"]
    
    output = "".join([random.choice(emojis_in_case) for i in range(14)])
    
    await msg.edit(f"⬜⬜⬜⬜⬜⬜3️⃣⬜⬜⬜⬜⬜⬜⬜\n{output}")
    
    await asyncio.sleep(0.5)
    
    await msg.edit(f"⬜⬜⬜⬜⬜⬜2️⃣⬜⬜⬜⬜⬜⬜⬜\n{output}")
    
    await asyncio.sleep(0.5)
    
    await msg.edit(f"⬜⬜⬜⬜⬜⬜1️⃣⬜⬜⬜⬜⬜⬜⬜\n{output}")
    
    await asyncio.sleep(0.5)
    
    await msg.edit(f"⬜⬜⬜⬜⬜⬜🔽⬜⬜⬜⬜⬜⬜⬜\n{output}")
    
    for i in range(int(spin)):
        try:
            output = output[1:]
            output += random.choice(emojis_in_case)
            
            await msg.edit(f"⬜⬜⬜⬜⬜⬜🔽⬜⬜⬜⬜⬜⬜⬜\n{output}")

            await asyncio.sleep(0.05)
        except FloodWait as e:
            await asyncio.sleep(e.value)

    await asyncio.sleep(0.5)
    
    emoji_rare = {
   f"{emojis_in_case[0]}": f"{emojis_in_case[0]} - common",
   f"{emojis_in_case[1]}": f"{emojis_in_case[1]} - uncommon",
   f"{emojis_in_case[2]}": f"{emojis_in_case[2]} - rare",
   f"{emojis_in_case[3]}": f"{emojis_in_case[3]} - epic",
   f"{emojis_in_case[4]}": f"{emojis_in_case[4]} - legendary",
   f"{emojis_in_case[5]}": f"{emojis_in_case[5]} - expensive",
   f"{emojis_in_case[6]}": f"{emojis_in_case[6]} - negr",
   f"{emojis_in_case[7]}": f"{emojis_in_case[7]} - incredible"
    }
    
    if msg.reply_to_message:
        try:
            name = msg.reply_to_message.from_user.first_name
        except:
            name = msg.from_user.first_name
        await msg.edit(f"⬜⬜⬜⬜⬜⬜🔽⬜⬜⬜⬜⬜⬜⬜\n{output}\n{name} выпало: {emoji_rare.get(output[6])}")
    else:
        await msg.edit(f"⬜⬜⬜⬜⬜⬜🔽⬜⬜⬜⬜⬜⬜⬜\n{output}\nвам выпало: {emoji_rare.get(output[6])}")

@func(filters.command('clown') & filters.me)
async def clown(app: Client, msg: Message):
    await msg.edit("""🫲 😐🫱            📷""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐🫱      📷""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐🫱  📷""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐📷""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐📸""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐📷""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐📷
           🖼️""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐🫱
           🖼️""")
    await asyncio.sleep(1)
    await msg.edit("""🫲 😐🖼️""")
    await asyncio.sleep(1)
    await msg.edit("""🫵 😐🤡""")
