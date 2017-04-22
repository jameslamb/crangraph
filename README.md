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
    - (Custom TCP Rule) 50070, 0.0.0.0/0
    - (Custom TCP Rule) 8080, 0.0.0.0/0
    - (Custom TCP Rule) 7180, 0.0.0.0/0
    - (Custom TCP Rule) 8088, 0.0.0.0/0
    - (Custom TCP Rule) 7474, 0.0.0.0/0
    - (SSH) 22, 0.0.0.0/0
    - (HTTP) 80, 0.0.0.0/0
d. 

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



