import re


# Just some tunes to test against
tunes = [
"""
X: 1
T: The Road To Lisdoonvarna
R: slide
M: 12/8
L: 1/8
K: Edor
E2B B2A B2c d2A|F2A ABA D2E FED|E2B B2A B2c d3|cdc B2A B2E E3:|
|:e2f gfe d2B Bcd|c2A ABc d2B B3|e2f gfe d2B Bcd|cdc B2A B2E E3:|| 
""",
"""
X: 6
T: The Kid On The Mountain
R: slip jig
M: 9/8
L: 1/8
K: Emin
~E3 FEF G2 F| ~E3 BcA BGD| ~E3 FEF G2 A| BAG FAG FED:|
BGB AFD G2 D| GAB dge dBA| BGB AFA G2 A| BAG FAG FED:|
~g3 eBe e2 f|~g3 efg afd| ~g3 eBe g2 a|bag fag fed:|
eB/B/B e2f ~g3|eB/B/B efg afd| eB/B/B e2f g2a|bag fag fed:|
edB dBA G2D|GAB dge dBA|edB dBA G2A|BAG FAG FED:| 
"""
]

# Information field table copied from
# http://abcnotation.com/wiki/abc:standard:v2.1#abc_files_tunes_and_fragments
information_field_table = """
A:area              yes     yes     no      no      string
B:book              yes     yes     no      no      string
C:composer          yes     yes     no      no      string
D:discography       yes     yes     no      no      string
F:file url          yes     yes     no      no      string
G:group             yes     yes     no      no      string
H:history           yes     yes     no      no      string
I:instruction       yes     yes     yes     yes     instruction
K:key               no      yes     yes     yes     instruction
L:unit note length  yes     yes     yes     yes     instruction
M:meter             yes     yes     yes     yes     instruction
m:macro             yes     yes     yes     yes     instruction
N:notes             yes     yes     yes     yes     string
O:origin            yes     yes     no      no      string
P:parts             no      yes     yes     yes     instruction
Q:tempo             no      yes     yes     yes     instruction
R:rhythm            yes     yes     yes     yes     string
r:remark            yes     yes     yes     yes     -
S:source            yes     yes     no      no      string
s:symbol line       no      no      yes     no      instruction
T:tune title        no      yes     yes     no      string
U:user defined      yes     yes     yes     yes     instruction
V:voice             no      yes     yes     yes     instruction
W:words             no      yes     yes     no      string
w:words             no      no      yes     no      string
X:reference number  no      yes     no      no      instruction
Z:transcription     yes     yes     no      no      string
"""

class InfoKey(object):
    def __init__(self, key, name, file_header, tune_header, tune_body, inline, type):
        self.key = key  # single-letter field identifier
        self.name = name.strip()  # information field name
        self.file_header = file_header=='yes'  # may be used in file header
        self.tune_header = tune_header=='yes'  # may be used in tune header
        self.tune_body = tune_body=='yes'  # may be used in tune body
        self.inline = inline=='yes'  # nay be used inline in tunes
        self.type = type.strip()  # data type:  string, instruction, or -

# parse info field table
info_keys = {}
for line in information_field_table.split('\n'):
    if line.strip() == '':
        continue
    key = line[0]
    fields = re.match(r'(.*)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(.*)', line[2:]).groups()
    info_keys[key] = InfoKey(key, *fields)






class Tune(object):
    def __init__(self, abc):
        self.parse_abc(abc)
        
    def parse_abc(self, abc):
        self.abc = abc
        header = []
        tune = []
        in_tune = False
        for line in abc.split('\n'):
            line = re.split(r'([^\\]|^)%', line)[0]
            line = line.strip()
            if line == '':
                continue
            if in_tune:
                tune.append(line)
            else:
                if line[0] in info_keys and line[1] == ':':
                    header.append(line)
                    if line[0] == 'K':
                        in_tune = True
                
        self.parse_header(header)
        self.parse_tune(tune)
        
    def parse_header(self, header):
        h = {}
        for line in header:
            key = line[0]
            data = line[2:].strip()
            h[info_keys[key].name] = data
        self.header = h
        print h
        self.reference = h['reference number']
        self.title = h['tune title']
        self.key = h['key']
            
        
    def parse_tune(self, tune):
        self.tune = tune


if __name__ == '__main__':
    t = Tune(tunes[0])
