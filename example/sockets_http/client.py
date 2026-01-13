import socket

HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect(HOST)
# text = b'123456789'
# text = b'Hello'
text = 'Hello'.encode('utf-8')
sock.send(text)
data = sock.recv(1024).decode() # залипает и ждет ответ
print(data)

sock.close()



