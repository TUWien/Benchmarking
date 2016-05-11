#!/usr/local/bin/python

""" module for parsing the mets file. use parsemets to get author and filelist"""


STRUCT_MAP = 'mets:structMap'
DIV_ELEMENT = 'mets:div'
DMD_SECTION = 'mets:dmdSec'
NAME_ELEMENT = 'mods:name'
ROLE_ELEMENT = 'mods:roleTerm'


def getLogicalStructure(xmldoc):
    from xml.dom import minidom

    # print("getting logical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "LOGICAL":
            return i


def getPhysicalStructure(xmldoc):

    # print("getting physical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "PHYSICAL":
            return i


def getIds(logStruct):

    # print("getting Ids")
    itemlist = logStruct.getElementsByTagName(DIV_ELEMENT)
    dmdId = -1
    id = -1
    for i in itemlist:
        if i.attributes['TYPE'].value == "document":
            dmdId = i.attributes['DMDID'].value
            id = i.attributes['ID'].value
            # print("dmdid:" + dmdId)
            # print("id:" + id)
    return(dmdId, id)


def getPersonList(dmdId, xmldoc):
    # print("searching for dmdSec")

    itemlist = xmldoc.getElementsByTagName(DMD_SECTION)

    plist = []
    for i in itemlist:
        if i.attributes['ID'].value == dmdId:
            nodes = i.getElementsByTagName(NAME_ELEMENT)
            for n in nodes:
                if n.hasAttribute("usage") and n.attributes['usage'].value == "primary":
                    return [n]
            return nodes


def getAuthor(personList):

    name = 0
    date = 0
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
                                date = n.firstChild.nodeValue
                        else:
                            name = n.firstChild.nodeValue

    return name, date


def getFileLinks(id, xmldoc):

    # print("searching for files")
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

    # print("getting files for fileLink:" + link)
    itemlist = physStruct.getElementsByTagName(DIV_ELEMENT)
    fileList = []
    for item in itemlist:
        if item.hasAttribute("ID") and item.attributes['ID'].value == link:
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
    import writer
    import os

    author = []
    files = []
    cur_dir = os.path.dirname(filepath)
    xmldoc = minidom.parse(filepath)
    logStruct = getLogicalStructure(xmldoc)
    (dmdId, id) = getIds(logStruct)
    cur_writer = 0
    if dmdId != -1 and id != -1:
        personList = getPersonList(dmdId, xmldoc)
        (author,date) = getAuthor(personList)
        if author == 0:
            print("no author found")
        else:
            cur_writer = writer.Writer(author, [], date)
            fileLinks = getFileLinks(id, xmldoc)
            physStruct = getPhysicalStructure(xmldoc)
            files = []

            for f in fileLinks:
                file = getFiles(f, physStruct)
                for f in file:
                    # TODO : CHANGE ME!!!!
                    fullPath = cur_dir + "\\img\\" + f + ".jpg"
                    cur_writer.addPage(fullPath)

            # print("\n\n\nauthor:" + author)
            # print("files:" + str(cur_writer.pages))

    return cur_writer


if __name__ == "__main__":
    from xml.dom import minidom

    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/913119/913119_mets.xml'
    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/108192/108192_mets.xml'
    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/emanusbau/1447421/1447421_mets.xml'

    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/1178030/1178030_mets.xml'
    # no author
    # filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/emanusswa/1013350/1013350_mets.xml'
    parsemets(filepath)