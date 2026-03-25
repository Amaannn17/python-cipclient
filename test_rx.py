import time
import logging
import threading
from cipclient import ReceiveThread, CIPSocketClient

logging.getLogger("cipclient").setLevel(logging.INFO)


class MockSocket:
    def __init__(self, data):
        self.data = data
        self.count = 0

    def recv(self, bufsize):
        if self.count > 10000:
            time.sleep(1)
            return b""
        self.count += 1
        return self.data

    def close(self):
        pass


def run():
    # Simulate standard digital join message from Crestron (packet type 0x05)
    packet = b"\x05\x00\x06\x00\x00\x03\x00\x00\x00"

    cip = CIPSocketClient("127.0.0.1", 1)
    cip.socket = MockSocket(packet)

    rx = ReceiveThread(cip)
    start = time.process_time()
    rx.start()
    time.sleep(2)
    rx._stop_event.set()
    rx.join()
    end = time.process_time()
    print(f"Time: {end - start:.6f}s")
    print(f"Items processed: {cip.socket.count}")


run()
