class FileMaker:

    def __init__(self, full_path, mode, encoding='utf-8'):
        self.full_path = None
        self.mode = None
        self.content = None
        try:

            self.file = open(full_path, mode)
        except Exception as e:
            print('File creation failed!')
            print(e)

    def write(self, content):
        self.file.write(content)
        self.file.close()
        print(f'{self.file.name} creation succeed!')

    def read(self):
        self.content = self.file.read()
        self.file.close()
        print(f'{self.file.name} read succeed!')


if __name__ == '__main__':
    fm = FileMaker('/Users/wukailang/Desktop/GameZone/files/linksListFiles/demo.txt', 'r')
    fm.read()
    print(fm.content)
