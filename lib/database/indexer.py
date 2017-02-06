#!/usr/local/bin/python


# returns a RegExp string with common image extensions
def image_ext():
    return ".jp(e)?g$|.tif(f)?$|.png$|.bmp$"


def is_valid(filename, ext=""):
    import re

    if ext == "":
        return True

    p = re.compile(ext, re.IGNORECASE)
    m = p.search(filename)

    if m:
        return True
    else:
        return False


# index a single folder and returns all files
def index_files(dirpath, ext=""):
    from os import listdir
    from os.path import isfile, join

    filelist = []

    try:

        for f in listdir(dirpath):
            fpath = join(dirpath, f)
            if isfile(fpath) and is_valid(fpath, ext):
                filelist.append(fpath)

    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)
    except PermissionError:
        print('%s permission denied' % dirpath)

    return filelist


# index a single folder and returns all directories
def index_dirs(dirpath):
    from os import listdir
    from os.path import isdir, join
    from database import utils

    dirlist = []

    try:

        # find all directories and append them to dirlist
        for d in listdir(dirpath):
            fp = join(dirpath, d)
            if isdir(fp):
                cfp = utils.clean_path(fp)
                dirlist.append(cfp)

    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)
    except PermissionError:
        print('%s permission denied' % dirpath)

    return dirlist


def dirs_to_info(dirlist, ext):

    dirInfoList = []
    for d in dirlist:
        dirInfoList.append(DirInfo(d, ext))

    return dirInfoList


# returns the total number of matched files in dirInfoList
def count_files(dirInfoList):

    cnt = 0

    for d in dirInfoList:
        cnt += d.size()

    return cnt


# returns a list with all filepaths
def file_list(dirInfoList):
    from database import utils

    fpaths = []

    for info in dirInfoList:
        fpaths += [utils.clean_path(f) for f in info.filepaths]

    return fpaths


class DirInfo:
    """Saves all info needed for each directory"""

    def __init__(self, name="", ext=""):
        self.name = name
        self.ext = ext
        self.filepaths = self._index()

    def _index(self):
        return index_files(self.name, self.ext)

    def subfolders(self):
        return index_dirs(self.name)

    def size(self):
        return len(self.filepaths)

    def size_recursive(self):

        total = len(self.filepaths)

        for d in dirs_to_info(self.subfolders(), self.ext):
            total += d.size_recursive()

        return total

    # lists the folder name and the number of files contained
    def to_string(self, all_count=False):

        if all_count:
            s = "[%s|%s] \t %s" % (str(self.size_recursive()),
                                   str(self.size()), self.name)
        else:
            s = "[%s] \t %s" % (str(self.size()), self.name)

        return s


if __name__ == "__main__":
    import sys

    dirpath = sys.argv[1]
    files = index_files(dirpath)

    info = DirInfo(dirpath)
    info.index()
    print(info.to_string())

    # print("\n".join(files))
    print(dirpath, "contains %d files" % len(files))
