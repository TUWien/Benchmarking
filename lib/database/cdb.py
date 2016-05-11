#!/usr/local/bin/python


# returns a DirInfo list with all subfolders of dirpath
def create_database(dirpath, numFilesDesired, ext=''):
    from database import crawler
    from database import indexer

    # init settings - I personally do not like this design...
    utils.Settings()

    # first choose which extensions to search for
    if ext == '':
        indexer.DirInfo.ext = indexer.image_ext()
    else:
        indexer.DirInfo.ext = ext

    print(' '.join(('file extension:', indexer.DirInfo.ext)))

    dirs = crawler.crawl_folder(dirpath)

    fileset = reduce_set(dirs, numFilesDesired)
    return fileset


def reduce_set(dirInfos, numFilesDesired):
    from database import indexer
    import math

    nf = indexer.count_files(dirInfos)

    files = indexer.file_list(dirInfos)

    if nf < numFilesDesired:
        print('WARNING: you asked for %d but I only found %d relevant files' %
              (numFilesDesired, nf))
        return files

    # compute step for reduced set
    step = math.floor(nf/numFilesDesired)

    print('step size: %d' % step)

    # first step through equidistantly
    rf = files[0:len(files):step]

    # now crop - to remove the error from floor (step)
    rf = rf[0:numFilesDesired]

    return rf


if __name__ == "__main__":
    import argparse
    from database import utils

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

    args = parser.parse_args()

    # init settings - I personally do not like this design...
    utils.Settings(args.settings)

    # index harddisk and reduce fileset
    set = create_database(args.root, args.nsamples, args.ext)

    if args.outfile != "":
        utils.write(args.outfile, set)
    if args.copyto != "":
        print("copy to is not implemented yet")
