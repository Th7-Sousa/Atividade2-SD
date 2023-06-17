import socket
import threading

class EstatisticaQuestoes:
    def _init_(self):
        self.questoes = {}

    def adicionarResposta(self, numQuestao, acertos, erros):
        if numQuestao in self.questoes:
            self.questoes[numQuestao][0] += acertos
            self.questoes[numQuestao][1] += erros
        else:
            self.questoes[numQuestao] = [acertos, erros]

    def obterEstatisticas(self):
        estatisticas = "Estatísticas:\n"
        for questao, resultado in self.questoes.items():
            acertos, erros = resultado
            estatisticas += f"Questão {questao}: acertos={acertos} erros={erros}\n"
        return estatisticas

def handleClient(conexao, endereco, estatisticas):
    print(f"Conexão estabelecida com {endereco}")

    file_data = b""
    while True:
        data = conexao.recv(1024)
        if not data:
            break
        file_data += data

    file_content = file_data.decode("utf-8")

    for resposta in file_content.split("\n"):
        if resposta:
            numQuestao, _, respostas = resposta.split(";")
            numQuestao = int(numQuestao)
            acertos = respostas.count("V")
            erros = respostas.count("F")
            estatisticas.adicionarResposta(numQuestao, acertos, erros)

    estatisticas_str = estatisticas.obterEstatisticas()
    conexao.send(estatisticas_str.encode("utf-8"))

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
    client_thread = threading.Thread(target=handleClient, args=(conexao, endereco, estatisticas))
    client_thread.start()