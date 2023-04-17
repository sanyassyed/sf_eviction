install-java:
	mkdir spark
	wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz -P ~/spark
	tar xzfv ~/spark/openjdk-11.0.2_linux-x64_bin.tar.gz -C ~/spark/
	echo 'export JAVA_HOME="${HOME}/spark/jdk-11.0.2"' >> ~/.bashrc
	echo 'export PATH="${JAVA_HOME}/bin:${PATH}"' >> ~/.bashrc
	rm ~/spark/openjdk-11.0.2_linux-x64_bin.tar.gz

install-spark:
	wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz -P ~/spark
	tar xzfv ~/spark/spark-3.3.2-bin-hadoop3.tgz -C ~/spark/
	rm ~/spark/spark-3.3.2-bin-hadoop3.tgz
	echo 'export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"' >> ~/.bashrc
	echo 'export PATH="${SPARK_HOME}/bin:${PATH}"' >> ~/.bashrc

install-miniconda:
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
	bash ~/miniconda.sh -b -p ${HOME}/miniconda
	rm ~/miniconda.sh
	eval "$$(~/miniconda/bin/conda shell.bash hook)"
	conda init
	. ~/.bashrc

install-sw:
	make -C ~ install-miniconda && \
	make -C ~ install-java && \
	make -C ~ install-spark

enable-apis:
	gcloud services enable \
	iam.googleapis.com \
	compute.googleapis.com \
	bigquery.googleapis.com 

create-sa:
	gcloud iam service-accounts \
	create ${GCP_SERVICE_ACCOUNT_NAME} --display-name="Master Service Account"

add-access:
	gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/storage.admin' && \
	gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/storage.objectAdmin' && \
    gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/bigquery.admin' && \
    gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/compute.instanceAdmin' && \
    gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/viewer' && \
    gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/iam.serviceAccountUser' && \
    gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
	--member='serviceAccount:'"${GCP_SERVICE_ACCOUNT_NAME}"'@'"${GCP_PROJECT_ID}"'.iam.gserviceaccount.com' \
	--role='roles/compute.osLoginExternalUser 

get-key:
	gcloud iam service-accounts keys create \
	${LOCAL_SERVICE_ACCOUNT_CREDENTIAL_PATH} \
	--iam-account=${GCP_SERVICE_ACCOUNT_NAME}@${GCP_PROJECT_ID}.iam.gserviceaccount.com

gcp-set-all:
	make enable-apis && \
	make create-sa && \
	make add-access && \
	make get-key

# make install-sw
# make gcp-set-all