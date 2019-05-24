CLASS_MAP = {
    'Machine-translated / generated texts': 'MT/Gen',
    'Description with intent to sell': 'D-Sell',
    'Personal blog': 'B-Personal',
    'Description of a thing': 'D-Thing',
    'News reports / News blogs': 'News',
    'News reports / news blogs': 'News',    # typo fix
    'How-to/instructions': 'How-to',
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
