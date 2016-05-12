#!/usr/local/bin/python


# splits string list with linebreaks and writes it to filename
def write(filename, strList):

    try:
        data = "\n".join(strList)

        file = open(filename, 'w')
        file.write(data)
        file.close()
        print("%s lines written to %s" % (str(len(strList)), filename))
    except Exception as e:
        print("WARNING: I cannot save to %s" % filename)
        print(e)


# read file's content in a string list
def read(filename):

    with open(filename, 'r') as file:
        data = [s.replace('\n', '') for s in file.readlines()]

    return data


# cleans (replaces) windows like file separators
def clean_path(p):
    return p.replace("\\", "/")


def make_path_unique(filepath):
    import os.path

    # nothing to do here if the file exists already
    if not os.path.exists(filepath):
        return filepath

    filepath, ext = os.path.splitext(filepath)

    for idx in range(1, 1000):
        newpath = "".join((filepath, "-", str(idx), ext))

        if not os.path.exists(newpath):
            return newpath
    else:
        print('WARNING: I could not find an alternative name for %s'
              % filepath)


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
        self._add_key('processes', 6)
        self._add_key('threads', 2)

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
