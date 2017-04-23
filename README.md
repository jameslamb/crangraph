# crangraph

## Project Overview

`crangraph` is an application which aims to visualize and make available data related to the interdepdencies between R packages available on the Comprehensive R Archive Network ([CRAN](https://cran.r-project.org/)).

## Background

This project was completed as part of the requirements of a course in UC-Berkeley's MIDS program, "W205: Storing and Retrieving Data".

## Setup

### 1. Create an EC2 instance

a. Create an EC2 instance using the `Amazon Linux AMI` (ami-c58c1dd3)
    - you should use at least a `t2.2xlarge` instance type
b. In the "Add Storage" stage of creating your AMI, add an EBS volume, general purpose SSD, with at least 80GB of storage
c. In the "Configure Security Group" stage, add the following rules:
    - (Custom TCP Rule) 4040, 0.0.0.0/0
    - (Custom TCP Rule) 5000, 0.0.0.0/0
    - (Custom TCP Rule) 7180, 0.0.0.0/0
    - (Custom TCP Rule) 7474, 0.0.0.0/0
    - (Custom TCP Rule) 8080, 0.0.0.0/0
    - (Custom TCP Rule) 8088, 0.0.0.0/0
    - (Custom TCP Rule) 50070, 0.0.0.0/0
    - (SSH) 22, 0.0.0.0/0
    - (HTTP) 80, 0.0.0.0/0
d. Other than the options above, use default settings given by AWS

### 2. Run Setup script

a. SSH into the EC2 instance you just created. This can be done with a command of the form:

    `ssh -i /path/to/my_keypair.pem ec2-user@ec2-174-129-53-252.compute-1.amazonaws.com`

b. Be sure that you are in home

    `cd $HOME`

c. Grab the setup script

    `curl https://raw.githubusercontent.com/jameslamb/crangraph/dev/setup/setup_instance.sh > setup_instance.sh`

d. Make this script executable:

    `chmod a+rwx setup_instance.sh`

e. This setup script is going to install all of the needed components for running this application, including Kafka, Postgres, Storm, and many others. Before these applications can be installed, the script needs to mount the EBS volume you created so that it can use that volume for storage. Execute the following:

    `sudo fdisk -l | grep ^Disk`

f. You will see a few lines of output that show disk size and the name of the volume. Use the disk size to identify the EBS volume you created. Note that this will not be exact...if you asked for 80 GB you may get a number like "85.9 GB". Here is an example output line that might represent a volume called `/dev/xvdb`:

    **Disk /dev/xvdb: 85.9 GB, 85899345920 bytes, 167772160 sectors**

g. Now that you've identified the name of your EBS volume (e.g. `/dev/xvdb`), run the setup script:

    `./setup_instance.sh <name_of_your_volume>`

h. The setup script is as automated as possible, but there are a few items which will need input from you. The prompts and the answers you should provide are given below. Answers wrapped in `<>` indicate keys (not literal commands).

    - *WARNING!! This will format the drive at /dev/xvdb. Press any key to continue or control-C to quit...*: **<ENTER>**
    - *In order to continue the installation process, please review the license agreement. Please, press ENTER to continue*: **<ENTER>**
    - *[misc. Anaconda license stuff]*: **d** until you hit the end
    - *Do you approve the license terms? [yes|no]*: **yes <ENTER>**
    - *Anaconda2 will now be installed into this location...*: **<ENTER>**
    - *Do you wish the installer to prepend the Anaconda2 install location to PATH in your /home/ec2-user/.bashrc ?*: **no <ENTER>**
    - 



1. Install Kafka
2. Install Storm
3. Install `lein`
4. Fetch this repo
5. From the root of this repo, run `make install_python`
6. Always work in this project's conda environment. Call `source activate crangraph` in all terminal shells

## Running the App

All instructions below assume that you have ssh'd into an AMI like the one described above.

1. Start up Kafka
2. Start the producer
3. Start up Storm

## Stopping the App

## UI access  to the app from the outside world



