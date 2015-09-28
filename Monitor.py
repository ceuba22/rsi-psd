# -*- coding: cp1252 -*-
from socket import *
import threading
import Queue
import os

class Monitor(threading.Thread):
	def __init__(self):
		super(Monitor, self).__init__()
		self.serverPort = 12000 # Porta que o servidor vai monitorar
		self.serverSocket = socket(AF_INET, SOCK_DGRAM) #Cria o Socket UDP (SOCK_DGRAM) para rede IPv4 (AF_INET)
		self.listadecoletores=[]
		self.stoprequest = threading.Event()

	def run(self):
		self.serverSocket.bind(('', self.serverPort)) #Associa o Socket criado com a porta desejada

		while not self.stoprequest.isSet():
			message, clientAddress = self.serverSocket.recvfrom(2048) #Aguarda receber dados do socket
			nome, clientAddress = self.serverSocket.recvfrom(2048) #Aguarda receber dados do socket
			if message.upper() == "ADICIONAR":
				if not clientAddress in self.listadecoletores:
					self.listadecoletores.append((nome, clientAddress))
					print "Novo coletor adicionado. Seu nome e endereço é:",(nome,clientAddress[0])
				else:
					print "O coletor já estava adicionado."
				returnMessage = "adicionado"
				self.serverSocket.sendto(returnMessage, clientAddress)
			else:
				print(clientAddress)
				print "tentou acionar um comando"
				returnMessage = "Comando Invalido"
				self.serverSocket.sendto(returnMessage, clientAddress)

			print("\nMonitor ON. Digite o numero correspondente as opções:")
			print("\n1-Retomar coleta de pacotes\n2-Parar coleta de pacotes\n3-Baixar log de erros\n4-SAIR\n\n")

		self.serverSocket.close()

	def stop(self):
		self.stoprequest.set()

	def coletar(self, clientAddress):
		returnMessage = "coletar"
		self.serverSocket.sendto(returnMessage, clientAddress)

	def coletarteste(self, clientAddress):
		returnMessage = "coletarteste"
		self.serverSocket.sendto(returnMessage, clientAddress)

	def suspender(self, clientAddress):
		returnMessage = "parar"
		self.serverSocket.sendto(returnMessage, clientAddress)

	def log(self, clientAddress):
		returnMessage = "log"
		self.serverSocket.sendto(returnMessage, clientAddress)

	def listarcoletores(self):
		n = 1
		print "Coletores ativos:"
		for i in self.listadecoletores:
			print str(n)+'-'+i[0]
			n = n + 1

	def retornaip(self, n):
		ip = self.listadecoletores[n-1][1]
		return ip


def main():
	try:
		monitor = Monitor()
		monitor.start()
		print("\nMonitor ON. Digite o numero correspondente as opções:")

		#######  Menu de Principal  #######
		while 1:
			opcao=raw_input("\n1-Retomar coleta de pacotes\n2-Parar coleta de pacotes\n3-Baixar log de erros\n4-SAIR\n\n")

			#######  Menu de Captura  #######
			if opcao == "1":
				print("\nMenu de captura. Digite o numero correspondente as opções:")
				opcao=raw_input("\n1-Reiniciar captura na rede\n2-Iniciar captura de teste\n\n")
				if opcao == "1":
					if not monitor.listadecoletores:
						print "\nNenhum coletor na rede."
					else:
						print "\nIniciada uma coleta de pacotes..."
						monitor.listarcoletores()
						n = input("Digite o número correspondente ao coletor desejado\n")
						ip = monitor.retornaip(n)
						monitor.coletar(ip)

				elif opcao == "2":
					print "\nIniciada uma coleta de pacotes..."
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)
					monitor.coletarteste(ip)
				else:
					print "Opção inválida"

			#######  Menu de Suspensão  #######
			elif opcao == "2":
				if not monitor.listadecoletores:
					print "\nNenhum coletor na rede."
				else:
					print "\nParando coleta de Pacotes"
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)
					monitor.suspender(ip)

			#######  Menu de Logs  #######
			elif opcao == "3":
				if not monitor.listadecoletores:
					print "\nNenhum coletor na rede."
				else:
					print "\nBaixando log..."
					monitor.listarcoletores()
					n = input("Digite o número correspondente ao coletor desejado\n")
					ip = monitor.retornaip(n)
					monitor.log(ip)

			#######  SAIR  #######
			elif opcao == "4":
				monitor.stop()
				os._exit(0)
			else:
				print "Opção inválida"

	except (KeyboardInterrupt, SystemExit):
		monitor.stop()
		os._exit(0)
		
if __name__ == '__main__':
	main()