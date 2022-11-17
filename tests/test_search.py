import os
import pytest
from datetime import datetime
from dateutil import parser
from pytz import utc

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)


def test_example_no_fixture():
    assert THING["data"] == None


def test_example_fixture(load_test_data):
    # Value of global THING variable has changed due to fixture being run
    assert THING["data"] == "hi"


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_something_depends_on_slash_badc():
    assert "data" in os.listdir("/badc/cmip5")


def test_search_for_instance_id_returns_correct_item():
    instance_id = "CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HH.highres-future.r1i1p1f1.day.tas.gn.v20191105"
    res = client.search(instance_id=instance_id)
    assert res.matched() == 1

    item = next(res.items())
    assert item.properties["instance_id"][0] == instance_id


def test_item_search_returns_correct_count():
    search = client.search()
    n_items = search.matched()
    assert n_items == 677813


def test_asset_search_returns_correct_count():
    a_search = client.asset_search()
    n_assets = a_search.matched()
    assert n_assets == 6137991


def test_item_search_on_facet_single():
    res = client.search(activity_id='HighResMIP')
    for item in res.items():
        assert item.properties['activity_id'] == ['HighResMIP']


def test_item_search_on_facet_multi():
    res = client.search(
        pid='hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae', data_node='esgf-data3.ceda.ac.uk')
    for item in res.items():
        assert item.properties['pid'] == [
            'hdl:21.14100/cbc76f50-84a1-30ed-8c06-4a60868161ae']
        assert item.properties['data_node'] == ['esgf-data3.ceda.ac.uk']


@pytest.mark.xfail(reason='Item.assets is no longer used')
def test_asset_search_within_one_item(load_test_data):
    item = TEST_ITEM['data']

    get_assets_len = len([a for a in item.get_assets()])
    assets_len = len([a for a in item.assets])

    assert get_assets_len > 0
    assert assets_len > 0

    assert get_assets_len == assets_len


@pytest.mark.xfail(reason='Asset count is wrong on server-side (not our problem in the client)')
def test_that_there_are_no_duplicates_in_item():
    item = TEST_ITEM['data']
    assets_generator = item.get_assets()
    file_ids_list = [asset.properties['file_id'] for asset in assets_generator]
    file_ids_set = set(file_ids_list)

    assert len(file_ids_list) > 0
    assert len(file_ids_list) == len(file_ids_set)


def test_item_search_on_datetime():
    time_range = ['2001-02-24:00:00:00Z', None]
    start_datetime = datetime.strptime('24/02/2001', '%d/%m/%Y')
    res = client.search(datetime=time_range)
    for item in res.items():
        item_start_datetime = item.properties['start_datetime']
        item_start_datetime = parser.isoparse(item_start_datetime)
        assert item_start_datetime >= start_datetime


def test_get_post_number_of_items():
    res_get = client.search(data_node='esgf-data3.ceda.ac.uk', method='GET')
    res_post = client.search(data_node='esgf-data3.ceda.ac.uk', method='POST')

    l1 = sorted([a.properties['instance_id'] for a in res_get.items()])
    l2 = sorted([a.properties['instance_id'] for a in res_post.items()])

    assert len(l1) == len(l2)

    for a, b in zip(l1, l2):
        assert a == b


def test_getting_collection_object_and_passing_to_the_search():
    colls = client.get_collections()
    my_collection = next(colls)

    res = client.search(collections=[my_collection])

    assert res


def test_getting_item_object_and_passing_to_the_search(load_test_data):
    res = client.search(items=[TEST_ITEM['data']])

    assert TEST_ITEM['data'] == res


def test_mapping_1():
    res_1 = client.search(doctype='item')
    res_2 = client.search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_mapping_2():
    res_1 = client.search(doctype='dataset')
    res_2 = client.search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_mapping_3():
    res_1 = client.search(doctype='asset')
    res_2 = client.asset_search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_mapping_4():
    res_1 = client.search(doctype='item')
    res_2 = client.asset_search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


@pytest.mark.xfail(reason='Doctype is not know')
def test_mapping_5():
    assert client.search(doctype='other')
