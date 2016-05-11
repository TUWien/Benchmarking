#!/usr/local/bin/python


def generateList(filelist, outputfile=""):
    import os
    # from writer import parsemets
    errors = ""
    logmsg = ""

    writerlist = {}
    for f in filelist:
        print(f)
        logmsg += f
        cur_writer = parsemets.parsemets(f)
        if cur_writer != 0:
            if cur_writer.name in writerlist:
                # check if date correct
                if cur_writer.date == writerlist[cur_writer.name].date:
                    writerlist[cur_writer.name].addPages(cur_writer.pages)
                    logmsg += " processed:\t" + str(len(cur_writer.pages)) + " pages added to existing writer\n"
                else:
                    print("skipping %s because date does not agree" % cur_writer.name)
                    errors += "date mismatch: " + f + "\n"
                    logmsg += " processed:\t" + "date mismatch\n";
            else:
                writerlist[cur_writer.name] = cur_writer
                logmsg += " processed:\t" + str(len(cur_writer.pages)) + " pages added to new writer\n"
        else:
            errors  += "no author detected: " + f + "\n"
            logmsg += " processed:\t" + "no author detected\n";


    print("\n\nprinting list")
    for w in writerlist:
        print(w + " " + str(writerlist[w].date) + " " + str(len(writerlist[w].pages)) + " pages")
        print(writerlist[w].pages)

    if outputfile != "":
        f = open(outputfile, 'w')
        for w in writerlist:
            f.write(w + ";")
            f.write(str(len(writerlist[w].pages)) + ";")
            for p in writerlist[w].pages:
                f.write("%s" % p + ";")
            f.write("\n")
        f.close()

        errorfile = os.path.splitext(outputfile)[0]+'-error.txt'
        f = open(errorfile, 'w')
        f.write(errors)
        f.close()

        logfile = os.path.splitext(outputfile)[0] + '-log.txt'
        f = open(logfile, 'w')
        f.write(logmsg)
        f.close()

    print("printing errors:-")
    print(errors)
    return writerlist


def loadfilelist(inputfile):
    f = open(inputfile, 'r')
    lines = f.read().splitlines()
    return lines


def generate_author_database(inputfile, outputfile):
    filelist = loadfilelist(inputfile)
    generateList(filelist, outputfile)


if __name__ == "__main__":
    import parsemets
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
