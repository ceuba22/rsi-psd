from kafka import KafkaConsumer
from threading import Thread

class Todos(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("todos",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Bittorrent(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("bittorrent",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Dhcp(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("dhcp",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Dns(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("dns",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Ftp(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("ftp",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Http(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("http",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Ssdp(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("ssdp",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Ssh(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("ssh",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Ssl(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("ssl",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

class Nenhum(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # To consume messages
        consumer = KafkaConsumer("",
                                 group_id='my_group',
                                 bootstrap_servers=['192.168.17.132:9092'])

        for message in consumer:
            # message value is raw byte string -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            parametros=message.value.split()
            size = float(parametros[0])
            timestamp = float(parametros[1])
            rate = float(parametros[2])
            print "%d fila %s - size:%.6f, timestamp:%.6f, rate:%.6f" % (message.offset, message.topic, size, timestamp, rate)

todos = Todos()
todos.start()

bittorrent = Bittorrent()
bittorrent.start()

dhcp = Dhcp()
dhcp.start()

dns = Dns()
dns.start()

ftp = Ftp()
ftp.start()

http = Http()
http.start()

ssdp = Ssdp()
ssdp.start()

ssh = Ssh()
ssh.start()

ssl = Ssl()
ssl.start()

nenhum = Nenhum()
nenhum.start()