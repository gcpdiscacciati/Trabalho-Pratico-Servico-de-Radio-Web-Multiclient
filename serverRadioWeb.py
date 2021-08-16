# serverRadioWeb.py
# coding: utf-8

import socket
import wave
import threading
import time
from queue import Queue

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

CHUNK = 2048    # Números de frames de áudio

print("Servidor pronto para enviar")


#Função que lê as músicas
def musicReading(queue):
    j=1
    
    #Limitado para 3 apenas para teste
    while j < 3:
       
        fname = "songs/Track " + str(j) + ".wav"
        wf = wave.open(fname, 'rb')
        data = wf.readframes(CHUNK)
        i=1
        while data:
            queue.put(data, True)
            data = wf.readframes(CHUNK)
        wf.close()
        j += 1
        if j==3:
            j=1

#Função que lida com a conexão e envia os dados para os clientes
def connection(connectionSocket, addr, queue):
    #wf = wave.open(fname, 'rb')
    #print("entrou no connection")
    #connectionSocket, addr = serverSocket.accept()
    print("Conexão vinda de {}".format(addr))

    
    while True:
        data = queue.get(True)
        connectionSocket.send(data)
    connectionSocket.close()        

def main():
    i = 1
    #o parâmetro de Queue não pode ser vazio, ou então a fila não terá limite e causará problemas de uso de memória
    q = Queue(1)
    th2 = threading.Thread(target=musicReading, args=(q, ))
    th2.start()
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("-----> Recebendo conexão pela {}a. vez! <-----".format(i))
        th = threading.Thread(target=connection, args=(connectionSocket, addr, q))
        
        th.start()
      
        i = i + 1
                	
if __name__ == '__main__':
	main()
