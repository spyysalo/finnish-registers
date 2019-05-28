ENGLISH_MAIN_REGISTER = {
    'NE': 'Narrative',
    'SR': 'Narrative',
    'PB': 'Narrative',
    'HA': 'Narrative',
    'TB': 'Narrative',
    'SS': 'Narrative',
    'NO': 'Narrative',
    'BS': 'Narrative',
    'MA': 'Narrative',
    'OT': 'Narrative',
    'ME': 'Narrative',
    'ON': 'Narrative',
    'OB': 'Opinion',
    'RV': 'Opinion',
    'RS': 'Opinion',
    'AV': 'Opinion',
    'LE': 'Opinion',
    'SH': 'Opinion',
    'AD': 'Opinion',
    'OO': 'Opinion',
    'DT': 'Informational Description/Explanation',
    'IB': 'Informational Description/Explanation',
    'DP': 'Informational Description/Explanation',
    'RA': 'Informational Description/Explanation',
    'AB': 'Informational Description/Explanation',
    'FI': 'Informational Description/Explanation',
    'LT': 'Informational Description/Explanation',
    'CM': 'Informational Description/Explanation',
    'EN': 'Informational Description/Explanation',
    'OI': 'Informational Description/Explanation',
    'TR': 'Informational Description/Explanation',
    'DF': 'Interactive discussion',
    'QA': 'Interactive discussion',
    'RR': 'Interactive discussion',
    'OF': 'Interactive discussion',
    'HT': 'How-To/instructions',
    'RE': 'How-To/instructions',
    'IS': 'How-To/instructions',
    'FH': 'How-To/instructions',
    'TS': 'How-To/instructions',
    'OH': 'How-To/instructions',
    'DS': 'Informational Persuasion',
    'PA': 'Informational Persuasion',
    'ED': 'Informational Persuasion',
    'OE': 'Informational Persuasion',
    'SL': 'Lyrical',
    'PO': 'Lyrical',
    'OL': 'Lyrical',
    'PR': 'Lyrical',
    'IT': 'Spoken',
    'TA': 'Spoken',
    'FS': 'Spoken',
    'TV': 'Spoken',
    'OS': 'Spoken'
}

FINNISH_MAIN_REGISTER = {
    'Narrative general': 'Narrative',
    'News reports / News blogs': 'Narrative',
    'News reports / news blogs': 'Narrative',    # caps fix
    'Personal blog': 'Narrative',
    'Historical article': 'Narrative',
    'Fiction': 'Narrative',
    'Travel blog': 'Narrative',
    'Community blog': 'Narrative',
    'Online article': 'Narrative',
    'Informational Description general': 'Informational Description/Explanation',
    'Description of a thing': 'Informational Description/Explanation',
    'Encyclopedia articles': 'Informational Description/Explanation',
    'Research articles': 'Informational Description/Explanation',
    'Description of a person': 'Informational Description/Explanation',
    'Information blogs': 'Informational Description/Explanation',
    'FAQs': 'Informational Description/Explanation',
    'Course materials': 'Informational Description/Explanation',
    'Legal terms / conditions': 'Informational Description/Explanation',
    'Report': 'Informational Description/Explanation',
    'Opinion general': 'Opinion',
    'Reviews': 'Opinion',
    'Personal opinion blogs': 'Opinion',
    'Religious blogs/sermons': 'Opinion',
    'Advice': 'Opinion',
    'Interactive discussion general': 'Interactive discussion',
    'Discussion forums': 'Interactive discussion',
    'Question-Answer forums': 'Interactive discussion',
    'How-to/instructions': 'How-To/instructions',
    'Recipes': 'How-To/instructions',
    'Informational Persuasion general': 'Informational Persuasion',
    'Description with intent to sell':  'Informational Persuasion',
    'News+Opinion blogs / Editorials':'Informational Persuasion',
    'Songs': 'Lyrical',
    'Poems': 'Lyrical',
    'Interviews': 'Spoken',
    'Formal speeches': 'Spoken',
    'TV transcripts': 'Spoken',
    'Sports reports': 'Narrative',
    'Machine-translated / generated texts': None,    # not an English main reg
    'Community blogs': None,    # not an English main reg
}

CLASS_ABBREV_MAP = {
    'Machine-translated / generated texts': 'MT/Gen',
    'Description with intent to sell': 'D-Sell',
    'Personal blog': 'B-Personal',
    'Description of a thing': 'D-Thing',
    'News reports / News blogs': 'News',
    'News reports / news blogs': 'News',    # typo fix
    'How-to/instructions': 'How-to',
    'How-To/instructions': 'How-to',    # caps fix
    'Religious blogs/sermons': 'Religious',
    'Personal opinion blogs': 'B-Personal-Opinion',
    'Discussion forums': 'Forums',
    'Reviews': 'Reviews',
    'Encyclopedia articles': 'A-Encyclopedia',
    'Community blogs': 'B-Community',
    'Community blog': 'B-Community',    # typo fix
    'Sports reports': 'Sports',
    'News+Opinion blogs / Editorials': 'Editorials',
    'Description of a person': 'D-Person',
    'Information blogs': 'B-Information',
    'Online article': 'A-Online',
    'Research articles': 'A-Research',
    'Historical article': 'A-Historical',
    'Question-Answer forums': 'QA-forums',
    'Advice': 'Advice',
    'Travel blog': 'B-Travel',
    'Narrative general': 'Narrative',
    'Interactive discussion general': 'Discussion',
    'Fiction': 'Fiction',
    'FAQs': 'FAQs',
    'Legal terms / conditions': 'Legal',
    'Informational Description general': 'D-Informational',
    'Course materials': 'Course',
    'Interviews': 'Interviews',
    'Report': 'Report',
    'Formal speeches': 'Speeches',
    'Recipes': 'Recipes',
    'Informational Persuasion general': 'Info-Persuasion',
    'Interactive discussion': 'Discussion',
    'Opinion': 'Opinion',
    'Informational Description/Explanation': 'D-Informational',
    'Informational Persuasion': 'Info-Persuasion',
    'Narrative': 'Narrative',
    None: None,
}


class Word(object):
    def __init__(self, id_, form, lemma, upos, xpos, feats, head, deprel,
                 deps, misc):
        self.id = id_
        self.form = form
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.feats = feats
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

    def __str__(self):
        return '\t'.join([
            self.id, self.form, self.lemma, self.upos, self.xpos, self.feats,
            self.head, self.deprel, self.deps, self.misc
        ])


def load_conllu(fn):
    with open(fn) as f:
        for comments, words in parse_conllu(f):
            yield comments, words


def parse_conllu(f):
    comments, words = [], []
    for l in f:
        l = l.rstrip('\n')
        if not l or l.isspace():
            yield comments, words
            comments, words = [], []
        elif l.startswith('#'):
            comments.append(l)
        else:
            fields = l.split('\t')
            words.append(Word(*fields))
