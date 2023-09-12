import os
import configparser

DEFAULT_CONFIG = {
    'delete_file': True,
    'file_directory': "Downloads"
}

class PrinterConfiguration:
    def __init__(self, filename='config.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def read(self):
        if not os.path.exists(self.filename):
            self.create_default_config()
        self.config.read(self.filename)
        return self.config

    def create_default_config(self):
        self.config['DEFAULT'] = DEFAULT_CONFIG
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def update(self, section, key, value):
        self.config.read(self.filename)
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
