from celery import group
from celery_test import long_running_task
import time

def run_parallel_tasks():
    print("=== Запуск 5 долгих задач параллельно ===\n")
    
    # Создаем группу из 5 задач
    job = group([
        long_running_task.s(3),   # задача 1 - 3 секунды
        long_running_task.s(4),   # задача 2 - 4 секунды  
        long_running_task.s(2),   # задача 3 - 2 секунды
        long_running_task.s(5),   # задача 4 - 5 секунд
        long_running_task.s(3)    # задача 5 - 3 секунды
    ])
    
    print("Задачи запущены...")
    start_time = time.time()
    
    # Запускаем группу и ждем результаты
    result = job.apply_async()
    results = result.get(timeout=30)  # timeout должен быть больше самой долгой задачи
    
    end_time = time.time()
    
    print("\n=== Результаты ===")
    for i, res in enumerate(results, 1):
        print(f"Задача {i}: {res}")
    
    print(f"\nОбщее время выполнения: {end_time - start_time:.2f} секунд")
    print(f"Задачи выполнялись параллельно!")

if __name__ == '__main__':
    run_parallel_tasks()