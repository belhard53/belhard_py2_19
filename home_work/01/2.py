'''
1. написать сервер на сокетах который может принимать 3 команды
    - time - отправляет обратно текущее время
    - rnd a:int b:int - отправляет обратно случайное число от а до b (пример - int 1 6)
    - stop - останавливает сервер - отправляет сообщение об этом
    - если прислана неизвестная  команда сообщить об этом клиенту
    
    * на сервере вести лог всех присланных команд в файл 
    
2. написать клиент который запрашивает бесконечно команду для сервера
    и выводит в консоль ответ.

'''


# ---------- server ----

import socket
import threading
from datetime import datetime
import random
import logging

HOST = ('127.0.0.1', 7777)
LOG_FILE = "server.log"

# Логирование
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

def log_command(client_ip, command):
    logging.info(f"{client_ip}: {command}")

def handle_client(conn, addr):
    """Обработка клиента в отдельном потоке"""
    client_ip = addr[0]
    print(f"Подключен {client_ip}")
    
    while True:
        try:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                break
                
            log_command(client_ip, data)
            
            if data == "time":
                answer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            elif data == "stop":
                answer = "Сервер остановлен"
                conn.send(answer.encode('utf-8'))
                conn.close()
                return  # Завершить поток
                
            elif data.startswith('rnd'):
                parts = data.split()
                if len(parts) == 3:
                    try:
                        a, b = int(parts[1]), int(parts[2])
                        answer = f"result: {random.randint(min(a,b), max(a,b))}"
                    except ValueError:
                        answer = "Ошибка: нужны целые числа (rnd a b)"
                else:
                    answer = "Формат: rnd a b"
                    
            else:
                answer = "Неизвестная команда"
                
            conn.send(answer.encode('utf-8'))
            
        except:
            break
    
    conn.close()
    print(f"Отключен {client_ip}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование порта
    sock.bind(HOST)
    sock.listen(5)  # Очередь из 5 клиентов
    
    print('Сервер запущен на', HOST)
    print('Команды: time, rnd a b, stop')
    
    try:
        while True:
            conn, addr = sock.accept()
            # Новый поток для каждого клиента
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
