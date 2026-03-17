import time
import threading
import queue


class MockSocket:
    def sendall(self, data):
        pass


class MockCIP:
    def __init__(self, connected=True):
        self.tx_queue = queue.Queue()
        self.restart_connection = False
        self.restart_lock = threading.Lock()
        self.socket = MockSocket()
        self.connected = connected
        self.buttons_pressed = {}
        self.buttons_lock = threading.Lock()
        self.join = {"out": {"d": {}}}


from cipclient import SendThread


def measure(connected=True):
    cip = MockCIP(connected)
    send_thread = SendThread(cip)

    start_cpu = time.process_time()
    send_thread.start()
    time.sleep(10.0)
    send_thread._stop_event.set()
    send_thread.join(timeout=1.0)
    end_cpu = time.process_time()

    return end_cpu - start_cpu


if __name__ == "__main__":
    t = measure(True)
    print(f"CPU Time used by SendThread (connected) for 10s: {t:.6f} seconds")
    t2 = measure(False)
    print(f"CPU Time used by SendThread (disconnected) for 10s: {t2:.6f} seconds")
