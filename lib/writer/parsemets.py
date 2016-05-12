#!/usr/local/bin/python

""" module for parsing the mets file to get author and filelist"""


STRUCT_MAP = 'mets:structMap'
DIV_ELEMENT = 'mets:div'
DMD_SECTION = 'mets:dmdSec'
NAME_ELEMENT = 'mods:name'
ROLE_ELEMENT = 'mods:roleTerm'


def get_logical_structure(xmldoc):
    from xml.dom import minidom

    # print("getting logical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "LOGICAL":
            return i


def get_physical_structure(xmldoc):

    # print("getting physical structure")
    itemlist = xmldoc.getElementsByTagName(STRUCT_MAP)
    for i in itemlist:
        if i.attributes['TYPE'].value == "PHYSICAL":
            return i


def get_ids(logstruct):

    # print("getting Ids")
    itemlist = logstruct.getElementsByTagName(DIV_ELEMENT)
    dmdid = -1
    id = -1
    for i in itemlist:
        if i.attributes['TYPE'].value == "document":
            dmdid = i.attributes['DMDID'].value
            id = i.attributes['ID'].value
            # print("dmdid:" + dmdid)
            # print("id:" + id)
    return(dmdid, id)


def get_person_list(dmdid, xmldoc):
    # print("searching for dmdSec")

    itemlist = xmldoc.getElementsByTagName(DMD_SECTION)

    for i in itemlist:
        if i.attributes['ID'].value == dmdid:
            nodes = i.getElementsByTagName(NAME_ELEMENT)
            for n in nodes:
                if n.hasAttribute("usage") \
                        and n.attributes['usage'].value == "primary":
                    return [n]
            return nodes


def get_author(personlist):

    name = 0
    date = 0
    for p in personlist:
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


def get_file_links(id, xmldoc):

    # print("searching for files")
    itemlist = xmldoc.getElementsByTagName('mets:structLink')

    filelinks = []
    for i in itemlist:
        for child in i.childNodes:
            if (
                child.hasAttribute("xlink:from") and
                child.attributes['xlink:from'].value == id
            ):
                    filelinks.append(child.attributes['xlink:to'].value)

    return filelinks


def get_files(link, physstruct):

    # print("getting files for fileLink:" + link)
    itemlist = physstruct.getElementsByTagName(DIV_ELEMENT)
    filelist = []
    for item in itemlist:
        if item.hasAttribute("ID") and item.attributes['ID'].value == link:
            for child in item.childNodes:
                if (
                    child.hasAttribute("FILEID") and
                    str(child.attributes['FILEID'].value).find("MAX", 0) > 0
                ):
                        file = child.attributes['FILEID'].value
                        filelist.append(file)
    return filelist


def parsemets(filepath):
    from xml.dom import minidom
    import writer
    import os

    author = []
    cur_dir = os.path.dirname(filepath)
    xmldoc = minidom.parse(filepath)
    logstruct = get_logical_structure(xmldoc)
    (dmdid, id) = get_ids(logstruct)
    cur_writer = 0
    if dmdid != -1 and id != -1:
        personlist = get_person_list(dmdid, xmldoc)
        (author, date) = get_author(personlist)
        if author == 0:
            print("no author found")
        else:
            cur_writer = writer.Writer(author, [], date)
            filelinks = get_file_links(id, xmldoc)
            physstruct = get_physical_structure(xmldoc)

            for f in filelinks:
                file = get_files(f, physstruct)
                for f in file:
                    # TODO : CHANGE ME!!!!
                    fullpath = cur_dir + "\\img\\" + f + ".jpg"
                    cur_writer.addPage(fullpath)

            # print("\n\n\nauthor:" + author)
            # print("files:" + str(cur_writer.pages))

    return cur_writer


if __name__ == "__main__":
    from xml.dom import minidom

    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
               'emanusbau/913119/913119_mets.xml'
    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
               'emanusbau/108192/108192_mets.xml'
    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
               'emanusbau/1447421/1447421_mets.xml'

    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
               '1178030/1178030_mets.xml'
    filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
               '1420675/1420675_mets.xml'
    # no author
    # filepath = 'E:/Databases/unibas_eManuscripta_firstExamples/' \
    #            'emanusswa/1013350/1013350_mets.xml'
    parsemets(filepath)
