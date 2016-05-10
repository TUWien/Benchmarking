#!/usr/local/bin/python


def write(filename, strList):

    data = "\n".join(strList)

    file = open(filename, 'w')
    file.write(data)
    file.close()

    print("%s lines written to %s" % (str(len(strList)), filename))
