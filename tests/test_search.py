import os
import pytest

from .conftest import THING, API_URL

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
