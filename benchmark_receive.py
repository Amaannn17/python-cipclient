import time
import threading
import queue
from cipclient import ReceiveThread


class MockSocket:
    def recv(self, size):
        time.sleep(1)  # simulate waiting for packet
        raise TimeoutError("timeout")


class MockCIP:
    def __init__(self, connected=True):
        self.restart_connection = False
        self.restart_lock = threading.Lock()
        self.socket = MockSocket()


def measure():
    cip = MockCIP()
    receive_thread = ReceiveThread(cip)

    start_cpu = time.process_time()
    receive_thread.start()
    time.sleep(10.0)
    receive_thread._stop_event.set()
    receive_thread.join(timeout=1.0)
    end_cpu = time.process_time()

    return end_cpu - start_cpu


if __name__ == "__main__":
    t = measure()
    print(f"CPU Time used by ReceiveThread for 10s: {t:.6f} seconds")
