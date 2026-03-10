from celery import chord
from celery_test import long_running_task, add

def process_final_results(results):
    """Callback функция, которая выполнится после всех задач"""
    print(f"\n=== Все задачи завершены! ===")
    print(f"Получено результатов: {len(results)}")
    print(f"Результаты: {results}")
    
    # Можно обработать результаты
    total_tasks = len(results)
    return f"Обработано {total_tasks} задач"

def run_with_callback():
    print("=== Запуск с callback после завершения ===\n")
    
    # Создаем группу задач
    header = [long_running_task.s(i) for i in [2, 3, 4, 2, 3]]
    
    # Создаем chord: группа задач + callback
    callback = add.s(100)  # Простая функция для демонстрации
    # Или свою callback функцию:
    # from celery_test import process_final_results
    # callback = process_final_results.s()
    
    job = chord(header)(callback)
    
    print("Задачи запущены, ожидаем окончания...")
    final_result = job.get(timeout=30)
    
    print(f"\nФинальный результат: {final_result}")

if __name__ == '__main__':
    run_with_callback()