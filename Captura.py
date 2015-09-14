import pcap, dpkt, re

class Captura():

    def captura(self):
		#assinaturas de protocolos de camada de aplicacao
		expr="^[\x01\x02][\x01- ]\x06.*c\x82sc"
		dhcp = re.compile(expr)
		expr="^(\x13bittorrent protocol|azver\x01$|get /scrape\?info_hash=)"
		bittorrent = re.compile(expr) 

		protocols = {"dhcp":dhcp,"bittorrent":bittorrent}
		#contadores
		cnt = {"dhcp":0,"bittorrent":0,"noClass":0}
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









