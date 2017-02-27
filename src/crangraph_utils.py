#!/usr/bin/env python


def get_metadata(pkg_name):
    """
    Given the name of a package on CRAN, hit GitHub and get the
    DESCRIPTION file. Return the DESCRIPTION contents as YAML
    """
    import requests
    import yaml

    # Grab the description
    desc_url = "https://raw.githubusercontent.com/cran/{pkg_name}/master/DESCRIPTION".format(pkg_name=pkg_name)
    result = requests.get(desc_url).contents

    # Return YAML version
    return(yaml.load(result))


def parse_dependencies(pkg_metadata):
    """
    Given package metadata from a DESCRIPTION file, return a
    list of dependency packag
    """
    pass


def get_commits(pkg_name):
    """
    Given the name of a package on CRAN, hit GitHub API and get a list
    of all commit hashes on the master branch at the CRAN mirror repo
    for that package.
    """
    pass


def filter_version_reqs(pkg_dep_string):
    """
    Given R package listing in a DESCRIPTION file, potentially strip off
    version requirements.

    e.g. Turns "data.table (>= 1.0.1), ggplot2" to "data.table, ggplot2"
    """
    import re
    x = re.sub('\(>=\s+[0-9]*\.[0-9]*\)', '', pkg_dep_string)
    return(x)
