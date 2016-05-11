#!/usr/local/bin/python


def write(filename, strList):

    data = "\n".join(strList)

    file = open(filename, 'w')
    file.write(data)
    file.close()

    print("%s lines written to %s" % (str(len(strList)), filename))


class Settings:
    """Reads settings from a yaml and provides them to all functions"""

    config = 0
    fpath = ""

    def __init__(self, fpath=""):
        Settings.fpath = fpath

        if (fpath != ""):
            self._load_settings(fpath)
        self._load_default()

    def _load_settings(self, fpath):
        import yaml

        try:
            sf = open(fpath)
            Settings.config = yaml.load(sf)

        except Exception as e:
            print("Sorry, I could not read settings from: %s" % fpath)
            fpath = ""
            print(e)

    # loads default keys
    def _load_default(self):
        self._add_key('debug_level', 0)
        self._add_key('threads', -1)

    def _add_key(self, key, val):

        if Settings.config == 0:
            Settings.config = dict()
        if key not in Settings.config:
            Settings.config[key] = val

    def print():

        print("Settings loaded from %s" % Settings.fpath)

        for k in Settings.config:
            s = "".join((k, ": ", str(Settings.config[k])))
            print(s)

        print()
