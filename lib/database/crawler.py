#!/usr/local/bin/python


def crawlfolder(dirpath, numfiles):
    from database.indexer import indexfiles

    files = indexfiles(dirpath)

    print("I found %d files, and you asked for %d files" %
          (len(files), numfiles))

if __name__ == "__main__":
    import sys
    crawlfolder(sys.argv[1], int(sys.argv[2]))
