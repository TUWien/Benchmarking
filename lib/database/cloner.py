#!/usr/local/bin/python


def clone(srclist, srcpath, dstpath, flat=0):

    print(srcpath, dstpath)

    # create destination filenames
    dstlist = []
    for f in srclist:
        if not flat:
            p = replace_path(f, srcpath, dstpath)
        else:
            p = create_path(f, dstpath)

        dstlist.append(p)

    clone_threaded(srclist, dstlist)


# clones files NOTE: it is not threaded yet
def clone_threaded(srclist, dstlist):

    print("src size: %d dst size: %d" % (len(srclist), len(dstlist)))

    # p = Pool(utils.Settings.config['processes'])
    # p.map(copy, srclist, dstlist)

    for i in range(0, len(srclist)):
        copy(srclist[i], dstlist[i])


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


def create_path(filepath, dstpath):
    import ntpath
    import os

    filename = ntpath.basename(filepath)
    dp = os.path.join(dstpath, filename)

    return dp
