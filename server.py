import socket
import threading

# Message 설정
HEADER = 64
# 최대 {HEADER}byte의 데이터(message)를 통신할 수 있다.

# PORT 지정
PORT = 6060

# SERVER 설정
SERVER = socket.gethostbyname(socket.gethostname())
# socket.gethostname() -> PC Name
# socket.gethostbyname(PC Name) -> IP Adress

# Final Server Aress
ADDR = (SERVER, PORT)
# result : ('PC Adress(IPV4)', PORT(6060))

# message 형식 설정
FORMAT = 'utf-8'

# 연결 해제 메세지 설정
DISCONNECT_MESSAGE = "DISCONNECT!"

# socket 설정
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
# SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

# 서버와 PORT 연결
server.bind(ADDR)
# 서버(PC Adress(IPV4))에 PORT(6060)를 연결
# bind는 값을 튜플로 받기에 괄호가 두개이어야한다
# result : server.bind(('PC Adress', 6060))

def Handle_client(conn, addr):
    # conn -> 연결된 대상과 다시 통신할 수 있게 해주는 소켓 개체
    # addr -> 연결 요청이 온 client의 ip adress와 PORT번호
    print(f"※NEW CONNECTION※\n{addr} connected.\n")
    connected = True
    while connected:
        message_length = conn.recv(HEADER).decode(FORMAT)
        # recv(HEADER) -> client로부터 최대 {HEADER}byte까지의 데이터를 받는다
        if message_length:    
            message_length = int(message_length)
            message = conn.recv(message_length).decode(FORMAT)
            if message == DISCONNECT_MESSAGE:
                print(f"{addr} disconnected.\n")
                connected = False
                # while문 종료
            print(f"[{addr}] {message}")
            conn.send("Message received.".encode(FORMAT))
    conn.close()
    # close() -> 연결 해제

def start():
    server.listen()
    # server에 새로운 연결을 listen
    print(f"※LISTENING※\nserver is listening on {SERVER}\n")
    while True:
        conn, addr = server.accept()
        # client에서 연결요청을 보내면 accept로 받고 return 값으로 소켓정보와 ip정보가 나온
        thread = threading.Thread(target=Handle_client, args=(conn, addr))
        thread.start()
        print(f"※ACTIVE CONNECTIONS※\n{threading.activeCount()-1} threads running......")
        # threading.activeCount() -> 현재 실행 중인 스레드 갯수
        # -1을 하는 이유 : 처음 실행 되는 스레드는 항상 실행되어야 하기 때문에 

print(f"※STARTING※\nserver is starting......\nserver adress : {SERVER}:{PORT}\n")
start()

