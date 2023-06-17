import socket

HOST = "127.0.0.1" 
PORT = 5000        

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

respostas = "2;8;FVFFVVFV"

sock.send(respostas.encode("utf-8"))

resposta_servidor = sock.recv(1024)
print(f"Resposta do servidor: {resposta_servidor.decode('utf-8')}")

sock.close()
