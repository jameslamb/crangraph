conda-env:
	# Create conda environment or update existing
	if ! (conda env list | grep -q "crangraph"); then \
		echo "crangraph conda environment doesn't exist. Creating..." && \
		conda env create -f python/crangraph.yml; \
	else \
	    conda env update -q -n crangraph -f python/crangraph.yml; \
	fi
	
install_python:
	# Creat or update conda env
	# Install crangraph Python package into crangraph env
	make conda-env && \
	source activate crangraph && \
	echo "Installing crangraph package..." && \
	python python/setup.py install && \
	echo "Installed crangraph."
	
make docs_python:
	# Create sphinx rst files for every package and subpackage
	cd python && \
	sphinx-apidoc -f -e -o docs crangraph && \
	cd docs && \
	make html && \
	cp -R _build/html/* ../../docs/