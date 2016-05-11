#!/usr/local/bin/python

""" classes for writer identification """


class Writer:
    """ Saves the author information and the list of his pages"""

    def __init__(self, name="", pages = [], date = []):
        self.name = name
        self.pages = pages
        self.date = date

    def addPages(self, newpages: list):
        for n in newpages:
            self.pages.append(n)

    def addPage(self, newpages: str):
        self.pages.append(newpages)
