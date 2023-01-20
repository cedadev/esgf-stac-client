#!/usr/bin/env bash

# Install main repository
perl -p -i -w -e 's/^git\+https:\/\/github.com\/cedadev\/pystac.git\@asset-search/#git\+https:\/\/github.com\/cedadev\/pystac.git\@asset-search/g' esgf-stac-client/requirements.txt
perl -p -i -w -e 's/^git\+https:\/\/github.com\/cedadev\/pystac-client.git\@asset-search/#git\+https:\/\/github.com\/cedadev\/pystac-client.git\@asset-search/g' esgf-stac-client/requirements.txt
pip install --user -e /workspaces/esgf-stac-client/. --no-deps
pip install --user pip --upgrade
pip install --user pyopenssl --upgrade
