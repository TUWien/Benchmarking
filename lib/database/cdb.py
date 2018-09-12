#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def create_database_batch(args):
    import os.path
    from database import utils
    from database import indexer

    cRoot = utils.clean_path(args['root'])
    rootDir = indexer.DirInfo(cRoot)

    if not rootDir.subfolders():
        print(cRoot + " has no subfolders...")
        print("""Please choose a different directory or \
remove --batch""")

    for cdir in rootDir.subfolders():
        print("\n")
        print("creating new database: %s --------------" % cdir)
        cargs = args.copy()
        folder = os.path.basename(cdir)

        dstname = "-".join((folder, str(cargs['nsamples'])))
        logname = ".".join((dstname, "log"))

        # customize args
        cargs['root'] = cdir
        cargs['copyto'] = os.path.join(args['copyto'], dstname)
        cargs['outfile'] = os.path.join(args['outfile'], logname)

        # now create the db
        create_database(cargs)


# returns a DirInfo list with all subfolders of dirpath
def create_database(args):
    from database import utils
    from database import cloner

    # init settings - I personally do not like this design...
    utils.Settings(args['settings'])

    # index harddisk and reduce fileset
    set = index_and_reduce_database(
            args['root'], args['nsamples'], args['ext'], args['ignoresmall'])

    if args['outfile'] != "":
        utils.write(args['outfile'], set)
    if args['copyto'] != "":
        print("")   # empty line
        cloner.clone(set, args['root'], args['copyto'],
                     args['flatcopy'], args['deletesource'])


# returns a DirInfo list with all subfolders of dirpath
def index_and_reduce_database(dirpath, numFilesDesired, ext='',
                              ignoresmall=False):
    from database import crawler
    from database import indexer
    from database import utils

    # init settings - I personally do not like this design...
    utils.Settings()

    # first choose which extensions to search for
    if ext == '':
        ext = indexer.image_ext()

    dirs = crawler.crawl_folder(dirpath, ext)
    fileset = reduce_set(dirs, numFilesDesired, ignoresmall)

    return fileset


# picks numFilesDesired samples from the database (equidistantly)
def reduce_set(dirInfos, numFilesDesired, ignoresmall):
    from database import indexer
    import math

    nf = indexer.count_files(dirInfos)

    files = indexer.file_list(dirInfos)

    if nf < numFilesDesired:
        print('WARNING: you asked for %d but I only found %d relevant files' %
              (numFilesDesired, nf))
        if ignoresmall:
            return []
        else:
            return files

    # compute step for reduced set
    step = math.floor(nf/numFilesDesired)

    # first step through equidistantly
    rf = files[0:len(files):step]

    # now crop - to remove the error from floor (step)
    rf = rf[0:numFilesDesired]

    return rf


if __name__ == "__main__":
    import argparse
    import sys
    from datetime import datetime

    # argument parser
    parser = argparse.ArgumentParser(description='Reduce a database')

    parser.add_argument('root', metavar='root-dir', type=str,
                        help='root directory of the database')
    parser.add_argument('nsamples', metavar='set-size', type=int,
                        help="""the size of the resulting set""")

    parser.add_argument('--outfile', default="", metavar="text-file",
                        help="""if set, the file paths of the reduced set
                        are written to text-file""")
    parser.add_argument('--copyto', default="", metavar="result-dir",
                        help="""if set, the reduced set will be copied
                        to result-dir""")
    parser.add_argument('--ext', default="", metavar="file-extension",
                        help="""if set, only files with the given extension
                        will be used (common image extensions are matched by
                        default)""")
    parser.add_argument('--settings', default="", metavar="path-to-settings",
                        help="""loads settings from the file""")

    # options:
    parser.add_argument('--flatcopy', action="store_true", help="""if set,
                        a flat copy is created (no folder tree)""")
    parser.add_argument('--batch', action="store_true", help="""if set,
                        each folder of root-dir is
                        treated as individual database""")
    parser.add_argument('--ignoresmall', action="store_true", help="""if set,
        folders with less files than specified are skipped""")
    parser.add_argument('--log', action="store_true", help="""save
                        outputs to a logfile in this folder
                        rather than printing them to the cmd""")
    parser.add_argument('--deletesource', action="store_true",
                        help="""deletes the original files - hence files are
                        moved than copying""")

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    # write print to log file
    # NOTE: the crawling is still reported to the cmd since these are processes
    # this is (at least for now) ok
    oldSysOut = sys.stdout
    if args['log']:
        dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        logName = "".join(("create-database-", dstr, ".log"))
        logFile = open(logName, "w")
        sys.stdout = logFile

    if args['batch']:
        print("mode: batch")
        create_database_batch(args)
    else:
        create_database(args)

    if args['log']:
        sys.stdout = oldSysOut
        logFile.close()
        print("log file written to: %s" % logName)
