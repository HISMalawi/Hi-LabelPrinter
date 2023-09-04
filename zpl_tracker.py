import re
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ZPL_EXTENSION_PATTERN = r"\.raw\.z64(?: \(\d+\))?\.zpl$"
TARGET_DIRECTORY = os.path.join(os.path.expanduser("~"), "Downloads")

class ZplHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if re.search(ZPL_EXTENSION_PATTERN, event.src_path):
            command = 'lpr -o raw "' + event.src_path + '"'
            print("Printing zpl: " + command)
            os.system(command)

if __name__ == '__main__':
    print("Starting Zpl tracker service")
    obs = Observer()
    obs.schedule(ZplHandler(), path=TARGET_DIRECTORY)
    obs.start()
    print("ZPL tracker started")
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting Zpl tracker")
    finally:
        obs.stop()
        obs.join()
