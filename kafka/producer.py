#!/usr/bin/env python

from kafka import KafkaProducer
import crangraph.crangraph_utils as cgu
import pickle
import sys
import time


# Set up producer running on localhost:9092
sys.stdout.write('Starting package metadata producer...\n')
metadata_producer = KafkaProducer(bootstrap_servers='localhost:9092')
sys.stdout.write('Producer running on localhost:9092\n')

# Get the packages!
while True:

    # Get all package dependencies
    sys.stdout.write('Refreshing package list...\n')
    package_names = cgu.get_package_list()
    sys.stdout.write('Found {n} packages on CRAN\n'.format(n = len(package_names)))

    # Go through them and grab their description files from the interwebs
    for pkg_name in package_names:

        # Get description file for current version
        sys.stdout.write('Grabbing metadata for ' + pkg_name + '\n')
        desc = cgu.get_metadata(pkg_name)

        # Write out to Kafka
        try:
            byte_output = pickle.dumps((pkg_name, desc))
            metadata_producer.send('package_metadata', byte_output)
        except Exception as e:
            sys.stdout.write(str(e) + '\n')

        # Slow the app down while we're in testing mode
        time.sleep(5)

    sys.stdout.write('done\n\n')