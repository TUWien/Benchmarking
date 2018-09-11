#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def split_database(args):
    from database import utils
    from database import indexer
    from database import cloner
    import math

    # init settings - I personally do not like this design...
    utils.Settings(args['settings'])

    srcpath = args['srcpath']
    dstpath = args['dstpath']
    ext = args['ext']

    tn = args['trainset']
    en = args['evalset']

    dirInfos = index_database(srcpath, ext)

    # compute # of files per set
    nf = indexer.count_files(dirInfos)
    files = indexer.file_list(dirInfos)

    if tn+en == 0:
        print('WARNING: trainset and evalset are set to zero - nothing to do here...')
        return []
    elif tn+en > 1:
        print('WARNING: trainset size (tn) + evalset size (en) are > 1: %d + %d = %d' % (tn, en, tn+en))
        return []

    numTrain = math.floor(nf*tn)
    numEval = math.floor(nf*en)
    numTest = nf-numTrain-numEval

    print("train size: %d" % numTrain)
    print("eval size: %d" % numEval)
    print("test size: %d" % numTest)

    trs = reduce_set(files, numTrain)
    files = list(filter(lambda f: f not in trs, files))
    
    evs = reduce_set(files, numEval)
    files = list(filter(lambda f: f not in evs, files))

    tes = files

    if (args["dryrun"]):
        if trs:
            print("Train Set (%d):" % numTrain)
            print("\n".join(trs))
        if evs:
            print("Evaluation Set (%d):" % numEval)
            print("\n".join(evs))
        if tes:
            print("Test Set (%d):" % numTest)
            print("\n".join(tes))
    else:
        print("")   # empty line
        if trs:
            print("Train Set (%d):" % numTrain)
            cloner.clone(trs, srcpath, dstpath + "/train")
        if evs:
            print("Evaluation Set (%d):" % numEval)
            cloner.clone(evs, srcpath, dstpath + "/eval")
        if tes:
            print("Test Set (%d):" % numTest)
            cloner.clone(tes, srcpath, dstpath + "/test")

    return []

# returns a DirInfo list with all subfolders of dirpath
def index_database(dirpath, ext=''):
    from database import crawler
    from database import indexer
    from database import utils

    # init settings - I personally do not like this design...
    utils.Settings()

    # first choose which extensions to search for
    if ext == '':
        ext = indexer.image_ext()

    dirs = crawler.crawl_folder(dirpath, ext)

    return dirs


# picks numFilesDesired samples from the database (equidistantly)
def reduce_set(filelist, numFilesDesired):
    import math

    # nothing to do here...
    if numFilesDesired == 0:
        return []

    # compute step for reduced set
    step = math.floor(len(filelist)/numFilesDesired)

    # first step through equidistantly
    rf = filelist[0:len(filelist):step]

    # now crop - to remove the error from floor (step)
    rf = rf[0:numFilesDesired]

    return rf


if __name__ == "__main__":
    import argparse
    import sys
    from datetime import datetime

    # argument parser
    parser = argparse.ArgumentParser(description='Split a database')

    parser.add_argument('srcpath', metavar='source-dir', type=str,
                        help='root directory of the database')
    parser.add_argument('dstpath', metavar='dest-dir', type=str,
                        help='destination of the database with splits')

    parser.add_argument('--trainset', default=0.3, type=float, metavar="trainset-size",
                        help="""size of the training set (value must be within [0 1])""")
    parser.add_argument('--evalset', default=0, type=float, metavar="evalset-size",
                        help="""size of the evaluation set (value must be within [0 1]""")
    
    parser.add_argument('--ext', default="", metavar="file-extension",
                        help="""if set, only files with the given extension
                    will be used (common image extensions are matched by
                    default)""")

    parser.add_argument('--settings', default="", metavar="path-to-settings",
                        help="""loads settings from the file""")

    # options:
    parser.add_argument('--dryrun', action="store_true", help="""if set,
                        a dry run is performed""")

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    split_database(args)

    # # write print to log file
    # # NOTE: the crawling is still reported to the cmd since these are processes
    # # this is (at least for now) ok
    # oldSysOut = sys.stdout
    # if args['log']:
    #     dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    #     logName = "".join(("create-database-", dstr, ".log"))
    #     logFile = open(logName, "w")
    #     sys.stdout = logFile

    # if args['batch']:
    #     print("mode: batch")
    #     create_database_batch(args)
    # else:
    #     create_database(args)

    # if args['log']:
    #     sys.stdout = oldSysOut
    #     logFile.close()
    #     print("log file written to: %s" % logName)
