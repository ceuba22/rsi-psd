# -*- coding: cp1252 -*-
from socket import *
from Captura import *

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
serverAddress = ""
serverName = '<broadcast>'
message= ""

while 1:
    #Recebe mensagem do usuario e envia ao destino
    message = raw_input('Digite "descoberta" para parear com o servidor\n>>>')
    if message.upper() == "DESCOBERTA":
    	clientSocket.sendto(message,(serverName, serverPort)) #envia mensagem para o server
    	returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno
    	print("\nServidor: "+returnMessage)
    	break
    else:
    	print "Comando invalido"

while 1:
	print "Aguandando ordens do Monitor"
	returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno
	print("\nServidor: "+returnMessage)
	if returnMessage.upper() == "COLETAR": 
		print "\nColetando Pacotes..."
		captura = Captura()
		captura.captura()
		clientSocket.sendto("\nColeta de pacotes terminada.",(serverName, serverPort)) #envia mensagem para o server

	elif returnMessage.upper() == "CLASSIFICAR": 
		print "\nClassificando Pacotes..."
		returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno
	elif returnMessage.upper() == "LOG": 
		print "\nAbrindo Log..."
		returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno

clientSocket.close()
