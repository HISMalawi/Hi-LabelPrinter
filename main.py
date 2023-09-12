import re
import os
import time
from config import PrinterConfiguration
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LABEL_PRINTER_FILE_EXTENSION_PATTERN = r"\.(zpl|lbl)$"

class LabelPrinterHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.config = PrinterConfiguration().read()

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            except Exception as e:
                print(f"An error occurred while deleting {file_path}: {str(e)}")
        else:
            print(f"{file_path} does not exist.")

    def on_modified(self, event):
        if re.search(LABEL_PRINTER_FILE_EXTENSION_PATTERN, event.src_path):
            command = 'lpr -o raw "' + event.src_path + '"'
            print("✨️ Printing Label Printer File: " + command)
            os.system(command)
            if self.config.getboolean('DEFAULT', 'delete_files', fallback=False):
                self.delete_file(event.src_path)

if __name__ == '__main__':
    print("✨️ Starting Label Printer Tracker Service")
    printhandler = LabelPrinterHandler()
    folder_config_path = printhandler.config.get('DEFAULT', 'file_directory', fallback='Downloads')
    target_directory = os.path.join(os.path.expanduser("~"), folder_config_path)
    if not os.path.exists(target_directory):
        raise NameError(f"Target directory {target_directory} does not exist!")
    obs = Observer()
    obs.schedule(printhandler, path=target_directory)
    obs.start()
    print(f"👀️ Monitoring directory: {target_directory}")
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("✅️ Exiting Label Printer Tracker")
    finally:
        obs.stop()
        obs.join()
