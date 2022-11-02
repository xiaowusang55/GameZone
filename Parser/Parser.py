import pprint
import re

from utils.FileMaker import FileMaker


class Parser:

    def __init__(self):
        self.result = None

    def parse(self, full_path, reg):
        """
        :param full_path: full file path
        :param reg: regular expression
        :return: None
        """
        fm = FileMaker(full_path, 'r')
        fm.read()
        self.result = re.findall(reg, fm.content, flags=re.VERBOSE)


if __name__ == '__main__':
    lp = Parser()
    regxe = r"""
    <a\s
    href="(.*?)"\s.*?>       # find href attribute with () group
    <img\ssrc="(.*?)"\s.*?>  # find src attribute with () group
    <div\s.*?>(.*?)</div>  # find contents of tag with () group
    <p>(.*?)</p>           # find contents of tag with () group
    </a>
    """
    lp.parse(full_path='/Users/wukailang/Documents/GameZoneFiles/linksListFiles/第1页.txt', reg=regxe)
    pprint.pprint(lp.result[0])
