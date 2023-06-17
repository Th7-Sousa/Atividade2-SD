import socket

HOST = "127.0.0.1"  
PORT = 5000       

socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socke.connect((HOST, PORT))

#arquivo de resposta
respostas = "1;5;VVFFV"
socke.send(respostas.encode("utf-8"))

#receber e printar resposta do servidor
resServidor = socke.recv(1024).decode("utf-8")
print(f"Resposta do servidor: {resServidor}")

socke.close()
