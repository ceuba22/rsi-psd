# -*- coding: cp1252 -*-
import os, time
from socket import *
import pcap, dpkt, re
import threading, Queue
from Captura import *
from LogDeErros import *

class Coletor(threading.Thread):

	def __init__(self):
		super(Coletor, self).__init__()
		self.stoprequest = threading.Event()
		self.capt = Captura()
		self.nomecoletor = "aluizio"

	def run(self):
		while not self.stoprequest.isSet():
			self.capt.captura()

	def stop(self):
		self.stoprequest.set()
		self.capt.status("stop")

	def resume(self):
		self.stoprequest.clear()
		self.capt.status("resume")

	def teste(self):
		self.stoprequest.clear()
		self.capt.status("teste")

	def log(self):
		self.stoprequest.set()
		self.capt.status("download")

def main():
	coletor = Coletor()
	serverPort = 12000
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	serverAddress = ""
	serverName = '<broadcast>'
	message= ""

	while True:
		message = "adicionar"
		clientSocket.sendto(message,(serverName, serverPort)) #envia mensagem para o server
		message = coletor.nomecoletor
		clientSocket.sendto(message,(serverName, serverPort)) #envia mensagem para o server
		returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno
		if returnMessage.upper() == "ADICIONADO":
			print "O coletor foi adicionado\n"
			break

	coletor.start()

	while True:
		print "Aguandando ordens do Monitor\n"
		returnMessage, serverAddress = clientSocket.recvfrom(2048) #Aguarda mensagem de retorno
		if returnMessage.upper() == "COLETAR":
			coletor.resume()
		if returnMessage.upper() == "COLETARTESTE":
			coletor.teste()
		if returnMessage.upper() == "PARAR":
			coletor.stop()
		if returnMessage.upper() == "LOG":
			coletor.log()
	clientSocket.close()

if __name__ == '__main__':
	main()