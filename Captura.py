# -*- coding: cp1252 -*-
import time
import pcap, dpkt, re
import threading, Queue
from os import system
from LogDeErros import *

class Captura():
	"""Classe que ira capturar pacotes"""
	def __init__(self):
		self.stats = "run"

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
		#pega assinaturas de prorocolos 
		protocols = self.assinar()
		#contadores
		cnt = {"noClass":0,"dns":0,"ftp":0,"http":0,"ssh":0}
		cNonIP = 0
		nPkts=0
		for ts, pkt in pcap.pcap("dns.pcap"):
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
					for p in protocols.items():
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
		print "O resultado da coleta de teste ira desaparecer em 10 segundos"
		time.sleep(10)
		self.status("stop")

	def captura(self):
		try:	
			#pega assinaturas de prorocolos 
			protocols = self.assinar()
			#contadores
			cnt = {"noClass":0,"dns":0,"ftp":0,"http":0,"ssh":0}
			cNonIP = 0
			nPkts=0

			for ts, pkt in pcap.pcap():
				if self.stats == "run" or self.stats == "resume":
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
							for p in protocols.items():
								if p[1].search(app):
									cnt[p[0]] += 1
									found = True
							if (not found):
								cnt["noClass"] += 1
					else:
						cNonIP += 1

				elif self.stats == "teste":
					self.capturateste()

				else:
					system("clear")
					print "Coleta da rede:\n"
					for p in cnt.items():
						print(p[0]+" Pkts:"+str(p[1]))
					print("Non IP Pkts:"+str(cNonIP))
		except:
			self.erro.setError(sys.exc_info()[1],self.nomeColetor)