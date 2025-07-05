import asyncio
from time import sleep
import sys
import subprocess

max_retries = 10
retry_delay = 15
retries = 0

while retries < max_retries:
    try:
        from main import app, main
        app.run(main(retries))
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()
    except KeyboardInterrupt:
        print('<3')
        break

    except (ConnectionError, TimeoutError) as e:
        print(e)
        print('Ошибка с соединением...')
        sleep(retry_delay)

    retries += 1
