import socket

HOST = "127.0.0.1" 
PORT = 5000        

sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

respostas = "1;5;VVFFV"

sockt.sendto(respostas.encode("utf-8"), (HOST, PORT))

resposta_servidor, _ = sockt.recvfrom(1024)
print(f"Resposta do servidor: {resposta_servidor.decode('utf-8')}")

sockt.close()
