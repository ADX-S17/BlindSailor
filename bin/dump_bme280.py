import time
import BlindSailor

import sihd
from sihd.srcs.Handlers.IHandler import IHandler

class Handler(IHandler):

    def handle(self, service, data):
        print(data)

def start_dump():
    service = BlindSailor.Readers.Bme280Reader()
    handler = Handler()
    service.add_observer(handler)
    service.set_conf({
        "port": "/dev/i2c-1",
        "addr": 0x76,
        "thread_frequency": 10,
    })
    service.setup()
    handler.start()
    service.save_data(True)
    service.start()
    time.sleep(10)
    service.stop()
    print(service.get_data_saved())

if __name__ == "__main__":
    start_dump()
