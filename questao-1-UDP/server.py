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

    def pegarEstatistica(self):
        estatisticas = "Estatísticas:\n"
        for questao, resultado in self.questoes.items():
            acertos, erros = resultado
            estatisticas += f"Questão {questao}: acertos={acertos} erros={erros}\n"
        return estatisticas

def handle_client(conexao, endereco, estatisticas):
    print(f"Conexão estabelecida com {endereco}")

    while True:
        data = conexao.recv(1024)
        if not data:
            break

        resposta = data.decode("utf-8")
        numero_questao, _, respostas = resposta.split(";")
        numero_questao = int(numero_questao)
        acertos = respostas.count("V")
        erros = respostas.count("F")

        estatisticas.adicionarRes(numero_questao, acertos, erros)

        resServer = f"{numero_questao};{acertos};{erros}"
        conexao.send(resServer.encode("utf-8"))

    print(f"Conexão encerrada com {endereco}")
    conexao.close()


HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("Servidor em execução")

estatisticas = EstatisticaQuestoes()

while True:
    conexao, endereco = sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(conexao, endereco, estatisticas))
    client_thread.start()
