import os
import pytest
from datetime import datetime
from dateutil import parser

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)

def test_1_1_without_datetime_argument():
    result = client.search()
    assert result.matched() > 1

def test_1_2_single_datetime():
    result = client.search(datetime='3580-12-01')
    my_datetime = parser.isoparse('3580-12-01T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_start_datetime = parser.isoparse(item.properties['start_datetime'])
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert item_start_datetime == my_datetime or item_end_datetime == my_datetime

def test_1_3_lower_bounded_datetime():
    result = client.search(datetime='3180-01-01/..')
    my_datetime = parser.isoparse('3180-01-01T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert my_datetime <= item_end_datetime


def test_1_4_upper_bounded_datetime():
    result = client.search(datetime='../3180-01-01')
    my_datetime = parser.isoparse('3180-01-01T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_start_datetime = parser.isoparse(item.properties['start_datetime'])
        assert item_start_datetime <= my_datetime

def test_1_5_full_time_datetime():
    result = client.search(datetime='3180-01-01/3580-12-01')
    my_start_datetime = parser.isoparse('3180-01-01T00:00:00.000Z')
    my_end_datetime = parser.isoparse('3580-12-01T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_start_datetime = parser.isoparse(item.properties['start_datetime'])
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert (my_start_datetime <= item_end_datetime) or (item_start_datetime <= my_end_datetime)

def test_1_6_single_datetime():
    result = client.search(instance_id="CMIP6.CMIP.NASA-GISS.GISS-E2-1-H.piControl.r1i1p1f1.Omon.zostoga.gn.v20190410", datetime='3581-01-01')
    assert result.matched() == 0

def test_1_7_lower_bounded_datetime():
    result = client.search(instance_id="CMIP6.CMIP.NASA-GISS.GISS-E2-1-H.piControl.r1i1p1f1.Omon.zostoga.gn.v20190410", datetime='3581-01-01/..')
    assert result.matched() == 0

def test_1_8_upper_bounded_datetime():
    result = client.search(instance_id="CMIP6.CMIP.NASA-GISS.GISS-E2-1-H.piControl.r1i1p1f1.Omon.zostoga.gn.v20190410", datetime='../3170-01-01')
    assert result.matched() == 0

def test_1_9_full_time_datetime():
    result = client.search(instance_id="CMIP6.CMIP.NASA-GISS.GISS-E2-1-H.piControl.r1i1p1f1.Omon.zostoga.gn.v20190410", datetime='3150-01-01/3170-01-01')
    assert result.matched() == 0


def test_2_1_without_datetime_argument(load_test_data):
    item = TEST_ITEM['data']
    assets = item.get_assets()
    assets = [a for a in assets]
    assert assets
     
def test_2_2_single_datetime(load_test_data):
    item = TEST_ITEM['data']
    assets = item.get_assets(datetime='2019-01-01')
    my_datetime = parser.isoparse('2019-01-01')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        asset_end_datetime = parser.isoparse(asset.properties['end_datetime'])
        assert asset_start_datetime == my_datetime  or asset_end_datetime == my_datetime

def test_2_3_lower_bounded_datetime(load_test_data):
    item = TEST_ITEM['data']
    assets = item.get_assets(datetime='2019-01-01/..')
    my_datetime = parser.isoparse('2019-01-01')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        assert asset_start_datetime >= my_datetime

def test_2_4_upper_bounded_datetime(load_test_data):
    item = TEST_ITEM['data']
    assets = item.get_assets(datetime='../2020-01-01')
    my_datetime = parser.isoparse('2020-01-01')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        assert asset_start_datetime <= my_datetime

def test_2_5_full_time_datetime(load_test_data):
    item = TEST_ITEM['data']
    assets = item.get_assets(datetime='2019-01-01/2020-01-01')
    my_start_datetime = parser.isoparse('2019-01-01')
    my_end_datetime = parser.isoparse('2020-01-01')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        asset_end_datetime = parser.isoparse(asset.properties['end_datetime'])
        assert (my_start_datetime <= asset_start_datetime <= my_end_datetime) or (my_start_datetime <= asset_end_datetime <= my_end_datetime)

    