#!/bin/env python

# This small program asks a command-line user to provide the public DNS for their EC2 instance, then subs that name into the config for nginx (our webserver)
import os
import re

ec2_dns = raw_input("Please enter the public DNS name of your EC2 instance: ")


# Read in the file
with open('$HOME/crangraph/setup/virtual.conf', 'r') as file :
  in_file = file.read()

# Replace the target string
file_contents = in_file.replace('~~AWS_EC2_PUBLIC_DNS~~', ec2_dns)

# Write the file out again
with open('$HOME/crangraph/setup/virtual.conf', 'w') as file:
  file.write(file_contents)