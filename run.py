import asyncio
from time import sleep
import sys
import subprocess
from pyrogram.client import Client
from sqlite3 import OperationalError
from main import main, api_id, api_hash, phone_number, password
import gc

max_retries = 10
retry_delay = 15
retries = 0

async def start_bot():
    global retries

    app = Client(
            'db', api_id=api_id.group(1) if api_id is not None else None, api_hash=api_hash.group(1) if api_hash is not None else None,
            phone_number=phone_number.group(1) if phone_number is not None else None,
            password=password.group(1) if password is not None else None, max_concurrent_transmissions=20, workers=8
            )

    async with app:
        await main(app, retries)
    
    del app
    gc.collect()

while retries < max_retries:
    try:
        asyncio.run(start_bot())

        subprocess.run([sys.executable] + sys.argv)
        sys.exit()
    except KeyboardInterrupt:
        print('<3')
        break

    except (ConnectionError, TimeoutError) as e:
        print(e)
        print('Ошибка с соединением...')
        sleep(retry_delay)
    except OperationalError:
        sleep(5)

    retries += 1
