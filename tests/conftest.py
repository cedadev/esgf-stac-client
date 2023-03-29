import os
from pathlib import Path
import pytest
from pystac.item import Item

THING = {"data": None}
<<<<<<< Updated upstream
API_URL = "https://api.stac.ceda.ac.uk"
=======
API_URL = "http://localhost:8081"
>>>>>>> Stashed changes
TEST_ITEM = {"data": None}

@pytest.fixture
def load_test_data():
    """
    Can be used as an argument to a unit test.
    """
    THING["data"] = "hi"
    TEST_ITEM['data'] = Item.from_file('test_item.json')
