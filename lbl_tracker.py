import re
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LBL_EXTENSION_PATTERN = r"\.lbl$"
TARGET_DIRECTORY = os.path.join(os.path.expanduser("~"), "Downloads")

class LblHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if re.search(LBL_EXTENSION_PATTERN, event.src_path):
            command = 'lpr -o raw "' + event.src_path + '"'
            print("Printing lbl: " + command)
            os.system(command)

if __name__ == '__main__':
    print("Starting Lbl tracker service")
    obs = Observer()
    obs.schedule(LblHandler(), path=TARGET_DIRECTORY)
    obs.start()
    print("Lbl tracker started")
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting Lbl tracker")
    finally:
        obs.stop()
        obs.join()
