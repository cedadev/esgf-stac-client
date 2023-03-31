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
    assert n_items == 91

# fails on localhost
def test_2_asset_search_returns_correct_count():
    a_search = client.asset_search()
    n_assets = a_search.matched()
    assert n_assets == 199

@pytest.mark.xfail(reason='Item.assets is no longer used')
def test_3_asset_search_within_one_item(load_test_data):
    item = TEST_ITEM['data']

    get_assets_len = len([a for a in item.get_assets()])
    assets_len = len([a for a in item.assets])

    assert get_assets_len > 0
    assert assets_len > 0

    assert get_assets_len == assets_len

# id is used instead of instance ID
def test_4_search_for_instance_id_returns_correct_item():
    instance_id = "c339d061a18b9cb60924448b07a3e2b0"
    res = client.search(ids=[instance_id])
    assert res.matched() == 1

    item = next(res.items())

    assert item.id == instance_id

@pytest.mark.xfail(reason='Asset count is wrong on server-side (not our problem, in the client)')
def test_5_that_there_are_no_duplicates_in_item():
    item = TEST_ITEM['data']
    assets_generator = item.get_assets()
    file_ids_list = [asset.properties['file_id'] for asset in assets_generator]
    file_ids_set = set(file_ids_list)

    assert len(file_ids_list) > 0
    assert len(file_ids_list) == len(file_ids_set)


def test_6_1_item_search_on_facet_single():
    res = client.search(general_data_type='aircraft')
    for item in res.items():
        assert item.properties['general_data_type'] == ['aircraft']


def test_6_2_item_search_on_facet_multi():
    res = client.search(
        general_data_type=['satellites'], inspire_theme=['orthoimagery'])
    for item in res.items():
        assert item.properties['general_data_type'] == ['satellites']
        assert item.properties['inspire_theme'] == ['orthoimagery']




 