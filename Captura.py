# -*- coding: cp1252 -*-
import time
import pcap, dpkt, re
import threading, Queue
from os import system
from LogDeErros import *
import sys

class Captura():
	"""Classe que ira capturar pacotes"""
	def __init__(self):
		self.stats = "run"
		self.log = LogDeErros()
		self.nomecoletor = ""
		self.noIPcount = 0
		self.UDPcount = 0
		self.TCPcount = 0
		self.nPkts=0

	def nomedocoletor(self,nome):
		self.nomecoletor = nome

	def status(self, arg):
		self.stats = arg
		print "Mudou status de captura para:", arg

	def assinar(self):
		file = open('l7-pat/dns.pat').readlines()
		expr = file[1]
		dns = re.compile(expr)
		file = open('l7-pat/ftp.pat').readlines()
		expr = file[1]
		ftp = re.compile(expr)
		file = open('l7-pat/http.pat').readlines()
		expr = file[1]
		http = re.compile(expr)
		file = open('l7-pat/ssh.pat').readlines()
		expr = file[1]
		ssh = re.compile(expr)
		assinaturas = {"dns":dns,"ftp":ftp,"http":http,"ssh":ssh}
		return assinaturas

	def capturateste(self):
		try:
			#pega assinaturas de prorocolos 
			self.protocols = self.assinar()
			#contadores
			cnt = {"noClass":0,"dns":0,"ftp":0,"http":0,"ssh":0}
			cNonIP = 0
			nPkts=0
			for ts, pkt in pcap.pcap("test-capture.pcap"):
				nPkts = nPkts + 1
				eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
				ip = eth.data

				#imprimindo pacotes 
				print("Pacote puro #"+str(nPkts))
				print(dpkt.hexdump(pkt))
				print("Mostrando o pacote #"+str(nPkts))
				print(ts, repr(eth))
				print("Mostrando o endereco de destino do pacote #"+str(nPkts))
				print(repr(eth.dst))
				print("\n")

				if isinstance(ip,dpkt.ip.IP):
					transp = ip.data
					if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
						app = transp.data.lower()
						found = False
						for p in self.protocols.items():
							if p[1].search(app):
								cnt[p[0]] += 1
								found = True
						if (not found):
							cnt["noClass"] += 1
				else:
					cNonIP += 1

			for p in cnt.items():
				print(p[0]+" Pkts:"+str(p[1]))
			print("Non IP Pkts:"+str(cNonIP))
			time.sleep(2)
			self.status("stop")
		except:
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura de teste."
			self.status("stop")

	def captura(self):
		try:
			#pega assinaturas de prorocolos 
			self.protocols = self.assinar()
			#contadores
			cnt = {"noClass":0,"dns":0,"ftp":0,"http":0,"ssh":0}
			tipo=""

			for ts, pkt in pcap.pcap():
				if self.stats == "run" or self.stats == "resume":
					inicio=time.time()
					eth = dpkt.ethernet.Ethernet(pkt)
					ip = eth.data

					if isinstance(ip,dpkt.ip.IP):
						transp = ip.data
						if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
							if isinstance(ip.data,dpkt.tcp.TCP):
								self.TCPcount += 1
							elif isinstance(ip.data,dpkt.udp.UDP):
								self.UDPcount += 1
								
							ipsrc = ip.src
							ipdst = ip.dst
							portsrc = ip.data.dport
							portdest = ip.data.sport
							print "\nTrafego do pacote:"
							print "origem:",str(ipsrc),portsrc
							print "destino:",str(ipdst),portdest
							app = transp.data.lower()
							found = False
							for p in self.protocols.items():
								if p[1].search(app):
									cnt[p[0]] += 1
									found = True
							if (not found):
								cnt["noClass"] += 1
							tipo = p[0]
					
					else:
						self.noIPcount += 1
						print "NonIP Pacote"


					fim=time.time()

					tempo = fim - inicio
					tamanho = len(pkt)

					self.criatupla(tipo, tamanho, tempo)

				elif self.stats == "teste":
					self.capturateste()

				else:
					print "Coletor suspenso"
		except:
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura."
			self.status("stop")			

	def criatupla (self, tp, tam, temp):
		tipo = tp
		tempo = temp
		tempo = (tempo*0.001) 
		tamanho = tam
		tamanho = tam/1024.0
		if tempo != 0 and tamanho != 0:
			taxa = tamanho/tempo
		item = (tipo,tamanho,tempo,taxa)
		tupla = (tipo,item)
		print "Tupla gerada:", tupla

	def enviatupla(self, tupla):
		pass
		####Implemente aqui a função para
		####enviar a tupla ao servidor de filas