from main import app, main
from time import sleep

max_retries = 10 # Кол-во попыток
retry_delay = 15 # В секундах
retries = 0

while retries < max_retries:
    try:
        app.run(main(retries))
    except KeyboardInterrupt:
        print('<3')
        break
    except (ConnectionError, TimeoutError):
        print('Ошибка с соединением...')
        sleep(retry_delay)

    retries += 1