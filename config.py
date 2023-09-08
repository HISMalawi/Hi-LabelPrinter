import configparser

class PrinterConfiguration:
    def __init__(self, filename='config.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def read(self):
        self.config.read(self.filename)
        return self.config

    def create(self):
        self.config['DEFAULT'] = {'delete_files': True}
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def update(self, section, key, value):
        self.config.read(self.filename)
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
