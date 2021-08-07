# serverRadioWeb.py
# coding: utf-8

import socket
import wave
import threading

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

CHUNK = 2048    # Números de frames de áudio

# fname = "songs/Track 1.wav"
# wf = wave.open(fname, 'rb')

print("Servidor pronto para enviar")


def connection(connectionSocket, addr):
    #wf = wave.open(fname, 'rb')
    #print("entrou no connection")
    #connectionSocket, addr = serverSocket.accept()
    print("Conexão vinda de {}".format(addr))

    j = 1
    while j <= 5:
        fname = "songs/Track " + str(j) + ".wav"
        wf = wave.open(fname, 'rb')

        data = wf.readframes(CHUNK)

        while data:
            connectionSocket.send(data)
            data = wf.readframes(CHUNK)
        j += 1

    connectionSocket.close()
    wf.close()

# connectionSocket, addr = serverSocket.accept()
# print("Conexão vinda de {}".format(addr))

# data = wf.readframes(CHUNK)

# while data:
#     connectionSocket.send(data)
#     data = wf.readframes(CHUNK)

# connectionSocket.close()
# wf.close()

def main():
    i = 1
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("-----> Recebendo conexão pela {}a. vez! <-----".format(i))
        th = threading.Thread(target=connection, args=(connectionSocket, addr))
        th.start()
        i = i + 1
                	
if __name__ == '__main__':
	main()