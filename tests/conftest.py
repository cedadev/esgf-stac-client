import os
from pathlib import Path
import pytest


THING = {"data": None}
API_URL = "https://api.stac.ceda.ac.uk"


@pytest.fixture
def load_test_data():
    """
    Can be used as an argument to a unit test.
    """
    THING["data"] = "hi"
