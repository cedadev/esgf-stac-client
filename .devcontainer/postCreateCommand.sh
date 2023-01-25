#!/usr/bin/env bash

# Install main repository
perl -p -i -w -e 's/^git\+https:\/\/github.com\/cedadev\/pystac.git\@asset-search/#git\+https:\/\/github.com\/cedadev\/pystac.git\@asset-search/g' esgf-stac-client/requirements.txt
perl -p -i -w -e 's/^git\+https:\/\/github.com\/cedadev\/pystac-client.git\@asset-search/#git\+https:\/\/github.com\/cedadev\/pystac-client.git\@asset-search/g' esgf-stac-client/requirements.txt
pip3 install --user -e /workspaces/esgf-stac-client/. --no-deps

cd /workspaces/stac-fastapi-elasticsearch
export STAC_ELASTICSEARCH_SETTINGS=stac_fastapi.elasticsearch.settings
uvicorn stac_fastapi.elasticsearch.app:app --reload