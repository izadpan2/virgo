import pytest
from server import APIHandler

@pytest.mark.parametrize("test_input, expected", [
    ("virgosvs.com", True),
    ("8.8.8.8", False),
    ("microsoft.com", True),
    ("172.217.6.46", False),
    ("www.amazon.com", True)
])
def test_is_hostname(test_input, expected):
    assert APIHandler.is_hostname(test_input) == expected