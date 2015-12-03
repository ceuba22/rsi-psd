# -*- coding: utf-8 -*-
from kafka import SimpleProducer, KafkaClient

class Produtor():

	def enviatupla(self, tp):

		kafka = KafkaClient('192.168.17.132:9092')
		producer = SimpleProducer(kafka)

		tupla = tp

		# Note that the application is responsible for encoding messages to type bytes
		
		if tupla[0] == "bittorrent":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'bittorrent', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "dhcp":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'dhcp', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "dns":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'dns', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "ftp":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'ftp', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "http":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'http', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "ssdp":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'ssdp', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "ssh":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'ssh', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "ssl":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'ssl', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

		if tupla[0] == "":
			# Note that the application is responsible for encoding messages to type bytes
			producer.send_messages(b'nenhum', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))
			producer.send_messages(b'todos', b'%s %s %s' % (tupla[1], tupla[2], tupla[3]))

#prod = Produtor()
#prod.enviatupla(("dns",10,20,30))
#prod.enviatupla(("ftp",40,50,60))
#prod.enviatupla(("http",10,20,30))
#prod.enviatupla(("ssh",10,20,30))
#prod.enviatupla(("noip",10,20,30))