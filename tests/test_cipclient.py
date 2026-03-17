import pytest
from cipclient import CIPSocketClient

def test_subscribe_invalid_direction():
    client = CIPSocketClient("localhost", 0x03)
    def callback(sigtype, join, value):
        pass

    with pytest.raises(ValueError) as excinfo:
        client.subscribe("d", 1, callback, direction="invalid")
    assert "is not a valid signal direction" in str(excinfo.value)

def test_subscribe_invalid_sigtype():
    client = CIPSocketClient("localhost", 0x03)
    def callback(sigtype, join, value):
        pass

    with pytest.raises(ValueError) as excinfo:
        client.subscribe("invalid", 1, callback, direction="in")
    assert "is not a valid signal type" in str(excinfo.value)

def test_subscribe_valid():
    client = CIPSocketClient("localhost", 0x03)
    def callback(sigtype, join, value):
        pass

    # These should not raise ValueError
    client.subscribe("d", 1, callback, direction="in")
    client.subscribe("a", 2, callback, direction="out")
    client.subscribe("s", 3, callback, direction="in")

    assert 1 in client.join["in"]["d"]
    assert 2 in client.join["out"]["a"]
    assert 3 in client.join["in"]["s"]
