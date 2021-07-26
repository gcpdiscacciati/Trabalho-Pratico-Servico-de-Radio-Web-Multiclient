# serverRadioWeb.py
# coding: utf-8

import socket
import wave

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

CHUNK = 2048    # Números de frames de áudio

fname = "/songs/Track 1.wav"
wf = wave.open(fname, 'rb')

print("Servidor pronto para enviar")

connectionSocket, addr = serverSocket.accept()
print("Conexão vinda de {}".format(addr))

data = wf.readframes(CHUNK)

while data:
    connectionSocket.send(data)
    data = wf.readframes(CHUNK)

connectionSocket.close()
wf.close()