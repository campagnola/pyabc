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
# Columns are:
# X:Field, file header, tune header, tune body, inline, type
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

file_header_fields = {k:v for k,v in info_keys.items() if v.file_header}
tune_header_fields = {k:v for k,v in info_keys.items() if v.tune_header}
tune_body_fields = {k:v for k,v in info_keys.items() if v.tune_body}
inline_fields = {k:v for k,v in info_keys.items() if v.inline}



# map natural note letters to chromatic values 
notes_values = {'A': 0, 'B': 2, 'C': 3, 'D': 5, 'E': 7, 'F': 8, 'G': 10}
accidental_values = {'': 0, '#': 1, 'b': -1}
for n,v in list(notes_values.items()):
    for a in '#b':
        notes_values[n+a] = v + accidental_values[a]

# map chromatic number back to most common key names
chromatic_notes = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']

# map mode names relative to Ionian (in chromatic steps)
mode_values = {'major': 0, 'minor': 3, 'ionian': 0, 'aeolian': 3, 
               'mixolydian': -7, 'dorian': -2, 'phrygian': -4, 'lydian': -5, 
               'locrian': 1}

# mode name normalization
mode_abbrev = {m[:3]: m for m in mode_values}

# sharps/flats in ionian keys
key_sig = {'C#': 7, 'F#': 6, 'B': 5, 'E': 4, 'A': 3, 'D': 2, 'G': 1, 'C': 0,
           'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7}
sharp_order = "FCGDAEB"
flat_order = "BEADGCF"


class Key(object):
    def __init__(self, name=None, root=None, mode=None):
        if name is not None:
            self.root, self.mode = self.parse_key(name)
            assert root is None and mode is None
        else:
            self.root = Pitch(root)
            self.mode = mode
            
        
    def parse_key(self, key):
        # highland pipe keys
        if key in ['HP', 'Hp']:
            return {'F': 1, 'C': 1, 'G': 0}
        
        base, acc, mode, extra = re.match(r'([A-G])(\#|b)?\s*(\w+)?(.*)', key).groups()
        if acc is None:
            acc = ''
        if mode is None:
            mode = 'major'
        try:
            mode = mode_abbrev[mode[:3].lower()]
        except KeyError:
            raise ValueError("Unrecognized key signature %s" % key)
        
        return Pitch(base+acc), mode
            
    @property
    def accidentals(self):
        """
        List of accidentals that should be displayed in the key
        signature for the given key description.
        """
        # determine number of sharps/flats for this key by first converting
        # to ionian, then doing the key lookup
        key = self.relative_ionian
        num_acc = key_sig[key.root.name]
        
        sig = []
        # sharps or flats?
        if num_acc > 0:
            for i in range(num_acc):
                sig.append(sharp_order[i] + '#')
        else:
            for i in range(-num_acc):
                sig.append(flat_order[i] + 'b')
        
        return sig
    
    @property
    def relative_ionian(self):
        """
        Return the ionian mode relative to the given key and mode.
        """
        key, mode = self.root, self.mode
        rel = mode_values[mode]
        return Key(root=(key.value + rel) % 12, mode='ionian')
    
    def __repr__(self):
        return "<Key %s %s>" % (self.root.name, self.mode)


class Pitch(object):
    def __init__(self, value, octave=None):
        if isinstance(value, Note):
            self._note = value
            self._name = value.note
            self._value = self.pitch_value(value.note)
            assert octave is None
            self._octave = value.octave
        elif isinstance(value, str):
            self._name = value
            self._value = self.pitch_value(value)
            self._octave = octave
        elif isinstance(value, Pitch):
            self._name = value._name
            self._value = value._value
            self._octave = value._octave
        else:
            self._name = None
            self._value = value  # 0-11
            self._octave = octave

    def __repr__(self):
        return "<Pitch %s>" % self.name
    
    @property
    def name(self):
        if self._name is not None:
            return self._name
        return chromatic_notes[self.value]
        
    @property
    def value(self):
        return self._value

    @staticmethod
    def pitch_value(pitch, root='A'):
        """Convert a pitch string like "A#" to a chromatic scale value relative
        to root.
        """
        pitch = pitch.strip()
        val = notes_values[pitch[0].upper()]
        if len(pitch) == 2:
            val += accidental_values[pitch[1]]
        if root == 'A':
            return val
        return (val - Pitch.pitch_value(root)) % 12

    def __eq__(self, a):
        return self.value == a.value
    

# Decoration symbols from
# http://abcnotation.com/wiki/abc:standard:v2.1#decorations
symbols = """
!trill!                "tr" (trill mark)
!trill(!               start of an extended trill
!trill)!               end of an extended trill
!lowermordent!         short /|/|/ squiggle with a vertical line through it
!uppermordent!         short /|/|/ squiggle
!mordent!              same as !lowermordent!
!pralltriller!         same as !uppermordent!
!roll!                 a roll mark (arc) as used in Irish music
!turn!                 a turn mark (also known as gruppetto)
!turnx!                a turn mark with a line through it
!invertedturn!         an inverted turn mark
!invertedturnx!        an inverted turn mark with a line through it
!arpeggio!             vertical squiggle
!>!                    > mark
!accent!               same as !>!
!emphasis!             same as !>!
!fermata!              fermata or hold (arc above dot)
!invertedfermata!      upside down fermata
!tenuto!               horizontal line to indicate holding note for full duration
!0! - !5!              fingerings
!+!                    left-hand pizzicato, or rasp for French horns
!plus!                 same as !+!
!snap!                 snap-pizzicato mark, visually similar to !thumb!
!slide!                slide up to a note, visually similar to a half slur
!wedge!                small filled-in wedge mark
!upbow!                V mark
!downbow!              squared n mark
!open!                 small circle above note indicating open string or harmonic
!thumb!                cello thumb symbol
!breath!               a breath mark (apostrophe-like) after note
!pppp! !ppp! !pp! !p!  dynamics marks
!mp! !mf! !f! !ff!     more dynamics marks
!fff! !ffff! !sfz!     more dynamics marks
!crescendo(!           start of a < crescendo mark
!<(!                   same as !crescendo(!
!crescendo)!           end of a < crescendo mark, placed after the last note
!<)!                   same as !crescendo)!
!diminuendo(!          start of a > diminuendo mark
!>(!                   same as !diminuendo(!
!diminuendo)!          end of a > diminuendo mark, placed after the last note
!>)!                   same as !diminuendo)!
!segno!                2 ornate s-like symbols separated by a diagonal line
!coda!                 a ring with a cross in it
!D.S.!                 the letters D.S. (=Da Segno)
!D.C.!                 the letters D.C. (=either Da Coda or Da Capo)
!dacoda!               the word "Da" followed by a Coda sign
!dacapo!               the words "Da Capo"
!fine!                 the word "fine"
!shortphrase!          vertical line on the upper part of the staff
!mediumphrase!         same, but extending down to the centre line
!longphrase!           same, but extending 3/4 of the way down
"""



class Token(object):
    def __init__(self, line, char, text):
        self._line = line
        self._char = char
        self._text = text

    def __repr__(self):
        return "<%s \"%s\">" % (self.__class__.__name__, self._text)


class Note(Token):
    def __init__(self, key_sig, note, accidental, octave, num, denom, **kwds):
        Token.__init__(self, **kwds)
        self.key_sig = key_sig
        self.note = note
        self.accidental = accidental
        self.octave = octave
        self.length = (num, denom)
        
    @property
    def pitch(self):
        """Chromatic note value taking into account key signature and transpositions.
        """
        return Pitch(self)




class Beam(Token):
    pass

class Space(Token):
    pass

class Slur(Token):
    """   ( or )   """
    pass

class Newline(Token):
    pass

class Continuation(Token):
    """  \ at end of line  """
    pass

class GracenoteBrace(Token):
    """  {  {/  or }  """
    pass

class ChordBracket(Token):
    """  [  or  ]  """
    pass

class ChordSymbol(Token):
    """   "Amaj"   """
    pass

class Annotation(Token):
    """    "<stuff"   """
    pass

class Decoration(Token):
    """  .~HLMOPSTuv  """
    pass

class Tuplet(Token):
    """  (5   """
    def __init__(self, num, **kwds):
        Token.__init__(self, **kwds)
        self.num = num

class BodyField(Token):
    pass

class InlineField(Token):
    pass

class Rest(Token):
    def __init__(self, char, num, denom, **kwds):
        # char==X or Z means length is in measures
        Token.__init__(self, **kwds)
        self.char = char
        self.length = (num, denom)
        
    


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
                elif line[:2] == '+:':
                    header[-1] += ' ' + line[2:]
                
        self.parse_header(header)
        self.parse_tune(tune)
        
    def parse_header(self, header):
        h = {}
        for line in header:
            key = line[0]
            data = line[2:].strip()
            h[info_keys[key].name] = data
        self.header = h
        self.reference = h['reference number']
        self.title = h['tune title']
        self.key = h['key']
            
    def parse_tune(self, tune):
        meter = self.header.get('meter', 'free')
        unit = self.header.get('unit note length', None)
        # determine default unit note length from meter if possible
        if unit is None and meter != 'free':
            if eval(meter) < 0.75:
                unit = "1/16"
            else:
                unit = "1/8"
        
        self.tokens = self.tokenize(tune, header)
        
    def tokenize(self, tune, header):
        key = KeySignature(self.header['key'])
        
        tokens = []
        for i,line in enumerate(tune):
            print line
            line = line.rstrip()
            
            if len(line) > 2 and line[1] == ':' and (line[0] == '+' or line[0] in tune_body_fields):
                tokens.append(BodyField(line=i, char=0, text=line))
                continue
            
            j = 0
            while j < len(line):
                part = line[j:]

                # Field
                if part[0] == '[' and len(part) > 3 and part[2] == ':':
                    fields = ''.join(inline_fields.keys())
                    m = re.match('\[[%s]:([^\]]+)\]' % fields, part)
                    if m is not None:
                        tokens.append(InlineField(line=i, char=j, text=m.group()))
                        j += m.end()
                        continue
                
                # Space
                m = re.match('(\s+)', part)
                if m is not None:
                    tokens.append(Space(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Note
                # Examples:  c  E'  _F2  ^^G,/4  =a,',3/2 
                m = re.match(r"(\^|\^\^|=|_|__)?([a-gA-G])([,']*)(\d+)?(/(\d+))?", part)
                if m is not None:
                    g = m.groups()
                    octave = 0
                    if g[2] is not None:
                        octave -= g[2].count(",")
                        octave += g[2].count("'")
                    tokens.append(Note(key_sig=key, note=g[1], accidental=g[0], octave=octave, num=g[3], denom=g[5], line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Beam  |   :|   |:   ||   and Chord  [ABC]
                m = re.match('([\[\]\|\:]+)([0-9\-,])?', part)
                if m is not None:
                    if m.group() in '[]':
                        tokens.append(ChordBracket(line=i, char=j, text=m.group()))                        
                    else:
                        tokens.append(Beam(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Broken rhythm
                if isinstance(tokens[-1], (Note, Rest)):
                    m = re.match('<+|>+', part)
                    if m is not None:
                        tokens.append(Dot(line=i, char=j, text=m.group()))
                        j += m.end()
                        continue

                # Rest
                m = re.match('([XZxz])(\d+)?(/(\d+))?', part)
                if m is not None:
                    g = m.groups()
                    tokens.append(Rest(g[0], num=g[1], denom=g[3], line=i, char=j, text=m.group()))
                    j += m.end()
                    continue
                    
                # Tuplets  (must parse before slur)
                m = re.match('\(([2-9])', part)
                if m is not None:
                    tokens.append(Tuplet(num=m.groups()[0], line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Slur
                if part[0] in '()':
                    tokens.append(Slur(line=i, char=j, text=part[0]))
                    j += 1
                    continue

                # Embelishments
                m = re.match('(\{\\?)|\}', part)
                if m is not None:
                    tokens.append(GracenoteBrace(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue
                
                # Decorations (single character)
                if part[0] in '.~HLMOPSTuv':
                    tokens.append(Decoration(line=i, char=j, text=part[0]))
                    j += 1
                    continue
                
                # Decorations (!symbol!)
                m = re.match('\!([^\! ]+)\!', part)
                if m is not None:
                    tokens.append(Decoration(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue
                
                # Continuation
                if j == len(line) - 1 and j == '\\':
                    tokens.append(Continuation(line=i, char=j, text='\\'))
                    j += 1
                    continue
                
                # Annotation
                m = re.match('"[\^\_\<\>\@][^"]+"', part)
                if m is not None:
                    tokens.append(Annotation(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Chord symbol
                m = re.match('"[\w]+"', part)
                if m is not None:
                    tokens.append(ChordSymbol(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue
                
                raise Exception("Unable to parse: %s" % part)
                
            if not isinstance(tokens[-1], Continuation):
                tokens.append(Newline(line=i, char=j, text='\n'))
                
        return tokens
            
        

if __name__ == '__main__':
    import user
    tune = Tune(tunes[0])
    
    print("Header: %s" % tune.header)
