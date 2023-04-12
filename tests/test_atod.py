import pytest

from .conftest import THING, API_URL, TEST_ITEM

from esgf_stac_client.client import ESGFStacClient


client = None


def setup_module():
    global client
    client = ESGFStacClient.open(API_URL)

def test_correct_count_of_items():
    search = client.search()
    n_items = search.matched()
    assert n_items == 91

def test_number_of_items_from_property():
    with open('properties_test.csv') as f:
        for line in f:
            property, value, expected_number_of_hits = line.split(',')
            search = client.search(filter=f"{property}='{value}'")
            assert search.matched() == int(expected_number_of_hits), f'Searching for "{property}={value}" returned {search.matched()} assets while {int(expected_number_of_hits)} was expected'

def test_datetime():
    def get_matches_from_datetime(datetime_string):
        search = client.search(datetime = datetime_string)
        return search.matched()

    test_cases = {
        '2007-01-25': 1,
        '2007-01-25/..': 2,
        '../2007-01-25': 1,
        '2007-01-25/2022-03-25': 2,
        '2022-03-25': 1,
        '2022-03-25/..': 1,
        '../2022-03-25': 2,
        '2022-03-24': 0,
    }

    for k, v in test_cases.items():
        assert get_matches_from_datetime(k) == v

def test_correct_count_of_assets():
    search = client.asset_search()
    n_assets = search.matched()
    assert n_assets == 199

def test_duplicated_assets():
    res = client.search()
    for i in res.items():
        assets = list(i.get_assets())
        assets_uris = [a.extra_fields['uri'] for a in assets]
        num_of_assets = len(assets)
        num_of_uris = len(set(assets_uris))
        assert  num_of_assets == num_of_uris, f"Number of assets ({num_of_assets}) is different than number of unique URIs ({num_of_uris}) for Item {i}"


def test_collections():
    res = client.search(collections=['faam', 'cmip5'])
    assert res.matched() == 44

def test_filter_not():
     with open('properties_test.csv') as f:
        for line in f:
            property, value, expected_number_of_hits = line.split(',')
            search = client.search(filter=f"{property}<>'{value}'")
            assert search.matched() == 91 - int(expected_number_of_hits), f'Searching for "{property}={value}" returned {search.matched()} assets while {91 - int(expected_number_of_hits)} was expected'

def test_on_multiple_facets():
    res = client.search(magic_number='application/x-hdf', permitted_use='personal')
    assert res.matched() == 1

def test_get_and_post():
    res_get = client.search(method='GET')
    res_post = client.search(method='POST')

    l1 = sorted([a.id for a in res_get.items()])
    l2 = sorted([a.id for a in res_post.items()])

    assert len(l1) == len(l2)

    for a, b in zip(l1, l2):
        assert a == b

def test_collections_argument():
    res = client.search(collections=['faam'])
    assert res.matched() == 2

    colls = client.get_collections()
    colls = [i for i in colls if i.id == 'faam']
    coll = colls[0]
    res = client.search(collections=coll)
    assert res.matched() == 2

def test_items_argument():
    res = client.search()
    item = next(res.items())
    
    res = client.search(items=[item])
    assert res.matched() == 1

def test_doc_types():
    res = client.search()
    res_mapp = client.search(doctype='item')
    assert res.matched() == res_mapp.matched()

    res_mapp = client.search(doctype='dataset')
    assert res.matched() == res_mapp.matched()

    res = client.asset_search()
    res_mapp = client.search(doctype='asset')
    assert res.matched() == res_mapp.matched()