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

def get_package_list():
    """
    Grab a list of all available packages on CRAN.
    Returns a dictionary keyed by package name.
    """

    # Load Dependencies
    import requests as rq
    from bs4 import BeautifulSoup
    from bs4 import SoupStrainer
    import re

    # Grab package listing from CRAN
    result = rq.get("https://cran.r-project.org/web/packages/available_packages_by_name.html")

    # Parse out just the package name elements
    soup = BeautifulSoup(result.content, 'html.parser', parse_only = SoupStrainer("a"))
    package_html = soup.findAll('a', {'href': re.compile('index\.html$')})

    # Get dictionary of packages w/ links to their index files
    index_path = 'https://cran.r-project.org/web/packages/{pkg_name}/index.html'
    packages = {pkg_name.text: index_path.format(pkg_name = pkg_name.text) for pkg_name in package_html}

    return(packages)



def parse_dependencies(pkg_metadata):
    """
    Given package metadata from a DESCRIPTION file, return a
    list of dependency packag
    """
    pass


def get_old_releases(pkg_name):
    """
    Given the name of a package on CRAN, hit that package's CRAN
    archive page to get a list of all releases.

    Returns a dictionary where keys are version numbers and values
    are release date-times.
    """

    # Load Dependencies
    import requests as rq
    from bs4 import BeautifulSoup
    from bs4 import SoupStrainer
    import re

    # Grab list of releases
    archive_url = 'https://cran.r-project.org/src/contrib/Archive/{pkg}/'.format(pkg = pkg_name)
    release_page = rq.get(archive_url)

    # Parse list
    release_nums = soup.findAll('a', {'href': re.compile('tar\.gz$')})
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
    import re
    x = re.sub('\(>=\s+[0-9]*\.[0-9]*\)', '', pkg_dep_string)
    return(x)
