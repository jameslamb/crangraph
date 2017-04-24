#!/bin/bash

# Break immediately if anything fails
set -e

# Create a `/bin` dir at home
if [ ! -d "$HOME/bin" ]; then
  mkdir $HOME/bin
fi

#### Install Git ####
if ! type "git" &> /dev/null; then
    
    echo "Installing Git..."

    # Install Git
    sudo yum install -y git-all

    # References:
    # [1] https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    echo "Completed installation of Git"
fi

#### Get project source code ####

    # Get the source code
    echo "Fetching application code from GitHub..."
    cd $HOME && \
    git clone https://github.com/jameslamb/crangraph && \
    cd crangraph && \
    git fetch origin dev && \
    git checkout dev
    echo "Completed fetching application code from GitHub."

#### Mount our EBS volume on /data ####
if [ ! -d "/data" ]; then
  
    cd $HOME

    echo "using drive " $1
    echo "WARNING!! This will format the drive at" $1
    read -rsp $'Press any key to continue or control-C to quit...\n' -n1 key

    # make a new ext4 filesystem on that EBS
    sudo mkfs.ext4 $1

    # mount the new filesystem under /data
    sudo mkdir /data
    sudo mount -t ext4 $1 /data
    sudo chmod a+rwx /data

    echo "Completed mounting EBS to /data."
fi



#### Install misc. system components ####

    echo "Installing gcc, openssl, and libffi-devel..."
    sudo yum install -y gcc-c++
    sudo yum install -y openssl-devel
    sudo yum install -y libffi-devel
    echo "Completed installation of miscellanous system components."

#### Install conda + Anaconda Python 2.7 ####

if ! type "conda" &> /dev/null; then

    echo "Installing conda..."

    # grab lein install source
    CONDA_SCRIPT="https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86_64.sh"
    curl $CONDA_SCRIPT > $HOME/install_conda.sh

    # Make it executable
    chmod a+rwx $HOME/install_conda.sh
    cd $HOME
    ./install_conda.sh

    # References:
    # [1] https://leiningen.org/#install
    echo "Completed installation of conda."
fi

#### Install lein ####
    
if ! type "lein" &> /dev/null; then

    echo "Installing leiningren..."

    # grab lein install source
    curl https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein > $HOME/bin/lein

    # Make it executable
    chmod a+rwx $HOME/bin/lein
    cd $HOME/bin
    ./lein

    # References:
    # [1] https://leiningen.org/#install
    echo "Completed installation of leiningren."
fi

#### Install Apache Storm ####

if ! type "storm" &> /dev/null; then

    echo "Installing Apache Storm...."

    # Download storm
    cd $HOME/bin
    STORMZIP="http://www-us.apache.org/dist/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz"
    wget $STORMZIP -O apache-storm-1.1.0.tar.gz
    tar -zxf apache-storm-1.1.0.tar.gz
    mkdir $HOME/bin/apache-storm-1.1.0/data

    # Replace the storm config file with our custom config
    echo "Replacing the Storm config with custom version..."
    cp $HOME/crangraph/setup/storm.yaml $HOME/bin/apache-storm-1.1.0/conf/storm.yaml

    # References:
    # [1] https://www.tutorialspoint.com/apache_storm/apache_storm_installation.html
    # [2] http://www.apache.org/dyn/closer.lua/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz
    echo "Completed installation of Apache Storm."

fi

#### Install kafka ####

if [ -z ${KAFKA_HOME+x} ]; then
    echo "Installing Apache Kafka..."

    # Download Kafka
    cd $HOME/bin
    KAFKAZIP="http://www-eu.apache.org/dist/kafka/0.10.1.1/kafka_2.10-0.10.1.1.tgz"
    wget $KAFKAZIP -O kafka_2.10-0.10.1.1.tgz
    tar -zxf kafka_2.10-0.10.1.1.tgz

    # Create KAFKA_HOME variable
    echo "export KAFKA_HOME=$HOME/bin/kafka_2.10-0.10.1.1" >> ~/.bashrc

    # References:
    # [1] http://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-
    # [2] https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm
    echo "Completed installation of Apache Kafka."
