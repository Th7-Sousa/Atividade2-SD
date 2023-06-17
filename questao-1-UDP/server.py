import socket
import threading

class EstatisticaQuestoes:
    def __init__(self):
        self.questoes = {}

    def adicionarRes(self, numero_questao, acertos, erros):
        if numero_questao in self.questoes:
            self.questoes[numero_questao][0] += acertos
            self.questoes[numero_questao][1] += erros
        else:
            self.questoes[numero_questao] = [acertos, erros]

    def pegarEsatatistica(self):
        estatisticas = "Estatísticas:\n"
        for questao, resultado in self.questoes.items():
            acertos, erros = resultado
            estatisticas += f"Questão {questao}: acertos={acertos} erros={erros}\n"
        return estatisticas

def handle_client(sock, addr, estatisticas):
    print(f"Conexão estabelecida com {addr}")

    while True:
        data, _ = sock.recvfrom(1024)
        if not data:
            break

        resposta = data.decode("utf-8")
        numero_questao, _, respostas = resposta.split(";")
        numero_questao = int(numero_questao)
        acertos = respostas.count("V")
        erros = respostas.count("F")

        estatisticas.adicionarRes(numero_questao, acertos, erros)

        resServer = f"{numero_questao};{acertos};{erros}"
        sock.sendto(resServer.encode("utf-8"), addr)

    print(f"Conexão encerrada com {addr}")


HOST = "127.0.0.1"  
PORT = 5000        

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Server run")

estatisticas = EstatisticaQuestoes()

while True:
    data, addr = sock.recvfrom(1024)

    client_thread = threading.Thread(target=handle_client, args=(sock, addr, estatisticas))
    client_thread.start()
