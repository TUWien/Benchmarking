#!/usr/local/bin/python

if __name__ == "__main__":
    import argparse
    import pickle
    import os
    import math

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
                        of pages are used)""")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        print("output directory does not exist ... exiting")
        exit()
    if os.listdir(args.outdir) != []:
        print("output directory is not empty ... exiting")
        exit()

    if args.maxnum == 0 or args.maxnum == []:
        maxnum = args.minnum
    else:
        maxnum = args.maxnum

    f = open(args.infile, 'rb')
    writerlist = pickle.load(f)
    f.close()

    print("filtering writers: current number:" + str(len(writerlist)))
    del_items = []
    for n, w in writerlist.items():
        if len(w.pages) < args.minnum:
            del_items.append(n)

    for i in del_items:
        writerlist.pop(i)

    print("remaining writers after filter:" + str(len(writerlist)))

    id = 0
    mapping = {}
    for w in writerlist:
        writer_dir = args.outdir + "/" + str(id) + "/"
        os.mkdir(writer_dir)

        # compute step for reduced set
        step = math.ceil(len(writerlist[w].pages) / maxnum)

        print('step size: %d' % step)

        # first step through equidistantly
        newpages = writerlist[w].pages[0:len(writerlist[w].pages):step]

        writerlist[w].pages = newpages[0:maxnum]

        for p in writerlist[w].pages:
            copy(p, writer_dir)

        mapping[id] = w
        id += 1

    if args.mapfile != "":
        f = open(args.mapfile, 'wb')
        for m in mapping:
            o = str(str(m) + "\t" + str(mapping[m] + "\n")).encode('utf-8')
            f.write(o)
        f.close()
