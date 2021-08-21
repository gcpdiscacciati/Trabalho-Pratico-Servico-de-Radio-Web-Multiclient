# clientRadioWeb.py
# coding: utf-8

import socket
import pyaudio
import threading

#Alterar para o IP do servidor
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((serverName, serverPort))
except ConnectionRefusedError:
    print("Conexão não estabelecida com o servidor. Tente novamente")

p = pyaudio.PyAudio()

FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 2048

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

try:
    content = clientSocket.recv(CHUNK)

    while content:
        stream.write(content)   # "Player" de áudio
        content = clientSocket.recv(CHUNK)
except KeyboardInterrupt:
    print("Conexão com o servidor encerrada")
except ConnectionResetError:
    print("Conexão encerrada pelo servidor")
except OSError:
    pass


stream.close()
p.terminate()
clientSocket.close()