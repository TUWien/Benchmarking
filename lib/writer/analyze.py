#!/usr/local/bin/python

if __name__ == "__main__":
    import author
    import argparse

    print("generating list")

    parser = argparse.ArgumentParser(
        description='analyze dataset for writer identification'
        )
    parser.add_argument('--infile', default="", metavar="text-file",
                        help="""txt files containgn the full paths to the mets
                            files of the dataset""",
                        required=True)
    parser.add_argument('--outfile', default="", metavar="text-file",
                        help="""csv file were the different writers with their
                            pages are written, -log.txt and -error.txt are
                            created automatically""",
                        required=True)
    parser.add_argument('--dumpfile', default="", metavar="pkl-file",
                        help="""dumps the writer list to this file""")

    args = parser.parse_args()

    filelist = author.load_filelist(args.infile)
    wl = author.generate_list(filelist, args.outfile)

    if args.dumpfile != "":
        import pickle
        f = open(args.dumpfile, 'wb')
        pickle.dump(wl, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    print("done")
