# clientRadioWeb.py
# coding: utf-8

import socket
import ssl
import pyaudio
import threading

#Alterar para o IP do servidor
serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('CA/cacert.pem')
clientSocket_ssl = context.wrap_socket(clientSocket, server_hostname=serverName)

try:
    clientSocket_ssl.connect((serverName, serverPort))
except ConnectionRefusedError:
    print("Conexão não estabelecida com o servidor. Tente novamente")

p = pyaudio.PyAudio()

FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 2048

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

try:
    content = clientSocket_ssl.recv(CHUNK)

    while content:
        stream.write(content)   # "Player" de áudio
        content = clientSocket_ssl.recv(CHUNK)
except KeyboardInterrupt:
    print("Conexão com o servidor encerrada")
except ConnectionResetError:
    print("Conexão encerrada pelo servidor")
except OSError:
    pass


stream.close()
p.terminate()
clientSocket_ssl.close()
