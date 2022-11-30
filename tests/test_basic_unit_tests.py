import os
import pytest

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)

def test_1_item_search_returns_correct_count():
    search = client.search()
    n_items = search.matched()
    assert n_items == 677813
    
def test_2_asset_search_returns_correct_count():
    a_search = client.asset_search()
    n_assets = a_search.matched()
    assert n_assets == 6137991

@pytest.mark.xfail(reason='Item.assets is no longer used')
def test_3_asset_search_within_one_item(load_test_data):
    item = TEST_ITEM['data']

    get_assets_len = len([a for a in item.get_assets()])
    assets_len = len([a for a in item.assets])

    assert get_assets_len > 0
    assert assets_len > 0

    assert get_assets_len == assets_len


def test_4_search_for_instance_id_returns_correct_item():
    instance_id = "CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HH.highres-future.r1i1p1f1.day.tas.gn.v20191105"
    res = client.search(instance_id=instance_id)
    assert res.matched() == 1

    item = next(res.items())
    assert item.properties["instance_id"][0] == instance_id

@pytest.mark.xfail(reason='Asset count is wrong on server-side (not our problem, in the client)')
def test_5_that_there_are_no_duplicates_in_item():
    item = TEST_ITEM['data']
    assets_generator = item.get_assets()
    file_ids_list = [asset.properties['file_id'] for asset in assets_generator]
    file_ids_set = set(file_ids_list)

    assert len(file_ids_list) > 0
    assert len(file_ids_list) == len(file_ids_set)


def test_6_1_item_search_on_facet_single():
    res = client.search(activity_id='HighResMIP')
    for item in res.items():
        assert item.properties['activity_id'] == ['HighResMIP']


def test_6_2_item_search_on_facet_multi():
    res = client.search(
        pid='hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae', data_node='esgf-data3.ceda.ac.uk')
    for item in res.items():
        assert item.properties['pid'] == [
            'hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae']
        assert item.properties['data_node'] == ['esgf-data3.ceda.ac.uk']




 