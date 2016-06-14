#!/usr/local/bin/python


# computes statistics of rootdir and saves them to statlog
def stats(rootdir, statfile, ext='jpg'):
    from database import indexer
    from database import crawler

    # first choose which extensions to search for
    if ext == '':
        ext = indexer.image_ext()

    print(rootdir)
    print(ext)

    dirs = crawler.crawl_folder(rootdir, ext)
    save_to_log(statfile, dirs)


# save statistics to logpath
def save_to_log(logpath, dirs):
    from database import utils

    print("START statistics ------------------------")

    stats = []
    for d in dirs:

        stats.append(d.to_string(True))
        print(d.to_string())

    if logpath:
        utils.write(logpath, stats)
        print("stats written to " + logpath)

    print("END statistics ------------------------")


# calls stats with cmd args
def stats_with_args(args):
    from database import utils

    # init settings - I personally do not like this design...
    utils.Settings(args['settings'])

    stats(args['root'], args['statfile'], args['ext'])


if __name__ == "__main__":
    import argparse
    import sys
    from datetime import datetime

    # argument parser
    parser = argparse.ArgumentParser(description="""Compute statistics of a
                        folder tree""")

    parser.add_argument('root', metavar='root-dir', type=str,
                        help='root directory of the folder tree')
    # parser.add_argument('nsamples', metavar='set-size', type=int,
    #                     help="""the size of the resulting set""")

    parser.add_argument('--ext', default="", metavar="file-extension",
                        help="""if set, only files with the given extension
                        will be counted""")
    parser.add_argument('--settings', default="", metavar="path-to-settings",
                        help="""loads settings from the file""")

    # options:
    parser.add_argument('--log', action="store_true", help="""save
                        outputs to a logfile in this folder
                        rather than printing them to the cmd""")
    parser.add_argument('--statfile', metavar="path-to-stats",
                        help="""path to file which stores the statistics""")

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

    stats_with_args(args)

    if args['log']:
        sys.stdout = oldSysOut
        logFile.close()
        print("log file written to: %s" % logName)
