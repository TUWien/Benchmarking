#!/usr/local/bin/python

""" module for parsing the mets file. use parsemets to get author and filelist"""

STRUCT_MAP = 'mets:structMap'
DIV_ELEMENT = 'mets:div'
DMD_SECTION = 'mets:dmdSec'
NAME_ELEMENT = 'mods:name'
ROLE_ELEMENT = 'mods:roleTerm'


def getLogicalStructure(xmldoc):
    from xml.dom import minidom

    print("getting logical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "LOGICAL":
            return i


def getPhysicalStructure(xmldoc):

    print("getting physical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "PHYSICAL":
            return i


def getIds(logStruct):

    print("getting Ids")
    itemlist = logStruct.getElementsByTagName(DIV_ELEMENT)
    dmdId = -1
    id = -1
    for i in itemlist:
        if i.attributes['TYPE'].value == "document":
            dmdId = i.attributes['DMDID'].value
            id = i.attributes['ID'].value
            print("dmdid:" + dmdId)
            print("id:" + id)
    return(dmdId, id)


def getPersonList(dmdId, xmldoc):
    print("searching for dmdSec")

    itemlist = xmldoc.getElementsByTagName(DMD_SECTION)

    for i in itemlist:
        if i.attributes['ID'].value == dmdId:
            return i.getElementsByTagName(NAME_ELEMENT)


def getAuthor(personList):

    name = 0
    for p in personList:
        role = p.getElementsByTagName(ROLE_ELEMENT)
        for r in role:
            if len(r.childNodes) > 0:
                code = r.firstChild.nodeValue
                if code == "aut":
                    name = p.getElementsByTagName('mods:namePart')
                    for n in name:
                        if n.hasAttribute("type"):
                            if n.attributes['type'].value == "date":
                                print("date:" + n.firstChild.nodeValue)
                        else:
                            name = n.firstChild.nodeValue

    return name


def getFileLinks(id, xmldoc):

    print("searching for files")
    itemlist = xmldoc.getElementsByTagName('mets:structLink')

    fileLinks = []
    for i in itemlist:
        for child in i.childNodes:
            if (
                child.hasAttribute("xlink:from") and
                child.attributes['xlink:from'].value == id
            ):
                    fileLinks.append(child.attributes['xlink:to'].value)

    return fileLinks


def getFiles(link, physStruct):

    print("getting files for fileLink:" + link)
    itemlist = physStruct.getElementsByTagName(DIV_ELEMENT)
    fileList = []
    for item in itemlist:
        if item.hasAttribute("ID") and item.attributes['ID'].value == link:
            print("id:" + item.attributes['ID'].value)
            for child in item.childNodes:
                if (
                    child.hasAttribute("FILEID") and
                    str(child.attributes['FILEID'].value).find("MAX", 0) > 0
                ):
                        file = child.attributes['FILEID'].value
                        fileList.append(file)
    return fileList


def parsemets(filepath):
    from xml.dom import minidom
    import os

    author = []
    files = []
    cur_dir = os.path.dirname(filepath)
    xmldoc = minidom.parse(filepath)
    logStruct = getLogicalStructure(xmldoc)
    (dmdId, id) = getIds(logStruct)
    if dmdId != -1 and id != -1:
        personList = getPersonList(dmdId, xmldoc)
        author = getAuthor(personList)
        if author == 0:
            print("no author found")
        else:
            fileLinks = getFileLinks(id, xmldoc)
            physStruct = getPhysicalStructure(xmldoc)
            files = []
            for f in fileLinks:
                file = getFiles(f, physStruct)
                for f in file:
                    # TODO : CHANGE ME!!!!
                    fullPath = cur_dir + "\\img\\" + f + ".jpg"
                    files.append(fullPath)

            print("\n\n\nauthor:" + author)
            print("files:" + str(files))

    return (author, files)


if __name__ == "__main__":
    from xml.dom import minidom

    l = []
    l.append("test")
    l.append('test')
    l.append('test')
    for u in l:
        print(u)
    xmldoc = minidom.parse(
        'E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/913119/913119_mets.xml'
    )
    # xmldoc = minidom.parse
    # ('E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/108192/108192_mets.xml')
    # xmldoc = minidom.parse(
    #     'E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/' +
    #     '1447421/1447421_mets.xml')

    # no aut
    # xmldoc = minidom.parse(
    #     'E:/Databases/unibas_eManuscripta_firstExamples/emanusswa/' +
    #     '1013350/1013350_mets.xml')
    logStruct = getLogicalStructure(xmldoc)
    (dmdId, id) = getIds(logStruct)
    print(dmdId)
    if dmdId != -1 and id != -1:
        personList = getPersonList(dmdId, xmldoc)
        author = getAuthor(personList)
        if author == 0:
            print("no author found")
            quit()
        fileLinks = getFileLinks(id, xmldoc)
        physStruct = getPhysicalStructure(xmldoc)
        files = []
        for f in fileLinks:
            file = getFiles(f, physStruct)
            for f in file:
                files.append(f)

        print("\n\n\nauthor:" + author)
        print("files:" + str(files))
