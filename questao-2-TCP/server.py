import socket
import threading

#armazenar estatistica
class EstatisticaQuestoes:
    def __init__(self):
        self.questoes = {}

    def addEstatistica(self, numQuestao, acertos, erros):
        if numQuestao in self.questoes:
            self.questoes[numQuestao][0] += acertos
            self.questoes[numQuestao][1] += erros
        else:
            self.questoes[numQuestao] = [acertos, erros]

    def obter_estatisticas(self):
        estatisticas = "Estatísticas:\n"
        for questao, resultado in self.questoes.items():
            acertos, erros = resultado
            estatisticas += f"Questão {questao}: acertos={acertos} erros={erros}\n"
        return estatisticas

def handleClient(conexao, endereco, estatisticas):
    print(f"Conexão estabelecida com {endereco}")

    while True:
        data = conexao.recv(1024)
        if not data:
            break

        #dados cliente
        resposta = data.decode("utf-8")
        numQuestao, _, respostas = resposta.split(";")
        numQuestao = int(numQuestao)
        acertos = respostas.count("V")
        erros = respostas.count("F")

        estatisticas.addEstatistica(numQuestao, acertos, erros)

        resServidor = f"{numQuestao};{acertos};{erros}"
        conexao.send(resServidor.encode("utf-8"))

    print(f"Conexão encerrada com {endereco}")
    conexao.close()


HOST = "127.0.0.1" 
PORT = 5000        

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("Servidor iniciado.")

estatisticas = EstatisticaQuestoes()

while True:
    conexao, endereco = sock.accept()

    #nova thread
    NovaThread = threading.Thread(target=handleClient, args=(conexao, endereco, estatisticas))
    NovaThread.start()
