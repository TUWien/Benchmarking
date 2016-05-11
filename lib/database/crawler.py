#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def crawl_folder(dirpath):
    import time
    from database import indexer

    start = time.clock()
    dirInfos = crawl_recursive_threaded(dirpath)
    end = time.clock()

    print("I found %d candidates in %d dirs in %d secs" %
          (indexer.count_files(dirInfos), len(dirInfos), (end-start)))

    return dirInfos


# recusrive function that appends all subfolders to allfolders
def crawl_recursive_threaded(dirpath):
    from database import indexer
    from database import utils
    from multiprocessing import Pool

    # convert to our infos
    cdir = indexer.DirInfo(dirpath)

    # comment if you want a silent indexing
    print(cdir.to_string())

    # recursive pooled call
    # NOTE: child calls must not be pooled
    p = Pool(utils.Settings.config['processes'])
    infos = p.map(crawl_recursive, cdir.subfolders())

    # remove hierarchy
    dirInfos = [d for sublist in infos for d in sublist]
    dirInfos.append(cdir)

    print('I was crawling with %d processes' %
          utils.Settings.config['processes'])

    return dirInfos


# recusrive function that appends all subfolders to allfolders
def crawl_recursive(dirpath):
    from database import indexer

    # convert to our info
    cdir = indexer.DirInfo(dirpath)

    # comment if you want a silent indexing
    if cdir.size() > 0:
        print(cdir.to_string())

    # recursive call
    dirInfos = []
    for d in cdir.subfolders():
        dirInfos += crawl_recursive(d)
    dirInfos.append(cdir)

    return dirInfos


# recusrive function that appends all subfolders to allfolders
def crawl_recursive_paths(dirpath, allfolders=[]):
    from database import indexer

    # convert to our infos
    cdir = dirpath
    allfolders.append(cdir)

    dirs = indexer.index_dirs(cdir)

    # recursive call
    for d in dirs:
        crawl_recursive_paths(d, allfolders)


if __name__ == "__main__":
    import sys
    from database import indexer

    indexer.DirInfo.ext = indexer.image_ext()
    print(' '.join(('file extension:', indexer.DirInfo.ext)))

    dirs = crawl_folder(sys.argv[1])
