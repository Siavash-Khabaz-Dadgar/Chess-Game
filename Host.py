import socket, time
from _thread import start_new_thread



ip = socket.gethostbyname(socket.gethostname())
port = 5555
connected = False

"""-------------------------------------------------------------retry connection---------------------------------------------------------------"""

def retry():
    pass


"""--------------------------------------------------function to receive data from other user-------------------------------------------------"""


def receive_data():
    while True:
        try:
            recv_data = conn.recv(4096)
            import game
            game.receive_data(recv_data)
        except:
            print("Disconnected(Host)")
            conn.close()
            break

"""--------------------------------------------------function to send data to other user-------------------------------------------------"""


def send_data(data):
    
    global connected

    try:
        conn.send(data)
    except socket.error as e:
        print("Host, send")
        print(str(e))
        connected = False
    
    start_new_thread(receive_data, ())


"""--------------------------------------------------function to start Host and wait for connection-------------------------------------------------"""
def connecter():
    global connected, conn
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((ip, port))
    except socket.error as e:
        print(str(e))
    
    s.listen(1)
    
    print("waiting for connection...")
    
    conn, addr = s.accept()
    connected = True
    print("connected")

    
