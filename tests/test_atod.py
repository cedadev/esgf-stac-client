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

# def test_filter_not():
