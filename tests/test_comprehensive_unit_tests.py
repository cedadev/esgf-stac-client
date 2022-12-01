import os
import pytest

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)


def test_1_get_post_number_of_items():
    res_get = client.search(data_node='esgf-data3.ceda.ac.uk', method='GET')
    res_post = client.search(data_node='esgf-data3.ceda.ac.uk', method='POST')

    l1 = sorted([a.properties['instance_id'] for a in res_get.items()])
    l2 = sorted([a.properties['instance_id'] for a in res_post.items()])

    assert len(l1) == len(l2)

    for a, b in zip(l1, l2):
        assert a == b

def test_3_passing_item_objects():
    result = client.search()
    ig = result.items()
    item1 = next(ig)
    item2 = next(ig)
    assets1 = item1.get_assets()
    assets2 = item2.get_assets()
    no_assets1 = len([a for a in assets1] + [a for a in assets2])
    
    ag = client.asset_search(items=[item1, item2])
    no_assets2 = len([a for a in ag])

    assert no_assets1 == no_assets2


def test_4_max_item_argument():
    MAX_ITEMS = 10

    res = client.search(max_items=MAX_ITEMS)

    items = [i for i in res.items()]
    assert len(items) == MAX_ITEMS

    
    

def test_getting_collection_object_and_passing_to_the_search():
    colls = client.get_collections()
    my_collection = next(colls)

    res = client.search(collections=[my_collection])

    items_from_coll = [i for i in my_collection.get_items()]
    items_from_coll = sorted(items_from_coll, key=lambda x: x.properties['file_id'])

    items_from_search = [i for i in res.items()]
    items_from_search = sorted(items_from_search, key=lambda x: x.properties['file_id'])

    for i, j in zip(items_from_coll, items_from_search):
        assert i.__dict__ == j.__dict__ 


def test_getting_item_object_and_passing_to_the_search(load_test_data):
    res = client.search(items=[TEST_ITEM['data']])

    assert TEST_ITEM['data'] == res


def test_8_1_mapping():
    res_1 = client.search(doctype='item')
    res_2 = client.search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_8_2_mapping():
    res_1 = client.search(doctype='dataset')
    res_2 = client.search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_8_3_mapping():
    res_1 = client.search(doctype='asset') 
    res_2 = client.asset_search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


def test_8_4_mapping():
    res_1 = client.search(doctype='item')
    res_2 = client.asset_search()

    assert res_1
    assert res_2
    assert res_1.__dict__ == res_2.__dict__


@pytest.mark.xfail(reason='Doctype is not know')
def test_8_5_mapping():
    assert client.search(doctype='other')


