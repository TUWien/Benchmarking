#!/usr/local/bin/python


class Author:
    """ Saves the author information and the list of his pages"""

    def __init__(self, name="", pages = []):
        self.name = name
        self.pages = pages

    def addPages(self,newpages):
        for n in newpages:
            self.pages.append(n)


def generateList(filelist, outputfile=""):
    from writer import parsemets

    authorlist = {}
    for f in filelist:
        print(f)
        (author, files) = parsemets.parsemets(f)
        if author != 0:
            if author in authorlist:
                authorlist[author].addPages(files)
            else:
                authorlist[author] = Author(author, files)

    print("\n\nprinting list")
    for a in authorlist:
        print(a)
        print(authorlist[a].pages)

    if outputfile != "":
        f = open(outputfile, 'w')
        for a in authorlist:
            f.write(a + ";")
            f.write(str(len(authorlist[a].pages)) + ";")
            for p in authorlist[a].pages:
                f.write("%s" % p + ";")
            f.write("\n")
        f.close()
    return authorlist


def loadfilelist(inputfile):
    f = open(inputfile, 'r')
    lines = f.read().splitlines()
    return lines


def generate_author_database(inputfile, outputfile):
    filelist = loadfilelist(inputfile)
    generateList(filelist, outputfile)


if __name__ == "__main__":
    print("generating list")

    # filelist = []
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/913119/913119_mets.xml')
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/108192/108192_mets.xml')
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/' +
    #     '1447421/1447421_mets.xml')
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusswa/' +
    #     '1013350/1013350_mets.xml')

    filelist = loadfilelist("c:/tmp/db.txt")
    generateList(filelist, "c:/tmp/output.csv")
    print("done")
