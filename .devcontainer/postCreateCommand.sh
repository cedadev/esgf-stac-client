#!/usr/bin/env bash

# Git clone other repositories
sudo git clone -b asset-search https://github.com/cedadev/pystac /workspaces/pystac
sudo git clone -b asset-search https://github.com/cedadev/pystac-client /workspaces/pystac-client

# Install Pystac requirements
pip install -r /workspaces/pystac/requirements-dev.txt

# Install Pystac-client requirements
pip install -r  /workspaces/pystac-client/requirements-min.txt
pip install -r /workspaces/pystac-client/requirements-dev.txt

# Install Esgf-stac-client requirements
pip install -r /workspaces/esgf-stac-client/requirements_dev.txt

# Install main repositories
pip install -e /workspaces/esgf-stac-client/. --no-deps
pip install -e /workspaces/pystac-client/. --no-deps
pip install -e /workspaces/pystac/. --no-deps