else 
    echo "Apache Kafka is already installed! KAFKA_HOME is set to '$KAFKA_HOME'";
fi

#### Install and start postgres ####

if ! type "psql" &> /dev/null; then

    echo "Installing PostgreSQL..."

    # Get postgres components
    sudo yum install -y postgresql
    sudo yum install -y postgresql-devel
    sudo yum install -y postgresql-server

    echo "Completed installation of Postgres."
    echo "Setting up Postgres..."

    # set up directories for postgres
    sudo mkdir /data/pgsql
    sudo mkdir /data/pgsql/data
    sudo mkdir /data/pgsql/logs

    # Create the postgres user
    if ! id -u postgres > /dev/null 2>&1; then
        sudo useradd postgres
    fi

    # Change permissions on /data/pgsql
    sudo chown postgres -R /data/pgsql
    sudo chmod 700 -R /data/pgsql

    # Initialize the DB
    sudo -u postgres initdb -D /data/pgsql/data

    # setup pg_hba.conf
    sudo chmod 777 -R /data/pgsql
    sudo -u postgres echo "host    all         all         0.0.0.0         0.0.0.0               md5" >> /data/pgsql/data/pg_hba.conf
    sudo -u postgres echo "listen_addresses = '*'" >> /data/pgsql/data/postgresql.conf
    sudo -u postgres echo "standard_conforming_strings = off" >> /data/pgsql/data/postgresql.conf
    sudo chown postgres -R /data/pgsql
    sudo chmod 700 -R /data/pgsql

    # Make start/stop scripts
    # make start postgres file
    # NOTE: These need to stay unindented to handle weird EOF thing
    cd /data
    cat > /data/start_postgres.sh <<EOF
sudo -u postgres pg_ctl -D /data/pgsql/data -l /data/pgsql/logs/pgsql.log start
EOF
    chmod +x /data/start_postgres.sh

    cat > /data/stop_postgres.sh <<EOF
#! /bin/bash
sudo -u postgres pg_ctl -D /data/pgsql/data -l /data/pgsql/logs/pgsql.log stop
EOF
    chmod +x /data/stop_postgres.sh

    #start postgres
    /data/start_postgres.sh

    echo "Completed setting up and starting PostgreSQL."
fi

#### Components needed to run Flask app ####

    echo "Installing components necessary to run Flask app.."

    # use nginx as a webserver
    sudo yum install -y nginx

    # Update nginx.conf
    sudo chown ec2-user -R /etc/nginx
    cp $HOME/crangraph/setup/nginx.conf /etc/nginx/nginx.conf

    # Update the server config
    python $HOME/crangraph/setup/sub_in_pub_dns.py
    cp $HOME/crangraph/setup/virtual.conf /etc/nginx/conf.d/virtual.conf

    # References:
    # [1] https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/
    # [2] http://nginx.org/en/docs/beginners_guide.html
    echo "Installation of Flask components complete."

#### Install python package and conda env ####

    # Set up variables (since Anaconda isn't on our path yet)
    CONDA_BIN="/home/ec2-user/anaconda2/bin"
    ACTIVATE_ALIAS="$CONDA_BIN/activate"
    DEACTIVATE_ALIAS="$CONDA_BIN/deactivate"
    CONDA_ENV_ALIAS="$CONDA_BIN/conda-env"

    # Create crangraph conda environment
    cd $HOME/crangraph/python && \
    $CONDA_ENV_ALIAS create -n crangraph -f crangraph.yml && \
    sudo pip install six==1.10.0 && \
    sudo python setup.py install
    
    # Install crangraph python package into that environment
    cd $HOME/crangraph/python && \
    source $ACTIVATE_ALIAS crangraph && \
    sudo python setup.py install && \
    source $DEACTIVATE_ALIAS crangraph

    # Add crangraph package to PYTHONPATH to be super sure
    echo "export PYTHONPATH=/home/ec2-user/crangraph/python:$PYTHONPATH" >> ~/.bashrc

# Setup path
echo "export PATH=$HOME/anaconda2/bin:$PATH:$HOME/bin:$HOME/bin/apache-storm-1.1.0/bin:$HOME/bin/kafka_2.10-0.10.1.1.tgz/bin" >> ~/.bashrc

