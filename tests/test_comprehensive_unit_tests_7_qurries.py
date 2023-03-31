import os
import pytest
import re

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)

def test_1_whole_word():
    word = 'atmosphere'

    result = client.search(q=word)

    for item in result.items():
        found = False
        for attribute in item.properties.values():
            if isinstance(attribute, list):
                for i in attribute:
                    if word == i:
                        found = True
            else:
                if word == str(attribute):
                    found = True
                    
        assert found