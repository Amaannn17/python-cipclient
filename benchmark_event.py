import time
import threading
import queue
from cipclient import EventThread


class MockCIP:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.join_lock = threading.Lock()
        self.join = {
            "in": {"d": {}, "a": {}, "s": {}},
            "out": {"d": {}, "a": {}, "s": {}},
        }
        self._cip_packet = {
            "d": b"\x05\x00\x06\x00\x00\x03\x00",
            "db": b"\x05\x00\x06\x00\x00\x03\x27",
        }
        self.buttons_lock = threading.Lock()
        self.buttons_pressed = {}
        self.connected = True
        self.restart_connection = False
        self.tx_queue = queue.Queue()


def measure():
    cip = MockCIP()
    event_thread = EventThread(cip)
    start_cpu = time.process_time()
    event_thread.start()
    time.sleep(10.0)
    event_thread._stop_event.set()
    event_thread.join(timeout=1.0)
    end_cpu = time.process_time()
    return end_cpu - start_cpu


if __name__ == "__main__":
    t = measure()
    print(f"CPU Time used by EventThread for 10s: {t:.6f} seconds")
