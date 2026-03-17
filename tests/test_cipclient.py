
import pytest
from cipclient import CIPSocketClient

@pytest.fixture
def client():
    return CIPSocketClient("localhost", 0x03)

@pytest.mark.parametrize("ciptype, payload", [
    (0x05, b"\x00\x00\x00"),             # ciptype 0x05, payload too short for datatype access
    (0x05, b"\x00\x00\x00\x00\x00"),     # ciptype 0x05, datatype 0x00, payload too short for digital join
    (0x05, b"\x00\x00\x00\x14\x00\x00\x00"), # ciptype 0x05, datatype 0x14, payload too short for analog join
    (0x05, b"\x00\x00\x00\x03"),         # ciptype 0x05, datatype 0x03, payload too short for update request type
    (0x05, b"\x00\x00\x00\x08\x00\x00\x00\x00\x00"), # ciptype 0x05, datatype 0x08, payload too short for date/time
    (0x12, b"\x00\x00\x00\x00\x00\x00"), # ciptype 0x12, payload too short for serial join
])
def test_short_payloads_no_crash(client, ciptype, payload):
    """Verify that short payloads do not cause IndexErrors."""
    try:
        client._processPayload(ciptype, payload)
    except IndexError:
        pytest.fail(f"IndexError raised for ciptype 0x{ciptype:02x} and payload len {len(payload)}")

def test_valid_digital_join(client):
    """Verify that a valid digital join is processed correctly (no crash, item in queue)."""
    # ciptype 0x05, payload: [0, 0, 0, datatype=0x00, join_low=0x00, join_high=0x00]
    # join = (0 << 8 | 0) + 1 = 1, state = (0 >> 7) ^ 1 = 1
    client._processPayload(0x05, b"\x00\x00\x00\x00\x00\x00")
    assert not client.event_queue.empty()
    item = client.event_queue.get()
    assert item == ("in", "d", 1, 1)

def test_valid_analog_join(client):
    """Verify that a valid analog join is processed correctly."""
    # ciptype 0x05, payload: [0, 0, 0, datatype=0x14, join_high=0x00, join_low=0x01, val_high=0x04, val_low=0xd2]
    # join = (0 << 8 | 1) + 1 = 2, value = (4 << 8 | 210) = 1234
    client._processPayload(0x05, b"\x00\x00\x00\x14\x00\x01\x04\xd2")
    assert not client.event_queue.empty()
    item = client.event_queue.get()
    assert item == ("in", "a", 2, 1234)

def test_valid_serial_join(client):
    """Verify that a valid serial join is processed correctly."""
    # ciptype 0x12, payload: [0, 0, 0, 0, 0, join_high=0x00, join_low=0x02, 0, 'H', 'e', 'l', 'l', 'o']
    # join = (0 << 8 | 2) + 1 = 3, value = "Hello"
    client._processPayload(0x12, b"\x00\x00\x00\x00\x00\x00\x02\x00Hello")
    assert not client.event_queue.empty()
    item = client.event_queue.get()
    assert item == ("in", "s", 3, "Hello")
