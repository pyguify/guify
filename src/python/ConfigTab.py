import os
from configparser import ConfigParser

CONFIG_FILE_NAME = 'config.ini'


class ConfigTab:
    verbose_name = None
    default_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

    def __init__(self) -> None:
        self.__init_config__()

    def __init_config__(self) -> None:
        cfg = ConfigParser(default_section=None)
        cfg.optionxform = str
        if not os.path.isfile(self.default_path):
            with open(self.default_path, 'w') as f:
                cfg.write(f)

        cfg.read(self.default_path)
        self._cfg = cfg

    def get(self, section, key):
        self.load()
        return self._cfg.get(section, key)

    def get_section(self, section):
        self.load()
        return self._cfg[section]

    def set(self, section, key, value):
        self.load()
        self._cfg.set(section, key, value)
        self.save()

    def save(self, cfg_dict):
        self._cfg.read_dict(cfg_dict)
        with open(self.default_path, 'w') as f:
            self._cfg.write(f)

    def load(self):
        self._cfg.clear()
        with open(self.default_path, 'r') as f:
            self._cfg.read_file(f)

        retval = {}

        for section in self._cfg.sections():
            retval[section] = dict(self._cfg.items(section))

        return retval
