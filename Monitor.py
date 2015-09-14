# -*- coding: cp1252 -*-
from socket import *

serverPort = 12000 # Porta que o servidor vai monitorar
serverSocket = socket(AF_INET, SOCK_DGRAM) #Cria o Socket UDP (SOCK_DGRAM) para rede IPv4 (AF_INET)
serverSocket.bind(('', serverPort)) #Associa o Socket criado com a porta desejada
listadecoletores=[]

print("\nMonitor ON. Digite o numero correspondente as opções:")
while 1:
    opcao=raw_input("\n1-Monitorar requisições de novos coletores\n2-Iniciar coleta de pacotes\n3-Classificar a ultima coleta de pacotes\n4-abrir log de erros\n5-Sair\n\n")
    if opcao == "1":
        while 1:
            try:
                print "\nMonitorando requisições de coletores...Press Ctrl+C para sair"
                message, clientAddress = serverSocket.recvfrom(2048) #Aguarda receber dados do socket
                if message.upper() == "DESCOBERTA":
                    if not clientAddress in listadecoletores:
                        listadecoletores.append(clientAddress)
                        print "Novo coletor adicionado."
                    returnMessage = "O coletor adicionado."
                    serverSocket.sendto(returnMessage, clientAddress)
                else:
                    print(clientAddress)
                    print "tentou acionar um comando"
                    returnMessage = "Comando Invalido"
                    serverSocket.sendto(returnMessage, clientAddress)
            except (KeyboardInterrupt, SystemExit):
                break
    elif opcao == "2":
        if not listadecoletores:
            print "\nNenhum coletor na rede."
        else:
            print "\nColetando Pacotes..."
            returnMessage = "coletar"
            serverSocket.sendto(returnMessage, clientAddress)
            message, clientAddress = serverSocket.recvfrom(2048) #Aguarda receber dados do socket
            print message
    elif opcao == "3":
        print "\nClassificando Pacotes"
        returnMessage = "classificar"
        serverSocket.sendto(returnMessage, clientAddress)
    elif opcao == "4":
        if not listadecoletores:
            print "\nNenhum coletor na rede."
        else:
            print "\nEm construção..."
            #returnMessage = "log"
            #serverSocket.sendto(returnMessage, clientAddress)
    elif opcao == "5":
        break
    else:
        print "Opção inválida"

serverSocket.close()

