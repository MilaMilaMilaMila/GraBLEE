import py4cytoscape as p4c
import sched
import threading
import time

def ping_cytoscape(scheduler):
    try:
        # Проверка подключения к Cytoscape
        # p4c.cytoscape_ping()

        print('Успешный пинг к Cytoscape')

    except Exception as e:
        print(f'Ошибка пинга: {e}')

    # Планирование следующего пингования через указанный интервал
    interval = 3 # Интервал в секундах
    scheduler.enter(interval, 1, ping_cytoscape, (scheduler,))

# Создание планировщика событий
scheduler = sched.scheduler(time.time, time.sleep)

# Планирование первого пингования Cytoscape
scheduler.enter(0, 1, ping_cytoscape, (scheduler,))

# Создание и запуск потока с планировщиком
scheduler_thread = threading.Thread(target=scheduler.run)
scheduler_thread.start()

# Продолжение выполнения других команд
# ...


def f():
    while True:
        print('privet')


f_thread = threading.Thread(target=f)
f_thread.start()

# Ожидание завершения потока с планировщиком (необязательно)
scheduler_thread.join()
f_thread.join()