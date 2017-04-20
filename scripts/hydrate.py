#!/usr/bin/env python

## This script is used to pull all historical versions of all packages
#  and hydrate a historical data store with them.
#
#  Running this program writes out historical package dependency messages
#  to standard out. You can pipe them to an appropriate downstream sink
#  from the command line as you see fit

# Grab imports
import argparse
import requests as rq
import crangraph_utils as cg
import sys

# Set up command-line args
parser = argparse.ArgumentParser(description = 'Get metadata on historical package releases.')
parser.add_argument('--n_packages',
                    type = int,
                    default = -1,
                    help='Number of packages to pull. If not specified, all packages on CRAN will be used.')
args = parser.parse_args()

# Parse command line args to get number of packages to iterate over
packages = cg.get_package_list().keys()
if args.n_packages != -1:
    packages = [packages[i] for i in range(args.n_packages)]

# Packages to iterate over (PLACEHOLDER: just a few)
#packages = ['ggplot2', 'lubridate', 'plyr', 'data.table', 'MASS']

for pkg_name in packages:

    # Find all versions
    #sys.stdout.write('\nSearching for versions of ' + pkg_name + '...\n')
    pkg_versions = cg.get_old_releases(pkg_name)
    #sys.stdout.write('Found {n_ver} versions.\n'.format(n_ver = len(pkg_versions.keys())))

    # Iterate over versions
    for version in pkg_versions.keys():

        # Grab a DESCRIPTION file
        #sys.stdout.write('Grabbing the DESCRIPTION file for {pkg} v{ver}...\n'.format(pkg = pkg_name, ver = version))
        try:
            desc_url = cg.build_release_path(pkg_name, version)['DESCRIPTION']
            desc_text = rq.get(desc_url)
        except ValueError:
            error_response = {"package": pkg_name,
                              "version": version,
                              "found": False,
                              "release_dateTime": None,
                              "dependencies": None
                              }
            
            # Write out quarantined message and skip to next version
            sys.stdout.write(str(error_response))
            sys.stdout.write('\n')
            next
                         
        # parse dependencies
        deps = cg.scrape_deps_from_description(desc_text.content)

        # Format message to write out
        out_msg = {"package": pkg_name,
                   "version": version,
                   "release_dateTime": pkg_versions[version],
                   "dependencies": deps,
                   "found": True
                  }

        # Write to standard out
        sys.stdout.write(str(out_msg))
        sys.stdout.write('\n')