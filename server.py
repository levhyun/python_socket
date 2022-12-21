import socket
import threading
from queue import Queue

# def Message_set(message):
#     start = 0
#     stop = 0
#     for i in range(0,len(str(message))):
#         if message[i] == '[':
#             start = i
#         if message[i] == ']':
#             stop = i+1
#     name = message[start:stop]
#     message = message[stop:len(str(message))]
#     message = message + name
#     message_length = len(str(message))
#     space = " "
#     final_space = ""
#     for i in range(0,146-message_length):
#         final_space = final_space + space   
#     final_message = final_space + message
#     return final_message

def Send(group, send_queue):
    print('Thread Send Start')
    while True:
        try:
            #새롭게 추가된 클라이언트가 있을 경우 Send 쓰레드를 새롭게 만들기 위해 루프를 빠져나감
            recv = send_queue.get()
            if recv == 'Group Changed':
                print('Group Changed')
                break


            #for 문을 돌면서 모든 클라이언트에게 동일한 메시지를 보냄
            for conn in group:
                message = str(recv[0])
                if recv[1] != conn: 
                    #client 본인이 보낸 메시지는 받을 필요가 없기 때문에 제외시킴
                    print(message)
                    conn.send(bytes(message.encode()))
                else:
                    pass
        except:
            pass

def Recv(conn, count, send_queue):
    print('Thread Recv(' + str(count) + ') Start\n')
    while True:
        message = conn.recv(1024).decode()
        print(f"RECEIVE([{SERVER}:6060][Thread:{str(count)}]{message})")
        # send_queue.put([Message_set(message), conn, count]) 
        send_queue.put([message, conn, count]) 
        #각각의 클라이언트의 메시지, 소켓정보, 쓰레드 번호를 send로 보냄

if __name__ == '__main__':
    send_queue = Queue()

    # PORT 지정
    PORT = 6060

    # SERVER 설정
    SERVER = socket.gethostbyname(socket.gethostname())
    # socket.gethostname() -> PC Name
    # socket.gethostbyname(PC Name) -> IP Adress

    # Final Server Aress
    ADDR = (SERVER, PORT)
    # result : ('PC Adress(IPV4)', PORT(6060))

    print(f"※STARTING※\nserver is starting......\nserver adress : {SERVER}:{PORT}\n")

    # socket 설정
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
    # SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

    # 서버와 PORT 연결
    server.bind(ADDR)
    # 서버(PC Adress(IPV4))에 PORT(6060)를 연결
    # bind는 값을 튜플로 받기에 괄호가 두개이어야한다
    # result : server.bind(('PC Adress', 6060))

    server.listen()
    # server에 새로운 연결을 listen
    # 소켓 연결, 여기서 파라미터는 접속수를 의미
    print(f"※LISTENING※\nserver is listening on {SERVER}\n")

    count = 0 
    # 쓰레드 번호 카운트
    group = [] 
    #연결된 클라이언트의 소켓정보를 리스트로 묶기 위함
    
    while True:
        count += 1
        conn, addr = server.accept()  
        # 해당 소켓을 열고 대기

        group.append(conn) 
        #연결된 클라이언트의 소켓정보
        print(f"※NEW CONNECTION※\n{str(addr)} connected.")

        #소켓에 연결된 모든 클라이언트에게 동일한 메시지를 보내기 위한 쓰레드(브로드캐스트)
        #연결된 클라이언트가 1명 이상일 경우 변경된 group 리스트로 반영
        if count > 1:
            send_queue.put('Group Changed')
            sendthread = threading.Thread(target=Send, args=(group, send_queue))
            sendthread.start()
            pass
        else:
            sendthread = threading.Thread(target=Send, args=(group, send_queue))
            sendthread.start()

        #소켓에 연결된 각각의 클라이언트의 메시지를 받을 쓰레드
        recvthread = threading.Thread(target=Recv, args=(conn, count, send_queue))
        recvthread.start()