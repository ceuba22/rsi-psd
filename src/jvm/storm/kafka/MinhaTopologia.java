package storm.kafka;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.testing.TestWordSpout;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import backtype.storm.utils.Utils;
import java.util.Map;
import storm.kafka.SpoutConfig;
import backtype.storm.spout.SchemeAsMultiScheme;
import storm.kafka.bolt.KafkaBoltTamanho;
import storm.kafka.bolt.KafkaBoltDuracao;
import storm.kafka.bolt.KafkaBoltTaxa;

public class MinhaTopologia {

//###################################################################################################//

	public static class TamanhoBolt extends BaseRichBolt {
		OutputCollector _collector;

		@Override
		public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
			_collector = collector;
		}

		@Override
		public void execute(Tuple tuple) {
			_collector.emit(tuple, new Values(classifica(tuple, 1)));
			_collector.ack(tuple);
		}

		public static String classifica(String tuple, int campo){
			String protocolo = new String()
			String animal = new String()
			String msg = new String()
			String valores[] = new String[4];
			valores = (tuple.split(" "));
			protocolo = valores[0]

			if (Integer.parseInt(valores[campo]) > 152) {
				animal = "elefante";
			} else{
				animal = "rato";
			}
			msg = protocolo+"/"+animal
			KafkaBoltTamanho kafkabolt = new KafkaBoltTamanho <null, String msg>() 
		}

		@Override
		public void declareOutputFields(OutputFieldsDeclarer declarer) {
			declarer.declare(new Fields("TamanhoBolt"));
		}
	}

//###################################################################################################//

	public static class DuracaoBolt extends BaseRichBolt {
		OutputCollector _collector;

		@Override
		public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
			_collector = collector;
		}

		@Override
		public void execute(Tuple tuple) {
		  
			_collector.emit(tuple, new Values(classifica(tuple, 2)));
			_collector.ack(tuple);
		}

		public static String classifica(String tuple, int campo){
			String protocolo = new String()
			String animal = new String()
			String msg = new String()
			String valores[] = new String[4];
			valores = (tuple.split(" "));
			protocolo = valores[0]

			if (Double.parseDouble(valores[campo])/60 > 12.0) {
				animal = "tartaruga";
			} else{
				animal = "libelula";
			}
			msg = protocolo+"/"+animal
			KafkaBoltDuracao kafkabolt = new KafkaBoltDuracao <null, String msg>() 
		}

		@Override
		public void declareOutputFields(OutputFieldsDeclarer declarer) {
			declarer.declare(new Fields("DuracaoBolt"));
		}
	}

//###################################################################################################//

	public static class TaxaBolt extends BaseRichBolt {
		OutputCollector _collector;

		@Override
		public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
			_collector = collector;
		}

		@Override
		public void execute(Tuple tuple) {
		  
			_collector.emit(tuple, new Values(classifica(tuple, 3)));
			_collector.ack(tuple);
		}

		public static String classifica(String tuple, int campo){
			String protocolo = new String()
			String animal = new String()
			String msg = new String()
			String valores[] = new String[4];
			valores = (tuple.split(" "));
			protocolo = valores[0]

			if (Double.parseDouble(valores[campo])/1000 > 101.0) {
				animal = "guepardo";
			} else{
				animal = "caramujo";
			}
			msg = protocolo+"/"+animal
			KafkaBoltTaxa kafkabolt = new KafkaBoltTaxa <null, String msg>() 
		}

		@Override
		public void declareOutputFields(OutputFieldsDeclarer declarer) {
			declarer.declare(new Fields("TaxaBolt"));
		}
	}

//###################################################################################################//

	public static void listen(TopologyBuilder builder,String endereco, String topicname, String spout) {
		BrokerHosts hosts = new ZkHosts(endereco);
		SpoutConfig spoutConfig = new SpoutConfig(hosts, topicname, " "+topicname, "discovery");
		spoutConfig.scheme = new SchemeAsMultiScheme(new StringScheme());
		KafkaSpout kafkaSpout = new KafkaSpout(spoutConfig);

		TopologyBuilder builder = new TopologyBuilder();
		builder.setSpout(spout, kafkaSpout);
		
		builder.setBolt("TAMANHO", new TamanhoBolt(), 3).shuffleGrouping(spoutsKafka);
		builder.setBolt("TAXA",new TaxaBolt(),3).shuffleGrouping(spoutsKafka);
		builder.setBolt("DURACAO", new DuracaoBolt(), 3).shuffleGrouping(spoutsKafka);
	}

//###################################################################################################//

	public static void main(String[] args) throws Exception {
		listen(builder,"172.16.206.184:2181","http","HttpSpout");
		listen(builder,"172.16.206.184:2181","bittorrent", "BitTorrentSpout");
		listen(builder,"172.16.206.184:2181","dhcp","DhcpSpout");
		listen(builder,"172.16.206.184:2181","ssdp","SsdpSpout");
		listen(builder,"172.16.206.184:2181","ssh","SshSpout");
		listen(builder,"172.16.206.184:2181","ssl","SslSpout");
		listen(builder,"172.16.206.184:2181","todos","TodosSpout");
		listen(builder,"172.16.206.184:2181","nenhum","NenhumSpout");
				 
		Config conf = new Config();
		conf.setDebug(true);

		if (args != null && args.length > 0) {
			conf.setNumWorkers(50);
			StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createTopology());
		} else {
			LocalCluster cluster = new LocalCluster();
			cluster.submitTopology("MinhaTopologia", conf, builder.createTopology());
		}
	}
}
