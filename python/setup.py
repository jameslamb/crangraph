import setuptools

# Required packages
normal_packages = [
    'bs4',
    'kafka',
    'networkx',
    'requests',
    'streamparse'
]
documentation_packages = [
    "sphinx",
    "sphinxcontrib-napoleon",
    "sphinxcontrib-programoutput"
]

setuptools.setup(name='crangraph',
                 version='0.1',
                 description='Python functions used in orchestrating a dependency graph of the R language',
                 url='https://github.com/jameslamb/repos/crangraph',
                 packages=setuptools.find_packages(),
                 install_requires= normal_packages,
                 extras_requires= {
                    'all': normal_packages + documentation_packages,
                    'docs': documentation_packages
                 }
)