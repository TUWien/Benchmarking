#!/usr/local/bin/python


# index a single folder and returns all files
def indexfiles(dirpath):
    from os import listdir
    from os.path import isfile, join

    try:
        filelist = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)

    return filelist


# index a single folder and returns all directories
def indexdirs(dirpath):
    from os import listdir
    from os.path import isdir, join

    try:
        dirlist = [f for f in listdir(dirpath) if isdir(join(dirpath, f))]
    except FileNotFoundError:
        print('%s does not exist - please specify a valid folder' % dirpath)

    return dirlist


if __name__ == "__main__":
    import sys

    dirpath = sys.argv[1]
    files = indexfiles(dirpath)

    print("\n".join(files))
    print(dirpath, "contains %d files" % len(files))
