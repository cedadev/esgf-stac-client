import os
import pytest

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)


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

    items_from_coll = [i for i in my_collection.get_items()]
    items_from_coll = sorted(items_from_coll, key=lambda x: x.properties['file_id'])

    items_from_search = [i for i in res.items()]
    items_from_search = sorted(items_from_search, key=lambda x: x.properties['file_id'])

    for i, j in zip(items_from_coll, items_from_search):
        assert i.__dict__ == j.__dict__ 


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

def test_max_item_argument():
    MAX_ITEMS = 10

    res = client.search(max_items=MAX_ITEMS)

    items = [i for i in res.items()]
    assert len(items) == MAX_ITEMS
