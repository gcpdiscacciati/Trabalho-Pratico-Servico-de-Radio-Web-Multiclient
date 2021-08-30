# serverRadioWeb.py
# coding: utf-8

import socket
import ssl
import wave
import threading
import time

NUMERO_MUSICAS = 5
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

# Criptografia ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='CA/cert-meucertificado.pem', keyfile='CA/priv-minhachave.pem')
serverSocket_ssl = context.wrap_socket(serverSocket, server_side=True)

CHUNK = 2048  # Números de frames de áudio

print("Servidor pronto para enviar...")

# Lista que abrigará todas as conexões
listaConexao = []


# Função que lê as músicas em looping
def musicReading():
    try:
        # Variável de controle de qual música tocar
        j = 1
        global listaConexao

        while True:
            fname = "songs/Track " + str(j) + ".wav"
            wf = wave.open(fname, 'rb')
            data = wf.readframes(CHUNK)

            while data:
                # Caso não haja conexões, aguarda um tempo e continua lendo frames da música
                if (len(listaConexao) == 0):
                    # 0.03s foi o tempo em que a execução sem nenhum clientes mais se aproximou da execução com clientes
                    # O que da uma impressão de "ao vivo"
                    time.sleep(0.03)
                else:
                    # Envia o mesmo dado para todas as conexões na lista
                    for conexao in listaConexao:
                        try:
                            conexao[0].send(data)
                        except ConnectionResetError:
                            # Remove conexões interrompidas da lista
                            print('Conexao {} removida'.format(conexao[1]))
                            conexaoRemovida = conexao
                            listaConexao.remove(conexao)
                            conexaoRemovida[0].close()

                data = wf.readframes(CHUNK)
            # Fecha a música atual e incrementa a variável de controle
            wf.close()
            j += 1
            # Ao chegar na última música, retorna para a primeira
            if j == NUMERO_MUSICAS + 1:
                j = 1
    except KeyboardInterrupt:
        return


def main():
    global listaConexao

    # Inicia a thread de leitura e envio das músicas
    th = threading.Thread(target=musicReading, args=())
    th.start()

    try:
        while True:
            # Aguarda por conexões e as adiciona na lista quando aceitas
            connectionSocket, addr = serverSocket_ssl.accept()
            listaConexao.append((connectionSocket, addr))
            print("-----> Recebendo conexão de {} <-----".format(addr))
    except KeyboardInterrupt:
        print("Servidor interrompido")
        return


if __name__ == '__main__':
    main()
