install-java:
	mkdir spark
	wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz -P ~/spark
	tar xzfv ~/spark/openjdk-11.0.2_linux-x64_bin.tar.gz -C ~/spark/
	export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
	export PATH="${JAVA_HOME}/bin:${PATH}"
	rm ~/spark/openjdk-11.0.2_linux-x64_bin.tar.gz
install-spark:
	wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz -P ~/spark
	tar xzfv spark-3.3.2-bin-hadoop3.tgz -C ~/spark/
	rm ~/spark/spark-3.3.2-bin-hadoop3.tgz
	export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
	export PATH="${SPARK_HOME}/bin:${PATH}"