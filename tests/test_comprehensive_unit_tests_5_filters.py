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
    my_filter = "general_data_type<>'AerChemMIP' AND flight_number='b262'"
    result = client.search(filter=my_filter)
    
    for item in result.items():
        assert item.properties['general_data_type'][0] != 'AerChemMIP'
        assert item.properties['flight_number'][0] == 'b262'


def test_2():
    my_filter = "inspire_theme='Meteorological geographical features'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['inspire_theme'][0] == 'Meteorological geographical features'


def test_3():
    my_filter = "platform='faam'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['platform'][0] == 'faam'


def test_4():
    my_filter = "extension='.nc' or magic_number='Pa'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert item.properties['extension'][0] == '.nc' or item.properties['magic_number'][0] == 'application/octet-stream'


def test_5():
    my_filter = "gemet_topic<>'Climatology'"
    result = client.search(filter=my_filter)

    for item in result.items():
        assert 'Climatology' not in item.properties['gemet_topic']


