import socket, time, game
import sys
from _thread import start_new_thread


ip = ""
port = 5555
connected = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""--------------------------------------------------function to receive data from other user-------------------------------------------------"""


def receive_data():
    while True:
        try:
            recv_data = client.recv(4096)
            
            import game
            game.receive_data(recv_data)
        except:
            print("Disconnected(Join)")
            client.close()
            break

"""--------------------------------------------------function to send data to other user-------------------------------------------------"""


def send_data(data):
    global connected

    try:
        client.send(data)
    except socket.error as e:
        print("Join, send")
        print(str(e))
        connected = False
    
"""--------------------------------------------------function to start connect to the host-------------------------------------------------"""

def Joiner():
    global connected, client
    try:
        client.connect((ip, port))
        connected = True
    except socket.error as e:
        print(str(e))
        return
    start_new_thread(receive_data, ())
    