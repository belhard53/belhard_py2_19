#redis-server

# Celery: асинхронная очередь задач в Python

#pip install celery
#pip install flower # устанавливает веб-UI для мониторинга Celery (Redis/RabbitMQ задачи)! 

# celery -A celery_test flower --port=5555
# celery -A celery_test worker --pool=solo --loglevel=info

# delay - это упрощенный вариант apply_async с стандартными параметрами.
# apply_async позволяет более гибко настроить выполнение задачи, например, установить время отсрочки, очередь, приоритет и т.д.


from celery import Celery
import time

# Создаем Celery приложение
app = Celery(
    'test_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Конфигурация
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

# Простая задача
@app.task
def add(x, y):
    print(f"Выполняется сложение: {x} + {y}")
    return x + y

# Долгая задача
@app.task
def long_running_task(seconds):
    print(f"Задача выполняется {seconds} секунд...")
    time.sleep(seconds)
    return f"Завершено после {seconds} секунд"

# Задача с ошибкой
@app.task(bind=True)
def failing_task(self, x):
    try:
        if x == 0:
            raise ValueError("Деление на ноль!")
        return 10 / x
    except Exception as exc:
        # Повторные попытки
        raise self.retry(exc=exc, countdown=5)

if __name__ == '__main__':
    # Тестируем синхронно (без воркера)
    print("Синхронный тест:")
    result = long_running_task.apply(args=[20])
    result = long_running_task.apply(args=[5])
    result = long_running_task.apply(args=[7])
    result = long_running_task.apply(args=[9])
    # result = add.apply(args=[4, 6])
    print(f"Результат: {result.get()}")