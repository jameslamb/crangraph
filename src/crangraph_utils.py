#!/usr/bin/env python

# Grab imports
import re
import requests as rq
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import yaml

def get_metadata(pkg_name):
    """
    Given the name of a package on CRAN, hit GitHub and get the
    DESCRIPTION file. Return the DESCRIPTION contents as YAML
    """

    # Grab the description
    desc_url = "https://raw.githubusercontent.com/cran/{pkg_name}/master/DESCRIPTION".format(pkg_name=pkg_name)
    result = re.get(desc_url).contents

    # Return YAML version
    return(yaml.load(result))

def get_package_list():
    """
    Grab a list of all available packages on CRAN.
    Returns a dictionary keyed by package name.
    """

    # Grab package listing from CRAN
    result = rq.get("https://cran.r-project.org/web/packages/available_packages_by_name.html")

    # Parse out just the package name elements
    soup = BeautifulSoup(result.content, 'html.parser', parse_only = SoupStrainer("a"))
    package_html = soup.findAll('a', {'href': re.compile('index\.html$')})

    # Get dictionary of packages w/ links to their index files
    index_path = 'https://cran.r-project.org/web/packages/{pkg_name}/index.html'
    packages = {pkg_name.text: index_path.format(pkg_name = pkg_name.text) for pkg_name in package_html}

    return(packages)

def get_old_releases(pkg_name):
    """
    Given the name of a package on CRAN, hit that package's CRAN
    archive page to get a list of all releases.

    Returns a dictionary where keys are version numbers and values
    are release date-times.
    """

    # Grab list of releases
    archive_url = 'https://cran.r-project.org/src/contrib/Archive/{pkg}/'.format(pkg = pkg_name)
    result = rq.get(archive_url)

    # Parse list
    soup = BeautifulSoup(result.content, 'html.parser')
    release_nums  = soup.findAll('a', {'href': re.compile('tar\.gz$')})
    release_dates = soup.findAll(text = re.compile('^\d{4}-\d{2}-\d{2}'))

    # Clean up the releases
    releases_clean = [re.sub('^' + pkg_name + '_', '', release.text) for release in release_nums]
    releases_clean = [re.sub('\.tar\.gz$', '', release) for release in releases_clean]

    # Give back a dictionary 
    releases = {}
    for release_num, release_date in zip(releases_clean, release_dates):
        releases[release_num] = release_date.strip()

    return(releases)


def filter_version_reqs(pkg_dep_string):
    """
    Given R package listing in a DESCRIPTION file, potentially strip off
    version requirements.

    e.g. Turns "data.table (>= 1.0.1), ggplot2" to "data.table, ggplot2"
    """
    x = re.sub('\(>=\s+[0-9]*\.[0-9]*\)', '', pkg_dep_string)
    return(x)

def find_release_commit(pkg_name, pkg_version):
    """
    Given a package name and version, find the corresponding commit
    on the package's CRAN mirror repo on GitHub.
    """

    # Find URL to scrape
    skeleton = 'https://github.com/cran/{p}/releases/tag/{v}'
    release_page = skeleton.format(p = pkg_name, v = pkg_version)

    # Grab the source of the release page
    result = rq.get(release_page)
    
    # Parse and extract commit number
    soup = BeautifulSoup(result.content, 'html.parser')
    commit_string = soup.findAll('a', {'href': re.compile('/cran/' + pkg_name + '/commit/')})[0].text
    commit_string = commit_string.strip()
    return(commit_string)

def build_release_path(pkg_name, pkg_version):
    """
    Given a package name and version, return full URLs to package metadata
    on CRAN mirror.
    """

    # Get release commit
    commit_string = find_release_commit(pkg_name, pkg_version)

    # Build up a dictionary of paths
    base_url = 'https://raw.githubusercontent.com/cran/{pkg_name}/{commit}/'
    commit_url = base_url.format(pkg_name = pkg_name, commit = commit_string)

    # Plug in stuff
    pkg_metadata = {'DESCRIPTION': commit_url + 'DESCRIPTION',
                    'NAMESPACE'  : commit_url + 'NAMESPACE'}

    return(pkg_metadata)

def scrape_deps_from_description(description_text):
    """
    Given a raw DESCRIPTION file from an R package,
    return a dictionary with package dependencies.
    """

    # Grab all the imported packages
    description_text = description_text.split('\n')
    dep_text = ''
    accumulate = False
    for line in description_text:
        
        # Control accumulation (we want Imports and everything after until the next entry)
        if re.match(r'^Imports', line):
            accumulate = True
        elif re.match(r'^[A-Za-z]', line):
            accumulate = False
        
        # Build up all the Imports text
        if accumulate:
            dep_text += line.strip()
            
    # Clean up the text
    dep_text = re.sub('Imports: ', '', dep_text)
    deps = dep_text.split(',')
    deps = [filter_version_reqs(dep).strip() for dep in deps]

    return(set(deps))
