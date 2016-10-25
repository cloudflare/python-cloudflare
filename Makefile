
PYTHON = python
PANDOC = pandoc
PYLINT = pylint

EMAIL = "mahtin@mahtin.com"
NAME = "cloudflare"

all: README.rst build

README.rst: README.md
    $(PANDOC) --from=markdown --to=rst < README.md > README.rst

build: setup.py
    $(PYTHON) setup.py build

install: build
    sudo $(PYTHON) setup.py install
    sudo rm -rf ${NAME}.egg-info

test: all
    # to be done

sdist: all
    make clean
    make test
    $(PYTHON) setup.py sdist
    rm -rf ${NAME}.egg-info

bdist: all
    make clean
    make test
    $(PYTHON) setup.py bdist
    rm -rf ${NAME}.egg-info

upload: clean all
    $(PYTHON) setup.py sdist upload --sign --identity="$(EMAIL)"

lint:
    $(PYLINT) CloudFlare cli4

clean:
    rm -rf build
    rm -rf dist
    mkdir build dist
    $(PYTHON) setup.py clean
    rm -rf ${NAME}.egg-info

