import requests
from crangraph_utils import *

#packages = get_package_list()
#print packages
#
#my_package = 'ggplot2'
#releases = get_old_releases(my_package)

#print releases

desc_text = requests.get('https://raw.githubusercontent.com/cran/data.table/master/DESCRIPTION')
deps_set = scrape_deps_from_description(desc_text.content)
print deps_set
