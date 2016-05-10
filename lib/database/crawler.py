#!/usr/local/bin/python


def crawl_folder(dirpath):
    import time

    start = time.clock()
    af = []
    crawl_recursive(dirpath, af)

    end = time.clock()
    print("I found %d folders in %d secs" % (len(af), (end-start)))

    # print("I found %d files, and you asked for %d files" %
    #   (len(files), numfiles))


def crawl_recursive(dirpath, allfolders=[]):
    from database import indexer

    cdirs = indexer.index_dirs(dirpath)

    # recursive call
    for d in cdirs:
        crawl_recursive(d, allfolders)

    # convert to our infos
    allfolders.append(indexer.dirs_to_info(cdirs))

    # files = indexfiles(dirpath)

if __name__ == "__main__":
    import sys
    crawl_folder(sys.argv[1])
