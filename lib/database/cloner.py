#!/usr/local/bin/python


# creates valid destination paths and clones all filepaths in srclist
# if flat is true, files are directly saved to dstpath
# if flat is false, the hierarchy is replicated relative to srcpath
def clone(srclist, srcpath, dstpath, flat=0):

    # create destination filenames
    dstlist = []
    for f in srclist:
        if not flat:
            p = replace_path(f, srcpath, dstpath)
        else:
            p = create_path(f, dstpath)

        dstlist.append(p)

    print("start cloning...")
    for i in range(0, len(srclist)):
        copy(srclist[i], dstlist[i])


# Copies the file from src to dst. If dst exists,
# an incrementer is added to the filename:
# josef.png -> josef-1.png
def copy(src, dst):
    from database import utils
    from shutil import copyfile
    import os

    try:
        dname = os.path.dirname(dst)

        if not os.path.isdir(dname):
            os.makedirs(dname)

        dst = utils.make_path_unique(dst)

        copyfile(src, dst)
        print("%s -> %s" % (src, dst))
    except Exception as e:
        print("could not copy: %s -> %s" % (src, dst))
        print(e)


# replaces the srcpath in filepath with dstpath
def replace_path(filepath, srcpath, dstpath):
    from database import utils

    srcpath = utils.clean_path(srcpath)
    dstpath = utils.clean_path(dstpath)

    dp = filepath.replace(srcpath, dstpath)

    if dp == filepath:
        print("WARNING: srcpath == dstpath: %s" % filepath)
        print("%s vs %s" % (srcpath, dstpath))
    return dp


# merges the filename in filepath with dstpath
def create_path(filepath, dstpath):
    import ntpath
    import os

    filename = ntpath.basename(filepath)
    dp = os.path.join(dstpath, filename)

    return dp
