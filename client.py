import socket
import threading

def Send(client):
    while True:
        str = input()
        if str != '':
            message = "[" + NAME + "] " + str
            # 사용자 입력
            client.send(bytes(message.encode()))  
            # Client -> Server 데이터 송신 

def Recv(client):
    while True:
        recv_data = client.recv(1024).decode()  
        # Server -> Client 데이터 수신
        print(recv_data)

if __name__ == '__main__':
    # client 설정
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
    # SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

    SERVER = input("IP:")
    # 통신할 대상의 IP 주소
    PORT = int(input("PORT:"))
    # 통신할 대상의 Port 주소

    NAME = input("NAME:")

    # Server Aress
    ADDR = (SERVER, PORT)
    # result : ('PC Adress(IPV4)', PORT(6060), 'NAME')
    
    # server에 연결
    client.connect(ADDR)
    # 서버로 연결시도

    print(f'Connecting to {SERVER}:{PORT}')

    #Client의 메시지를 보낼 쓰레드
    sendthread = threading.Thread(target=Send, args=(client, ))
    sendthread.start()

    #Server로 부터 다른 클라이언트의 메시지를 받을 쓰레드
    recvthread = threading.Thread(target=Recv, args=(client, ))
    recvthread.start()