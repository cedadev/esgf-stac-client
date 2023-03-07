#!/usr/bin/env bash

# Install main repository
cd /workspaces/esgf-stac-client/
pip3 install --user -r requirements.txt
pip3 install --user -e . --no-deps
