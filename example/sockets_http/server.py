import socket

# HOST = socket.gethostname()
# print(HOST)

HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print('---start---')

while 1:
    print('----------------- listen ------------------')
    conn, addr = sock.accept() # залипает на этой строчке и ждет запроса от любого клиента
    print(f'---connected from {addr[0]}---')
    # print(conn)
    # print(addr)
    
    print('---wait data---')
    data = conn.recv(1024).decode() # если соединение не закрыто клиентом залипает на этой строчке                    
    # data = conn.recv(4).decode() # получит только 4 байта, неважно send или sendall
    if data:
        print(f'send data - {data}')
        conn.send(b'OK')
    
    
# recv() переходит к следующей строке когда:
#     Пришли данные (любое количество)
#     Соединение закрыто (data = b'')
#     Произошла ошибка (исключение)
#     Истек таймаут (если установлен sock.settimeout(1))    