import socket

HOST = "127.0.0.1"
PORT = 5000

socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socke.connect((HOST, PORT))

caminho_arquivo = "/respostas.txt"

with open(caminho_arquivo, "r") as arquivo:
    respostas = arquivo.read().strip()

socke.send(respostas.encode("utf-8"))

resServidor = socke.recv(1024).decode("utf-8")
print(f"Resposta do servidor: {resServidor}")

socke.close()
