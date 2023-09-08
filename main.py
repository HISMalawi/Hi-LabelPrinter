import re
import os
import time
from config import PrinterConfiguration
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser


LABEL_PRINTER_FILE_EXTENSION_PATTERN = r"\.(zpl|lbl)$"
TARGET_DIRECTORY = os.path.join(os.path.expanduser("~"), "Downloads")
CONFIG_FILE_PATH = 'config.ini'


class LabelPrinterHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.config = self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE_PATH):
            config.read(CONFIG_FILE_PATH)
        else:
            config['DEFAULT'] = {'delete_files': True}
            with open(CONFIG_FILE_PATH, 'w') as configfile:
                config.write(configfile)
        return config

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

    if not os.path.exists(CONFIG_FILE_PATH):
        print("✨️ Configuration file does not exist. Creating default configuration...")
        config_manager = PrinterConfiguration(CONFIG_FILE_PATH)
        config_manager.create()
        print("✅️ Default configuration created.")

    config_manager = PrinterConfiguration(CONFIG_FILE_PATH)
    config = config_manager.read()

    obs = Observer()
    obs.schedule(LabelPrinterHandler(), path=TARGET_DIRECTORY)
    obs.start()
    print("✨️ Label Printer Tracker Started")
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("✅️ Exiting Label Printer Tracker")
    finally:
        obs.stop()
        obs.join()
