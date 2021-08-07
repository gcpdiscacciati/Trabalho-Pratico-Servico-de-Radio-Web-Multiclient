# clientRadioWeb.py
# coding: utf-8

import socket
import pyaudio
import threading

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

p = pyaudio.PyAudio()

FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 2048

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

content = clientSocket.recv(CHUNK)

while content:
    stream.write(content)   # "Player" de áudio
    content = clientSocket.recv(CHUNK)

print("Audio executado")

stream.close()
p.terminate()
clientSocket.close()