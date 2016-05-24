#!/usr/local/bin/python


def generate_list(filelist, outputfile=""):
    import os
    import writer
    import parsemets


    errors = ""
    logmsg = ""

    writerlist = writer.WriterList()
    for f in filelist:
        print(f)
        logmsg += f
        cur_writer = parsemets.parsemets(f)
        if cur_writer != 0 and len(cur_writer.pages) > 0:
            new_id = writerlist.add_or_update(cur_writer)

            if new_id < writerlist.get_last_id():
                logmsg += " processed:\t" + str(len(cur_writer.pages)) + \
                          " pages added to existing writer (" + str(
                    str(cur_writer.name).encode('utf-8')) + ")\n"
            elif new_id == writerlist.get_last_id():
                logmsg += " processed:\t" + str(len(cur_writer.pages)) + \
                          " new writer created(" + str(
                    str(cur_writer.name).encode('utf-8')) + ")\n"

        else:
            errors += "no author detected: " + f + "\n"
            logmsg += " processed:\t" + "no author detected\n"


    writerlist.eliminate_duplicates()

    print("\n\nprinting list")
    for w in writerlist.wlist:
        encw = str(str(w.id) + "  " + str(w.name)).encode('utf-8', errors='ignore')
        enco = str(" " + str(w.date) + " " +
                   str(len(w.pages)) + " pages").encode(
                    'utf-8', errors='ignore')
        print(encw + enco)
        # print(writerlist[w].pages)

    if outputfile != "":
        f = open(outputfile, 'wb')
        for w in writerlist.wlist:
            f.write(str(str(w.id) + ";" + w.name + ";" + str(len(w.pages)) + ";" + str(w.date) + ";").encode(
                'utf-8'))
            for p in w.pages:
                f.write(str("%s" % p + ";").encode('utf-8'))
            f.write(str("\n").encode('utf-8'))
        f.close()

        errorfile = os.path.splitext(outputfile)[0]+'-error.txt'
        f = open(errorfile, 'wb')
        f.write(errors.encode('utf-8'))
        f.close()

        logfile = os.path.splitext(outputfile)[0] + '-log.txt'
        f = open(logfile, 'wb')
        f.write(logmsg.encode('utf-8'))
        f.close()

    print("printing errors:-")
    print(errors)
    return writerlist


def load_filelist(inputfile):
    f = open(inputfile, 'r')
    lines = f.read().splitlines()
    return lines


def generate_author_database(inputfile, outputfile):
    filelist = load_filelist(inputfile)
    generate_list(filelist, outputfile)


if __name__ == "__main__":
    print("generating list")

    # filelist = []
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/'+
    #     'emanusbau/913119/913119_mets.xml)
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/' +
    #     'emanusbau/108192/108192_mets.xml')
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/' +
    #     'emanusbau/1447421/1447421_mets.xml')
    # filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/' +
    #     'emanusswa/1013350/1013350_mets.xml')

    filelist = load_filelist("c:/tmp/db.txt")
    wl = generate_list(filelist, "c:/tmp/output.csv")

    # pages = []
    # import pickle
    # f = open('c:/tmp/output.pkl', 'rb')
    # wl = pickle.load(f)
    # f.close()
    # pages = []
    # for w in wl:
    #     pages.append(len(wl[w].pages))
    # import matplotlib.pyplot as plt
    #
    # plt.bar(range(0, len(pages)), pages)
    # plt.show()



    print("done")
