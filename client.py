import socket

# Message 설정
HEADER = 64
# 최대 {HEADER}byte의 데이터(message)를 통신할 수 있다.

# message 형식 설정
FORMAT = 'utf-8'

# 연결 해제 메세지 설정
DISCONNECT_MESSAGE = "DISCONNECT!"

SERVER = input()
PORT = int(input())

# Server Aress
ADDR = (SERVER, PORT)
# result : ('PC Adress(IPV4)', PORT(6060))

# client 설정
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
# SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

# server에 연결
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

print(f"연결 해제 메세지 : {DISCONNECT_MESSAGE}\n")
while True:
    talk = input()
    send(talk)    