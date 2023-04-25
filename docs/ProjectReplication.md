# Project Replication
---                                         
>## Execute the below on your LOCAL MACHINE
<br>

### ***REQUIREMENTS*** - Local Machine
---
* GCP Account

* Google SDK: Download from [here](https://cloud.google.com/sdk/docs/downloads-interactive#linux-mac)

    >NOTE: Don't do the `gcloud init` initialization step just yet

* Terraform: Download from [here](https://developer.hashicorp.com/terraform/downloads)

* Make: 
    - Windows: Install via  Chocolatey 
    - Linux: `sudo apt install make`

### ***CREATING GCP PROJECT VIA CLI & TERRAFORM***
---
1. Clone the project on your local machine
    ```bash
        git clone https://github.com/sanyassyed/sf_eviction.git
        cd sf_eviction
    ```
1. Rename `env_boilerplate` file to .env

1. **Create the GCP Project named sf-eviction-2023:** by executing the below from the `sf_eviction` project folder in the terminal. [GCP Documentation](https://cloud.google.com/sdk/docs)

    ```bash
        # Follow instructions to setup your project and do the intial project setup
        gcloud init --no-browser --skip-diagnostics
        # Select Option 2 - Create a new configuration
        # Enter configuration name (enter the project name here): sf-eviction
        # Choose the account you would like to use to perform operations for this configuration: 1 (your gmail account)
        # Pick cloud project to use: (Create new project)
        # Please enter project id: sf-eviction-2023

        # To check that all is configured correctly and that your CLI is configured to use your created project use the command
        gcloud info
    ```
1. **SSH Key Creation** : Generate ssh keys which will be used to connect to the VM [Official Documentation](https://cloud.google.com/compute/docs/connect/create-ssh-keys)
    
    ```bash
        cd ~/.ssh
        ssh-keygen -t rsa -f ~/.ssh/id_eviction -C project_user -b 2048
        # Remember the passphrase as you need it when sshing into the machine
    ```
    Now two keys should be created in the .ssh folder id_eviction (private key) and id_eviction.pub (public key)

1. **Setting env variables:** Use the default values or add the following values to your .env file
    * GCP_PROJECT_ID - if the name is different from `sf-eviction-2023`
    * GCP_SERVICE_ACCOUNT_NAME - name to assign to your service account. Default is set to `sf-eviction-editor`
    * GCP_REGION - the region for your project. Default is set to `us-central1`
    * GCP_ZONE - the zone for your project. Default is set to `us-central1-c`

1. **[Enable billing:](https://support.google.com/googleapi/answer/6158867?hl=en)** for this project on the GCP Console
1. **Setup Access:** Enable API's, Create Service Account, Setup Access via IAM Roles & Download Credentials by executing the below commands. **NOTE: This command will take time to execute**

    ```bash
        cd ~/sf_eviction
        # set the environment variables from the .env file
        set -o allexport && source .env && set +o allexport
        make gcp-set-all
    ```
1. **Build the Project Infrastructure** via Terraform as follows 
    ```bash
        # run terrafrom from sf_eviction project root directory
        terraform -chdir=terraform init
        terraform -chdir=terraform plan
        terraform -chdir=terraform apply
    ```
1. Now check the project on GCP Console to make sure the following resources are created
    * Cloud Storage - 1 Google Storage Bucket named `data-lake-sf-eviction-2023-final`
    * BigQuery - 3 Datasets named `raw`, `dev` and `prod`
    * Compute Instance - 1 VM named `eviction-vm`

1. Start the VM from the local machine via CLI and get the External IP
    ```bash
        gcloud compute instances start $GCP_COMPUTE_ENGINE_NAME --zone $GCP_ZONE --project $GCP_PROJECT_ID
    ```
1. SSH into VM as follows:
    ```bash
        ssh -i ~/.ssh/id_eviction $GCP_COMPUTE_ENGINE_SSH_USER@external_ip
    ```
---
<br>
<br>

>## Execute the below on the VM we just started
<br>

### ***CREATING A PIPELINE ON THE VM***
---
1. Clone the Project repo on the VM
    ```bash
    git clone https://github.com/sanyassyed/sf_eviction.git && cd sf_eviction
    ```

1. Rename the file `env_boilerplate` on the VM to `.env`
    ```bash
    mv env_boilerplate .env
    ```

1. Copy the variables from your local machine's `sf_eviction/.env` file to the `sf_eviction/.env` file on the VM.

### ***REQUIREMENTS*** - Virtual Machine
---
Below are the required Applications & API's needed for this project and the instructions to install them on the VM.

1. Make & Screen: Install the `make` & `screen` software as follows:

    ```bash
        cd ~ && sudo apt install make && sudo apt install screen
    ```
1. Java, Spark & Miniconda: We are going to install these using the Makefile which is in the `sf_eviction`

    ```bash
        # goto project directory
        cd sf_eviction
        # install java, spark & miniconda in the system ~ as follows
        make -C ~ -f sf_eviction/Makefile install-sw
        # activate & initialize conda
        eval "$(~/miniconda/bin/conda shell.bash hook)" && conda init
        source ~/.bashrc
    ```
1. Virtual conda env with pip : Install the virtual conda env with pip and python 3.10.9 as follows
    ```bash
        conda create --prefix ./.my_env python=3.10.9 pip
        conda activate .my_env/
        pip install -r requirements.txt
    ```

### ***API REQUIREMENTS***
---
* SODU API Keys:
    - `API_KEY_ID` & `API_KEY_SECRET` are needed for extracting Eviction data for this project. Find the instructions [here](docs/info_api.md) to get your key.
* PREFECT CLOUD API:
    - Get your Prefect API Key by following instructions [here](info_api.md) 
* Add the keys to the .env file
* Copy the  `credentials/gcp-credentials.json` file from your local system to vm in the same location.

### ***SCHEDULING & RUNNING THE INGESTION PIPELINE***
---
1. Log into Prefect Cloud
    ```bash
        set -o allexport && source .env && set +o allexport
        prefect cloud login -k $PREFECT_CLOUD_API
    ```
    **Now you can use the Prefect cloud to register blocks and run your flows**

1. Create Prefect Blocks & Deploy via code. You can view the execution of the below code in your Prefect Cloud account
    ```bash
        # Run the create_prefect_blocks.py and register the block
        prefect block register --file flows/create_prefect_blocks.py
        python flows/deploy_ingest.py
        # on VM start the agent in detached mode
        screen -A -m -d -S prefectagent prefect agent start --work-queue "development"
        # force run the deployment for testing or ignore the below if you want to run it on schedule
        prefect deployment run ParentFlow/etl_web_to_gcp
        # Stop the prefect agent 
        screen -r prefectagent
        Ctrl + C
        prefect cloud logout
    ```
1. Now there should be 
    1. raw and clean data available on GCS and 
    2. clean data available in the tables `eviction_external` & `eviction` in the dataset `raw` on BQ.
    3. transformed data in the `stg_eviction` & `fact_eviction` in the `production`/`staging` dataset depending on which enviroment you are working in.

### ***SHUTDOWN VM***
---
```bash
# shutdown / stop the VM
sudo shutdown now
```

### ***DESTROY THE INFRASTRUCTURE ON GCP***
---
**On your local machine** in the project folder `sf_eviction` destroy the GCP infrastructure as follows

```bash
    terraform -chdir=terraform destroy
```