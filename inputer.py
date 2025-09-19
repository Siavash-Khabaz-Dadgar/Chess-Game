import socket, pickle, time

ip = "192.168.43.74"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def go():
	while True:
	
		try:
			s.bind((ip, port))
		except socket.error as e:
			print(str(e))

		s.listen()

		print("waiting for connection...")

		conn, addr = s.accept()

		connected = True
		print("connected")
		while connected == True:
			x = [(1, 2), (3, 5), (7, 9)]
			y = ["hello", "world"]
			z = [(4, 5), (6, 7)]
			w = [x, y, z]
			r = pickle.dumps(w)
			time.sleep(5)
			s.send(r)

		s.close()
go()


