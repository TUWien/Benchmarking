#!/usr/local/bin/python

if __name__ == "__main__":
    import argparse
    import pickle
    import os
    import math
    import random

    from shutil import copy

    parser = argparse.ArgumentParser(
        description='creates dataset for writer identification'
    )
    parser.add_argument('--infile', default="", metavar="pkl-file",
                        help="""dump files created with analyze.py""",
                        required=True)
    parser.add_argument('--outdir', default="", metavar="outputdir",
                        help="""directory where the files should be written""",
                        required=True)
    parser.add_argument('--minnum', default="", metavar="int", type=int,
                        help="""minimal number of pages""",
                        required=True)
    parser.add_argument('--mapfile', default="", metavar="file",
                        help="""txt file where the mapping should be written"""
                        )
    parser.add_argument('--maxnum', default=0, metavar="int", type=int,
                        help="""maximal number of pages (if 0 or not set minimal number
                        of pages are used, -1 for all pages)""")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        print("output directory does not exist ... exiting")
        exit()
    if os.listdir(args.outdir) != []:
        print("output directory is not empty ... exiting")
        exit()

    if args.minnum < 0:
        print("minimal number of documents is smaller than 0 ... exiting")
        exit()

    if args.maxnum == 0 or args.maxnum == []:
        maxnum = args.minnum
    else:
        maxnum = args.maxnum

    f = open(args.infile, 'rb')
    writerlist = pickle.load(f)
    f.close()

    print("filtering writers: current number:" + str(len(writerlist.wlist)))
    del_items = []
    for w in writerlist.wlist:
        if len(w.pages) < args.minnum:
            del_items.append(w)

    for i in del_items:
        writerlist.wlist.pop(i)

    print("remaining writers after filter:" + str(len(writerlist.wlist)))

    mapping = {}
    for w in writerlist.wlist:
        print("processing id " + str(w.id) + " with " + str(len(w.pages)) + " pages")

        writer_dir = args.outdir + "/" + str(w.id) + "/"
        os.mkdir(writer_dir)

        pages = []
        if args.maxnum == -1:
            pages = w.pages
        else:
            # take random pages
            items = list(range(0, len(w.pages)))
            random.shuffle(items)
            items = items[0:maxnum]
            for i in items:
                pages.append(w.pages[i])

        for p in pages:
            copy(p, writer_dir)

        mapping[w.id] = w

    if args.mapfile != "":
        f = open(args.mapfile, 'wb')
        for m in mapping:
            o = str(str(m) + "\t" + str(mapping[m] + "\n")).encode('utf-8')
            f.write(o)
        f.close()
