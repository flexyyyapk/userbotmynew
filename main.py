import subprocess
import asyncio
import re
import json

#⚠️нечего не убирать
modules = ["pyrogram", "colorama", "progress", "pyfiglet", "wikipedia", "googletrans", "gtts", "speedtest", "pillow"]

try:
   with open("options.txt", "r") as f:
      options = json.loads(f.read())
      
      if options["install"] == "1":
         for module in modules:
            subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL)
            print(f"\033[31m{module} Установлен\033[0m")
except Exception as e:
   with open("options.txt", "w") as f:
      options = {"clue": "0 = False, 1 = True","install": "1", "ask_for_install": "1", "afk": "0", "installs": modules}
         
      options = json.dumps(options, indent=2)
      
      f.write(options)
      
      for module in modules:
         subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL)
         print(f"\033[31m{module} Установлен\033[0m")

try:
   with open("options.txt", "r") as f:
      options = json.loads(f.read())
      
      if options["ask_for_install"] == "1":
         ask = input("Установить библеотеки?(да/Нет): ")
         
         if ask.lower() == "да":
            for module in modules:
               subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL)
               print(f"\033[31m{module} Установлен\033[0m")
         else:
            options["ask_for_install"] = "0"
            options["install"] = "0"
            
            for module in modules:
               if module not in options["installs"]:
                  subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL)
                  print(f"\033[31m{module} Установлен\033[0m")
            
            options["installs"] = modules
            
            options = json.dumps(options, indent=2)
            
            with open("options.txt", "w") as f:
               f.write(options)
except Exception as e:
   with open("options.txt", "w") as f:
      options = {"clue": "0 = False, 1 = True","install": "1", "ask_for_install": "1", "afk": "0", "installs": modules}
         
      options = json.dumps(options, indent=2)
      
      f.write(options)
      
      for module in modules:
         subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL)
         print(f"\033[31m{module} Установлен\033[0m")

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode

from colorama import init, Style, Fore
import progress.bar as pb
from pyfiglet import Figlet
import wikipedia
from googletrans import Translator
from gtts import gTTS
import speedtest
from PIL import Image, ImageDraw, ImageFont

import time
import random
import io

init()

load = pb.ShadyBar("Загрузка", max=100)
for i in range(100):
   load.next()
   time.sleep(0.01)
load.finish()

custom_fig = Figlet(font='slant')
ascii_art = custom_fig.renderText('New User Bot')
print(ascii_art)

print(f"{Fore.YELLOW}Код запущен, чтобы узнать команды введите .help в чате{Fore.RESET}")

api_id = "your id"
api_hash = "your hash"

