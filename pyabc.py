tune1 = """
X: 1
T: The Road To Lisdoonvarna
R: slide
M: 12/8
L: 1/8
K: Edor
E2B B2A B2c d2A|F2A ABA D2E FED|E2B B2A B2c d3|cdc B2A B2E E3:|
|:e2f gfe d2B Bcd|c2A ABc d2B B3|e2f gfe d2B Bcd|cdc B2A B2E E3:|| 
"""


class ABC(object):
    def __init__(self, abc):
        self.parse_abc(abc)
        
    def parse_abc(self, abc):
        self.abc = abc
        keys = 'XTRMLK'
        header = []
        tune = []
        in_tune = False
        for line in abc.split('\n'):
            if line.strip() == '':
                continue
            if not in_tune:
                if line[0] in keys and line[1] == ':':
                    header.append(line)
                else:
                    in_tune = True
               
            if in_tune:
                tune.append(line)
                
        self.parse_header(header)
        self.parse_tune(tune)
        
    def parse_header(self, header):
        self.header = header
        
    def parse_tune(self, tune):
        self.tune = tune


if __name__ == '__main__':
    abc = ABC(tune1)
