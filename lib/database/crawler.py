#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def crawl_folder(dirpath):
    import time

    start = time.clock()
    dirs = []
    crawl_recursive(dirpath, dirs)

    end = time.clock()

    for f in dirs:

        if f.size() > 0:
            print(f.to_string())

    print("I found %d candidates %d dirs in %d secs" %
          (indexer.count_files(dirs), len(dirs), (end-start)))

    return dirs


# recusrive function that appends all subfolders to allfolders
def crawl_recursive(dirpath, allfolders=[]):
    from database import indexer

    # convert to our infos
    cdir = indexer.DirInfo(dirpath)
    allfolders.append(cdir)

    # recursive call
    for d in cdir.subfolders():
        crawl_recursive(d, allfolders)


if __name__ == "__main__":
    import sys
    from database import indexer

    indexer.DirInfo.ext = indexer.image_ext()
    print(' '.join(('file extension:', indexer.DirInfo.ext)))

    dirs = crawl_folder(sys.argv[1])
