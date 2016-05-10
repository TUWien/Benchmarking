#!/usr/local/bin/python


# index a single folder and returns all files
def index_files(dirpath):
    from os import listdir
    from os.path import isfile, join

    filelist = []

    try:
        filelist = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)
    except PermissionError:
        print('%s permission denied' % dirpath)

    return filelist


# index a single folder and returns all directories
def index_dirs(dirpath):
    from os import listdir
    from os.path import isdir, join

    dirlist = []

    try:

        # find all directories and append them to dirlist
        for d in listdir(dirpath):
            fp = join(dirpath, d)
            if isdir(fp):
                dirlist.append(fp)

    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)
        dirlist = []
    except PermissionError:
        print('%s permission denied' % dirpath)

    return dirlist


def dirs_to_info(dirlist):

    dirInfoList = []
    for d in dirlist:
        dirInfoList.append(DirInfo(d))

    return dirInfoList


class DirInfo:
    """Saves all info needed for each directory"""

    def __init__(self, name):
        self.name = name
        self.cnt = 0

    def index(self):
        self.cnt = len(index_files(self.name))

    # yes the to string works
    def to_string(self):
        s = " ".join((self.name, 'has', str(self.cnt), 'files'))
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
