import re

from utils.FileMaker import FileMaker


class Matcher:

    def __init__(self, full_path):
        self.file = FileMaker(full_path, 'r')
        self.file.read()

    def re_findall(self, reg):
        return re.findall(reg, self.file.content, flags=re.VERBOSE)

    def re_search(self, reg):
        return re.search(reg, self.file.content, flags=re.VERBOSE)
