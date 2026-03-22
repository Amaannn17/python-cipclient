import time
import threading
import queue


class MockSocket:
    def recv(self, bufsize):
        raise socket.timeout("timed out")


class MockCIP:
    def __init__(self, restart=False):
        self.restart_connection = restart
        self.restart_lock = threading.Lock()
        self.socket = MockSocket()


import socket
from cipclient import ReceiveThread


def measure(restart=False):
    cip = MockCIP(restart)
    recv_thread = ReceiveThread(cip)

    start_cpu = time.process_time()
    recv_thread.start()
    time.sleep(5.0)
    recv_thread._stop_event.set()
    recv_thread.join(timeout=1.0)
    end_cpu = time.process_time()

    return end_cpu - start_cpu


if __name__ == "__main__":
    t2 = measure(True)
    print(f"CPU Time used by ReceiveThread (disconnected) for 5s: {t2:.6f} seconds")
