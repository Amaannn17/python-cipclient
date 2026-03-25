import time
import logging
from cipclient import CIPSocketClient

logging.getLogger("cipclient").setLevel(logging.INFO)

cip = CIPSocketClient("127.0.0.1", 1)


def run():
    for _ in range(100000):
        cip.event_queue.put(("out", "s", 1, "test_string_123"))

    from cipclient import EventThread

    thread = EventThread(cip)
    start = time.process_time()
    thread.start()
    while not cip.event_queue.empty():
        pass
    thread._stop_event.set()
    thread.join()
    end = time.process_time()
    print(f"Time: {end - start:.6f}s")


run()
