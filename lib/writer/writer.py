#!/usr/local/bin/python

""" classes for writer identification """


class Writer:
    """ Saves the author information and the list of his pages"""

    def __init__(self, name="", pages=[], date=[]):
        self.name = name
        self.pages = pages
        self.date = date
        self.id = -1

    def addPages(self, newpages: list):
        for n in newpages:
            self.pages.append(n)

    def addPage(self, newpages: str):
        self.pages.append(newpages)


class WriterList:
    """stores the writes in a list and updates it"""
    def __init__(self):
        self.wlist = []
        self.__id = 0

    def add_or_update(self, writer: Writer):
        for w in self.wlist:
            if w.name == writer.name and w.date == writer.date:
                w.addPages(writer.pages)
                print("added pages to writer with id " + str(w.id))
                return w.id
            elif w.name == writer.name and w.date != writer.date:
                self.__id += 1
                writer.id = self.__id
                self.wlist.append(writer)
                print("date mismatch: created new writer with id " + str(self.__id))
                return self.__id
        # writer is not in list
        self.__id += 1
        writer.id = self.__id
        self.wlist.append(writer)
        print("created new writer with id " + str(self.__id))
        return self.__id

    def eliminate_duplicates(self):
        old_length = len(self.wlist)
        del_list = []
        for i in self.wlist:
            for j in self.wlist:
                if i.name == j.name and i.date != j.date:
                    if i.date == 0:
                        if i not in del_list and j not in del_list:
                            del_list.append(i)
                    elif j.date == 0:
                        if i not in del_list and j not in del_list:
                            del_list.append(j)
                    elif len(i.pages) <= len(j.pages):
                        if i not in del_list and j not in del_list:
                            del_list.append(i)

        # remove duplicates (taken from https://www.peterbe.com/plog/uniqifiers-benchmark
        del_list = list(set(del_list))
        for d in del_list:
            self.wlist.remove(d)
        for w in self.wlist:
            self.wlist = list(set(self.wlist))

        print("deleted " + str(old_length - len(self.wlist)) + " elements")

        self.wlist = sorted(self.wlist, key=lambda w: w.id)


    def get_last_id(self):
        return self.__id