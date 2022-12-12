import os
import pytest
import re

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)

def test_1():
    result = client.search(q='*rain*')

    for item in result.items():
        rain = False
        for attribute in item.properties.values():
            if 'rain' in str(attribute):
                rain = True
        assert rain