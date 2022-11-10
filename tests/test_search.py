import os
import pytest

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient



def test_example_no_fixture():
    assert THING["data"] == None


def test_example_fixture(load_test_data):
    # Value of global THING variable has changed due to fixture being run
    assert THING["data"] == "hi"


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_something_depends_on_slash_badc():
    assert "data" in os.listdir("/badc/cmip5")


def test_search_for_instance_id_returns_correct_item():
    client = ESGFStacClient.open(API_URL)
    instance_id = "CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HH.highres-future.r1i1p1f1.day.tas.gn.v20191105"
    res = client.search(instance_id=instance_id)
    assert res.matched() == 1

    item = next(res.items())
    assert item.properties["instance_id"][0] == instance_id

def test_item_search_returns_correct_count():
    client = ESGFStacClient.open(API_URL)
    search = client.search()
    n_items = search.matched()
    assert n_items == 677813


def test_asset_search_returns_correct_count():
    client = ESGFStacClient.open(API_URL)
    a_search = client.asset_search()
    n_assets = a_search.matched()
    assert n_assets == 6137991

def test_item_search_on_facet_single():
    client = ESGFStacClient.open(API_URL)
    res = client.search(activity_id='HighResMIP')
    for item in res.items():
        assert item.properties['activity_id'] == ['HighResMIP']

def test_item_search_on_facet_multi():
    client = ESGFStacClient.open(API_URL)
    res = client.search(pid='hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae', data_node='esgf-data3.ceda.ac.uk')
    for item in res.items():
        assert item.properties['pid'] == ['hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae']
        assert item.properties['data_node'] == ['esgf-data3.ceda.ac.uk']

def test_asset_search_within_one_item(load_test_data):
    item = TEST_ITEM['data']

    assert len(item.get_assets()) > 0
    assert len(item.assets) > 0

    assert item.get_assets() == item.assets


def test_that_there_are_no_duplicates_in_item():
    item = TEST_ITEM['data']
    assets_generator = item.get_assets()
    file_ids_list =  [asset.properties['file_id'] for asset in assets_generator]
    file_ids_set = set(file_ids_list)
    
    assert len(file_ids_list) > 0
    assert len(file_ids_list) == len(file_ids_set)
