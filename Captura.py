# -*- coding: cp1252 -*-
import time
import pcap, dpkt, re
import threading, Queue
from os import system
from LogDeErros import *
import sys
from Producer import *

class Captura():
	"""Classe que ira capturar pacotes"""
	def __init__(self):
		self.stats = "resume"
		self.log = LogDeErros()
		self.nomecoletor = ""
		self.noIPcount = 0
		self.UDPcount = 0
		self.TCPcount = 0
		self.nPkts=0
		self.producer = Produtor()
		self.fluxos={}

	def nomedocoletor(self,nome):
		self.nomecoletor = nome

	def status(self, arg):
		self.stats = arg
		print "Mudou status de captura para:", arg

	def assinar(self):
		file = open('l7-pat/dns.pat').readlines()
		expr = file[0]
		dns = re.compile(expr)
		file = open('l7-pat/ftp.pat').readlines()
		expr = file[0]
		ftp = re.compile(expr)
		file = open('l7-pat/http.pat').readlines()
		expr = file[0]
		http = re.compile(expr)
		file = open('l7-pat/ssh.pat').readlines()
		expr = file[0]
		ssh = re.compile(expr)
		file = open('l7-pat/bittorrent.pat').readlines()
		expr = file[0]
		bittorrent = re.compile(expr)
		file = open('l7-pat/dhcp.pat').readlines()
		expr = file[0]
		dhcp = re.compile(expr)
		file = open('l7-pat/ssdp.pat').readlines()
		expr = file[0]
		ssdp = re.compile(expr)
		file = open('l7-pat/ssl.pat').readlines()
		expr = file[0]
		ssl = re.compile(expr)

		assinaturas = {"dns":dns,"ftp":ftp,"http":http,"ssh":ssh,"bittorrent":bittorrent,"dhcp":dhcp,"ssdp":ssdp,"ssl":ssl}
		return assinaturas

	def capturateste(self):
		try:
			#pega assinaturas de prorocolos 
			self.protocols = self.assinar()
			#contadores
			cnt = {"nenhum":0,"dns":0,"ftp":0,"http":0,"ssh":0,"bittorrent":0,"dhcp":0,"ssdp":0,"ssl":0}
			tipo=""
			ti = 0
			for ts, pkt in pcap.pcap("test-capture.pcap"):
				if self.stats == "teste":
					tf = ts - ti
					ti = ts
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
							print "origem:",ipsrc,portsrc
							print "destino:",str(ipdst),portdest
							app = transp.data.lower()
							found = False
							for p in self.protocols.items():
								if p[1].search(app):
									cnt[p[0]] += 1
									found = True
									tipo = p[0]
							if (not found):
								cnt["nenhum"] += 1
					
					else:
						self.noIPcount += 1
						print "NonIP Pacote"

					tempo = tf
					tamanho = len(pkt)
					self.criatupla(tipo, tamanho, tempo)
					time.sleep(0.5)

				elif self.stats == "resume":
					self.captura()
				else:
					print "Coletor suspenso"
					system("clear")
			self.status("stop")
		except (KeyboardInterrupt, SystemExit):
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura de teste."
			self.status("stop")
			os._exit(0)

	def captura(self):
		try:
			#pega assinaturas de prorocolos 
			self.protocols = self.assinar()
			#contadores
			cnt = {"nenhum":0,"dns":0,"ftp":0,"http":0,"ssh":0,"bittorrent":0,"dhcp":0,"ssdp":0,"ssl":0}
			tipo=""
			for ts, pkt in pcap.pcap():
				if  self.stats == "resume":
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
							print "origem:",ipsrc,portsrc
							print "destino:",str(ipdst),portdest
							app = transp.data.lower()
							found = False
							for p in self.protocols.items():
								if p[1].search(app):
									cnt[p[0]] += 1
									found = True
									tipo = p[0]
							if (not found):
								cnt["nenhum"] += 1
							chave=str(ipsrc)+str(ipdst)+str(portsrc)+str(portdest)+str(tipo)
							if chave not in self.fluxos:
								self.fluxos[chave]=str(pkt)+"%&*"+str(ts)
					else:
						self.noIPcount += 1
						print "NonIP Pacote"


					fim=time.time()

					tempo = ts
					tamanho = len(pkt)

					self.criatupla(tipo, tamanho, tempo)

				if self.stats == "teste":
					self.capturateste()

				if self.stats == "stop":
					print "Coletor suspenso"
					print self.fluxos
					break
			print "sai"
		except (KeyboardInterrupt, SystemExit):
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)
			print "Erro ao fazer captura."
			os._exit(0)			

	def criatupla (self, tp, tam, temp):
		tipo = tp
		tempo = temp
		tempo = (tempo*0.001) 
		tamanho = tam
		tamanho = tam/1024.0
		if tempo != 0 and tamanho != 0:
			taxa = tamanho/tempo
			tupla = (tipo,"%.6f" % tamanho,"%.6f" % tempo,"%.6f" % taxa)
			print "Tupla gerada:", tupla
			time.sleep(2)
			#self.enviatupla(tupla)

	def enviatupla(self, tupla):
		try:
			self.producer.enviatupla(tupla)
		except:
			print "servidor de filas indisponivel"
			self.log.setErro(sys.exc_info()[1],self.nomecoletor)