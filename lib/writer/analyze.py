#!/usr/local/bin/python

if __name__ == "__main__":
    import author
    import argparse

    print("generating list")

    parser = argparse.ArgumentParser(description='analyze dataset for writer identification')
    parser.add_argument('--infile', default="", metavar="text-file",
                        help="""txt files containgn the full paths to the mets files of the dataset""",
                        required = True)
    parser.add_argument('--outfile', default="", metavar="text-file",
                        help="""csv file were the different writers with their pages are written""",
                        required = True)

    args = parser.parse_args()

    filelist = author.loadfilelist(args.infile)
    author.generateList(filelist, args.outfile)
    print("done")