app = Client("NewUserBotDB", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help(_, msg):
   await msg.edit("<code>.helpM</code> - Основные команды\n<code>.helpF</code> - команды для веселья", parse_mode=ParseMode.HTML)

@app.on_message(filters.command("helpM", prefixes="."))
async def help_main(_, msg):
   await msg.edit("""
Раздел: Основные функции
**__1)__****.spam** [кол-во] [текст] - спамит
**__2)__****.ispam** [интервал сек.] [кол-во] [текст] - спамит интервалом
**__3)__****.rd** [число1] [число2] - выводит рандомное число
**__4)__****.rt** [текст1],[текст2],[и так далее...] - выводит рандомный текст, писать через запятые
**__5)__****.c** [пример] - обычный калькулятор
**__6)__****.wiki** [текст] - ищет информацию на Википедии
**__7)__****.tr** [с] [на] [текст] - переводит текст
**__8)__****.tts** [текст] - преобразует текст в речь
**__9)__****.ping** - выводит ваш пинг
**__10)__****.afk** - вводит вас в режим афк.Если вы включите его, то пользователи пишущие вам, получат сообщение о том, что вы заняты.Чтобы выключить, введите снова
**__11)__****.info** - Показывает информацию о чате/пользователе.Чтобы узнать о пользователе, нужно ответить на его сообщение
   """)

@app.on_message(filters.command("helpF", prefixes="."))
async def help_fun(_, msg):
   await msg.edit("""
Раздел: Функции для веселья
**__1)__****.love** - анимация сердечек
**__2)__****.t** [текст] - анимация печатания
**__3)__****.cit** [символ курсора] [текст] - анимация печатания с своим курсором
**__4)__****.s** [текст загрузки],[текст успешной загрузки] - анимация загрузки
**__5)__****.tanos** - называет все имена и добавляет к этому текст изчезает
**__6)__****.ex** - выводит рандомно Правда или Ложь
**__7)__****.dc** - выводит рандомно чист или заражён
**__8)__****.ghoul** - показывает таблицу где отнимают -7, 1000 до -1
**__9)__****.ocase** [необязательно(кол-во прокрутки)] - анимация 'кейса'
**__10)__****.sti** [текст] - отправляет стикер со шрифтом из Майнкрафта
""")

@app.on_message(filters.command("spam", prefixes="."))
async def spam(_, msg):
   value = len(msg.text.split())
   
   try:
      text = " ".join(msg.text.split()[2:])
      count = int(msg.text.split()[1])
   except IndexError as e:
      return await msg.edit(f"{'Вы не указали параметры: [кол-во] [текст]' if value == 1 else ''}{'Вы не указали параметр: [текст]' if value == 2 else ''}")
   except ValueError as e:
      return await msg.edit("Вы не верно указали кол-во спама")
   
   if not text:
      return await msg.edit(f"{'Вы не указали параметры: [кол-во] [текст]' if value == 1 else ''}{'Вы не указали параметр: [текст]' if value == 2 else ''}")
   
   await msg.delete()
   
   if count >= 10_000:
      print(f"{Fore.YELLOW}Кол-во спама свыше 10К может сильно тормозить процесс!{Fore.RESET}")
   
   info = pb.ShadyBar("spam", max=count)
   for i in range(count):
      info.next()
      try:
         await app.send_message(msg.chat.id, text)
      except FloodWait as e:
         await asyncio.sleep(e.value)
   info.finish()

@app.on_message(filters.command("ispam", prefixes=".") & filters.me)
async def interval_spam(_, msg):
   value = len(msg.text.split())
   try:
      interval = int(msg.text.split()[1])
      count = int(msg.text.split()[2])
      text = " ".join(msg.text.split()[3:])
   except IndexError as e:
      return await msg.edit(f"{'Вы не указали параметры: [интервал] [кол-во] [текст]' if value == 1 else ''}{'Вы не указали параметры: [кол-во] [текст]' if value == 2 else ''}{'Вы не указали параметры: [текст]' if value == 3 else ''}")
   except ValueError as e:
      return await msg.edit("Вы не верно указали кол-во спама или интервал")
   
   if not text:
      return await msg.edit(f"{'Вы не указали параметры: [интервал] [кол-во] [текст]' if value == 1 else ''}{'Вы не указали параметры: [кол-во] [текст]' if value == 2 else ''}{'Вы не указали параметры: [текст]' if value == 3 else ''}")
   
   await msg.delete()
   
   if count >= 10_000:
      print(f"{Fore.YELLOW}Кол-во спама свыше 10К может сильно тормозить процесс!{Fore.RESET}")
   
   info = pb.ShadyBar("ispam", max=count)
   for i in range(count):
      info.next()
      try:
         await app.send_message(msg.chat.id, text)
         await asyncio.sleep(interval)
      except FloodWait as e:
         await asyncio.sleep(e.value)
   info.finish()

@app.on_message(filters.command("rd", prefixes=".") & filters.me)
async def r_digit(_, msg):
   value = len(msg.text.split())
   try:
      value1 = int(msg.text.split()[1])
      value2 = int(msg.text.split()[2])
   except IndexError:
      return await msg.edit(f"{'Вы не указали параметры: [число1] [число2]' if value == 1 else ''}{'Вы не указали параметр: [число2]' if value == 2 else ''}")
   except ValueError as e:
      return await msg.edit("Вы не верно указали параметр, пример: .ri 0 10")
   
   await msg.edit(random.randint(value1, value2))

@app.on_message(filters.command("rt", prefixes=".") & filters.me)
async def random_text(_, msg):
   value = len(msg.text.split())
   
   texts = msg.text.split(",")[1:]
   
   if not texts:
      return await msg.edit("Вы не указали список, пример: .rt текст 1,текст 2,и так далее...")
   
   output = ""
   for text in texts:
      if text[0] == " ":
         text = text[1:]
      output += f"{f'{text}' if not output else f',{text}'}"
   
   await msg.edit(random.choice(output.split(",")))

@app.on_message(filters.command("c", prefixes=".") & filters.me)
async def calculator(_, msg):
   value = len(msg.text.split())
   try:
      if not any(True for i in range(len(" ".join(msg.text.split(".c ")[1:]))) if " ".join(msg.text.split(".c ")[1:])[i] in "0 1 2 3 4 5 6 7 8 9 * / + -".split()):
         return print(f"{Fore.YELLOW}Была совершена попытка взлома вашего устройства, программа отклонила запрос на выполнение функций.{Fore.RESET}")
      result = int(eval(msg.text.split(".c ")[1]))
   except ValueError as e:
      return await msg.edit("Вы не верно указали уравнения")
   except IndexError as e:
      return await msg.edit("Вы не указали параметр: [уравнение], пример: .c 4*2+3")
   except Exception as e:
      return await msg.edit("Что то пошло не так")
   
   await msg.edit(result)

@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
async def search_in_wikipedia(_, msg):
   try:
        wikipedia.set_lang("ru")
        
        search_query = msg.text.split('.wiki ')[1]
        
        result = wikipedia.summary(search_query, sentences=1000)
        
        await msg.edit(result)
        
   except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        
        output = "Выберите один из вариантов: "
        
        for i, option in enumerate(options, start=1):
            output += f"\n{i}. {option}"
         
        await msg.edit(output)
         
        user_response = await dp.wait_for(msg, timeout=60.0, check=lambda message: message.from_user.id == message.from_user.id)
        choice = int(user_response.text)
       
        if 1 <= choice <= len(options):
           selected_option = options[choice - 1]
           
           result = wikipedia.summary(selected_option, sentences=100)
           
           await msg.edit(msg.chat.id, result)
        else:
           await msg.edit("Выбран недопустимый вариант.")
   except asyncio.TimeoutError:
       await app.send_message(msg.chat.id, "Истекло время ожидания выбора.")
   except ValueError:
       await msg.edit("Пожалуйста, введите номер выбранного варианта.")

@app.on_message(filters.command("tr", prefixes=".") & filters.me)
async def translate_text(_, msg):
   value = len(msg.text.split())
   try:
      t1 = msg.text.split()[1]
      t2 = msg.text.split()[2]
      text = " ".join(msg.text.split()[3:])
   except IndexError as e:
      return await msg.edit(f"{'Вы не указали параметры: [с] [на] [текст для перевода]' if value == 1 else ''}{'Вы не указали параметры: [на] [текст для перевода]' if value == 2 else ''}{'Вы не указали параметр: [текст для перевода]' if value == 3 else ''}")
   
   if not text:
      return await msg.edit(f"{'Вы не указали параметры: [с] [на] [текст для перевода]' if value == 1 else ''}{'Вы не указали параметры: [на] [текст для перевода]' if value == 2 else ''}{'Вы не указали параметр: [текст для перевода]' if value == 3 else ''}")
   
   translator = Translator()
   
   try:
      translated = translator.translate(f"{text}", src=f"{t1}", dest=f"{t2}")
   except ValueError as e:
      return await msg.edit("Вы указали неверный языковой код")
   
   await msg.edit(translated.text)

@app.on_message(filters.command("tts", prefixes=".") & filters.me)
async def tts(_, msg):
   try:
      text = msg.text.split(".tts ")[1]
   except IndexError as e:
      return await msg.edit("Вы не указали параметр: [текст]")
   
   tts = gTTS(text, lang="ru")
   
   audio_buffer = io.BytesIO()
   
   tts.write_to_fp(audio_buffer)
   
   audio_buffer.seek(0)
   
   audio_buffer.name = "audio.mp3"
   
   await msg.delete()
   
   if msg.reply_to_message:
      await app.send_voice(chat_id=msg.chat.id, voice=audio_buffer, reply_to_message_id=msg.reply_to_message_id)
   else:
      await app.send_voice(chat_id=msg.chat.id, voice=audio_buffer)

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(_, msg):
   st = speedtest.Speedtest()
   
   await msg.edit("Подбор лучшего сервера...")
   
   st.get_best_server()
   
   ping_result = st.results.ping
   
   await msg.edit(f"Пинг: {ping_result}ms")

@app.on_message(filters.command("afk", prefixes=".") & filters.me)
async def afk(_, msg):
   try:
      with open("options.txt", "r") as f:
         options = json.loads(f.read())
         
         if options["afk"] == "0":
            options["afk"] = "1"
            
            await msg.edit("Вы успешно вошли в режим афк")
         else:
            options["afk"] = "0"
            
            await msg.edit("Вы успешно вышли из режима афк")
         
         options = json.dumps(options, indent=2)
         
         with open("options.txt", "w") as f:
            f.write(options)
   except:
      with open("options.txt", "w") as f:
         options = {"clue": "0 = False, 1 = True","install": "1", "ask_for_install": "1", "afk": "1", "installs": modules}
            
         options = json.dumps(options, indent=2)
         
         f.write(options)

@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def info(_, msg):
   if msg.reply_to_message:
      await msg.edit(f"Имя: {msg.reply_to_message.from_user.first_name.replace('<', '').replace('>', '')}\nФамилия: {msg.reply_to_message.from_user.last_name}\nЮзер: {msg.reply_to_message.from_user.username}\nID: <code>{msg.reply_to_message.from_user.id}</code>", parse_mode=ParseMode.HTML)
   else:
      await msg.edit(f"Имя канала/группы: {msg.chat.title.replace('<', '').replace('>', '') if msg.chat.title else 'Нету'}\nID: <code>{msg.chat.id if msg.chat.id else 'Нету'}</code>", parse_mode=ParseMode.HTML)

@app.on_message(filters.command("love", prefixes=".") & filters.me)
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
            output += "".join([random.choice(["❤", "🧡", "💛", "💚", "💙",
