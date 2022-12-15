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
    my_filter = "activity_id<>'AerChemMIP' AND (variable='hus' or variable='ta')"
    result = client.search(filter=my_filter)
    
    for item in result.items():
        assert item.properties['activity_id'][0] != 'AerChemMIP'
        assert item.properties['variable'][0] in ['hus', 'ta']


def test_2():
    my_filter = "insitution_id='CMCC'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['insitution_id'][0] == 'CMCC'


def test_3():
    my_filter = "realm='aerosol'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['realm'][0] == 'aerosol'


def test_4():
    my_filter = "variable_units='K' or variable_units='Pa'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['variable_units'][0] in ['K', 'Pa']


def test_5():
    my_filter = "cf_standard_name<>'air_temperature' AND variable_units='m'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['cf_standard_name'][0] != 'air_temperature'
        assert item.properties['variable_units'][0] == 'm'


