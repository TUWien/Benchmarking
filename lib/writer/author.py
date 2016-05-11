#!/usr/local/bin/python


class Author:
    """ Saves the author information and the list of his pages"""

    def __init__(self, name="", pages = []):
        self.name = name
        self.pages = pages

    def addPages(self,newpages):
        self.pages.append(newpages)


def generateList(filelist):
    from writer import parsemets

    list = {}
    for f in filelist:
        print(f)
        (author, files) = parsemets.parsemets(filelist)

        list['author'] = Author(author, files)

    for a in list.items():
        print(a)



if __name__ == "__main__":
    print("generating list")

    filelist = []
    filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/913119/913119_mets.xml')
    filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/108192/108192_mets.xml')
    filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/' +
        '1447421/1447421_mets.xml')
    filelist.append('E:/Databases/unibas_eManuscripta_firstExamples/emanusswa/' +
        '1013350/1013350_mets.xml')

    generateList(filelist)
    print("done")
