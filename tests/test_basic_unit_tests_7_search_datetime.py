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

# fails on localhost
def test_1_2_single_datetime():
    result = client.search(datetime='2007-01-25')
    my_datetime = parser.isoparse('2007-01-25T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_start_datetime = parser.isoparse(item.properties['start_datetime'])
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert item_start_datetime <= my_datetime or item_end_datetime >= my_datetime

def test_1_3_lower_bounded_datetime():
    result = client.search(datetime='2007-01-24/..')
    my_datetime = parser.isoparse('2007-01-24T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert my_datetime <= item_end_datetime


def test_1_4_upper_bounded_datetime():
    result = client.search(datetime='../2007-01-24')
    assert result.matched() == 0
   

def test_1_5_full_time_datetime():
    result = client.search(datetime='2007-01-24/3580-12-01')
    my_start_datetime = parser.isoparse('2007-01-24T00:00:00.000Z')
    my_end_datetime = parser.isoparse('3580-12-01T00:00:00.000Z')
    assert result.matched() > 0
    for item in result.items():
        item_start_datetime = parser.isoparse(item.properties['start_datetime'])
        item_end_datetime = parser.isoparse(item.properties['end_datetime'])
        assert (my_start_datetime <= item_end_datetime) or (item_start_datetime <= my_end_datetime)

def test_1_6_single_datetime():
    result = client.search(ids="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-24')
    assert result.matched() == 0

def test_1_7_lower_bounded_datetime():
    result = client.search(ids="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-24/..')
    assert result.matched() == 1

def test_1_8_upper_bounded_datetime():
    result = client.search(ids="c339d061a18b9cb60924448b07a3e2b0", datetime='../2007-01-24')
    assert result.matched() == 0

def test_1_9_full_time_datetime():
    result = client.search(ids="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-24/2007-01-24')
    assert result.matched() == 0


def test_2_1_without_datetime_argument(load_test_data):
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    assets = item.get_assets()
    assets = [a for a in assets] 
    assert assets
     
def test_2_2_single_datetime(load_test_data):
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    assets = item.get_assets(datetime='2007-01-25')
    my_datetime = parser.isoparse('2007-01-25')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        asset_end_datetime = parser.isoparse(asset.properties['end_datetime'])
        assert asset_start_datetime == my_datetime  or asset_end_datetime == my_datetime

def test_2_3_lower_bounded_datetime(load_test_data):
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    assets = item.get_assets(datetime='2007-01-25/..')
    my_datetime = parser.isoparse('2007-01-25')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        assert asset_start_datetime >= my_datetime

def test_2_4_upper_bounded_datetime(load_test_data):
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    assets = item.get_assets(datetime='../2007-01-25')
    my_datetime = parser.isoparse('2007-01-25')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        assert asset_start_datetime <= my_datetime

def test_2_5_full_time_datetime(load_test_data):
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    assets = item.get_assets(datetime='2007-01-25/2007-01-25')
    my_start_datetime = parser.isoparse('2007-01-25')
    my_end_datetime = parser.isoparse('2007-01-25')

    for asset in assets:
        asset_start_datetime = parser.isoparse(asset.properties['start_datetime'])
        asset_end_datetime = parser.isoparse(asset.properties['end_datetime'])
        assert (my_start_datetime <= asset_start_datetime) or (asset_end_datetime <= my_end_datetime)


def test_2_6_1_single_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(items=item, datetime='2007-01-25')
    assert result.matched() == 0

def test_2_6_2_single_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(items=[item], datetime='2007-01-25')
    assert result.matched() == 0

def test_2_6_3_single_datetime():
    result = client.asset_search(items="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-25')
    assert result.matched() == 0

def test_2_6_4_single_datetime():
    result = client.asset_search(item=["c339d061a18b9cb60924448b07a3e2b0"], datetime='2007-01-25')
    assert result.matched() == 0

def test_2_7_1_lower_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=item, datetime='2007-01-25/..')
    assert result.matched() == 0

def test_2_7_2_lower_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=[item], datetime='2007-01-25/..')
    assert result.matched() == 0

def test_2_7_3_lower_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-25/..')
    assert result.matched() == 0

def test_2_7_4_lower_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=["c339d061a18b9cb60924448b07a3e2b0"], datetime='2007-01-25/..')
    assert result.matched() == 0

def test_2_8_1_upper_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=item, datetime='../2007-01-25')
    assert result.matched() == 0

def test_2_8_2_upper_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=[item], datetime='../2007-01-25')
    assert result.matched() == 0

def test_2_8_3_upper_bounded_datetime():
    result = client.asset_search(item="c339d061a18b9cb60924448b07a3e2b0", datetime='../2007-01-25')
    assert result.matched() == 0

def test_2_8_4_upper_bounded_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=["CMIP6.CMIP.NASA-GISS.GISS-E2-1-H.piControl.r1i1p1f1.Omon.zostoga.gn.v20190410"], datetime='../3170-01-01')
    assert result.matched() == 0

def test_2_9_1_full_time_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=item, datetime='2007-01-25/2007-01-25')
    assert result.matched() == 0

def test_2_9_2_full_time_datetime():
    res = client.search(ids="c339d061a18b9cb60924448b07a3e2b0")
    item = next(res.items())
    result = client.asset_search(item=[item], datetime='2007-01-25/2007-01-25')
    assert result.matched() == 0

def test_2_9_3_full_time_datetime():
    result = client.asset_search(item="c339d061a18b9cb60924448b07a3e2b0", datetime='2007-01-25/2007-01-25')
    assert result.matched() == 0

def test_2_9_4_full_time_datetime():
    result = client.asset_search(item=["c339d061a18b9cb60924448b07a3e2b0"], datetime='2007-01-25/2007-01-25')
    assert result.matched() == 0

