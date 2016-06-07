#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def crawl_folder(dirpath, ext):
    import time
    from database import indexer

    start = time.clock()
    dirInfos = crawl_recursive_threaded(dirpath, ext)
    end = time.clock()

    print("I found %d candidates in %d dirs in %d secs" %
          (indexer.count_files(dirInfos), len(dirInfos), (end-start)))

    return dirInfos


# recusrive function that appends all subfolders to allfolders
def crawl_recursive_threaded(dirpath, ext):
    from database import indexer
    from database import utils
    from multiprocessing import Pool

    # convert to our infos
    cdir = indexer.DirInfo(dirpath, ext)
    cInfos = indexer.dirs_to_info(cdir.subfolders(), ext)

    # comment if you want a silent indexing
    print(cdir.to_string())

    # recursive pooled call
    # NOTE: child calls must not be pooled
    p = Pool(utils.Settings.config['processes'])
    infos = p.map(crawl_recursive, cInfos)
    p.close()
    
    # remove hierarchy
    dirInfos = [d for sublist in infos for d in sublist]
    dirInfos.append(cdir)

    print('IN was crawling with %d processes' %
          utils.Settings.config['processes'])

    return dirInfos


# recusrive function that returns all subfolders of a given path
def crawl_recursive(cdir):
    from database import indexer

    dirInfos = []

    try:

        # comment if you want a silent indexing
        if cdir.size() > 0:
            print(cdir.to_string())

        # recursive call
        for d in cdir.subfolders():
            dirInfos += crawl_recursive(indexer.DirInfo(d, cdir.ext))

        dirInfos.append(cdir)

    except Exception as e:
        print("Sorry, I cannot index: %s" % cdir.name)
        print(e)

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

    dirs = crawl_folder(sys.argv[1], indexer.image_ext())
