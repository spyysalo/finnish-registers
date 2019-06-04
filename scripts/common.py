import re

from glob import glob
from logging import error, warning, info


EN_ANY_CLASS_COMMENT_RE = re.compile(r'^# \S+\/\d+\+[A-Z]{2}[+_].*')

EN_TARGET_CLASS_COMMENT_RE = re.compile(r'^# \S+\/1\+[A-Z]{2}\+([A-Z]{2})\+.*')

EN_DOCID_COMMENT_RE = re.compile(r'^# <(\d+)>\s*$')

FI_CLASS_COMMENT_RE = re.compile(r'^#.*?\bregister:(.*)')


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
    'OS': 'Spoken',
    'UC': None,
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
    'Spoken': 'Spoken',
    'Lyrical': 'Lyrical',
    None: None,
}

EN_CLASS_MAP = {
    # None: 'MT/Gen',              # 'Machine-translated / generated texts' [not in English data]
    'DS': 'D-Sell',                # 'Description with intent to sell'
    'PB': 'B-Personal',            # 'Personal blog'
    'DT': 'D-Thing',               # 'Description of a thing'
    'NE': 'News',                  # 'News reports / News blogs'
    'HT': 'How-to',                # 'How-to/instructions'
    'RS': 'Religious',             # 'Religious blogs/sermons'
    'OB': 'B-Personal-Opinion',    # 'Personal opinion blogs'
    'PO': 'Poems',                 # 'Poems'
    'DF': 'Forums',                # 'Discussion forums'
    'RV': 'Reviews',               # 'Reviews'
    'EN': 'A-Encyclopedia',        # 'Encyclopedia articles'
    # None: 'B-Community',         # 'Community blogs' [not in English data]
    'SR': 'Sports',                # 'Sports reports'
    'ED': 'Editorials',            # 'News+Opinion blogs / Editorials'
    'DP': 'D-Person',              # 'Description of a person'
    'IB': 'B-Information',         # 'Information blogs'
    'MA': 'A-Online',              # 'Magazine article'
    'RA': 'A-Research',            # 'Research articles'
    'HA': 'A-Historical',          # 'Historical article'
    'QA': 'QA-forums',             # 'Question-Answer forums'
    'AV': 'Advice',                # 'Advice'
    'TB': 'B-Travel',              # 'Travel blog'
    'NA': 'Narrative',             # 'Narrative general'
    'ID': 'Discussion',            # 'Interactive discussion general'
    'SS': 'Fiction',               # 'Short stories'
    'FI': 'FAQs',                  # 'FAQs'
    'LT': 'Legal',                 # 'Legal terms / conditions'
    'IN': 'D-Informational',       # 'Informational Description general'
    'CM': 'Course',                # 'Course materials'
    'IT': 'Interviews',            # 'Interviews'
    # None: 'Report',              # 'Report' [not in English data]
    'FS': 'Speeches',              # 'Formal speeches'
    'RE': 'Recipes',               # 'Recipes'
    'IP': 'Info-Persuasion',       # 'Informational Persuasion general'
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


class WordLex(object):
    """Memory-saving option"""
    def __init__(self, word):
        self.id = word.id
        self.form = word.form
        self.lemma = word.lemma
        self.upos = word.upos


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


def load_conllu_lexonly(fn):
    with open(fn) as f:
        for comments, words in parse_conllu(f):
            words = [WordLex(w) for w in words]
            yield comments, words


def en_is_new_document(comments):
    class_comments = [c for c in comments if EN_ANY_CLASS_COMMENT_RE.match(c)]
    docid_comments = [c for c in comments if EN_DOCID_COMMENT_RE.match(c)]
    if class_comments:
        if not docid_comments:
            warning('class but no document id:\n{}'.format('\n'.join(comments)))
        return True
    elif docid_comments:
        warning('document id but no class:\n{}'.format('\n'.join(comments)))
    return False


def en_get_document_id(comments):
    matches = [c for c in comments if EN_DOCID_COMMENT_RE.match(c)]
    if not matches:
        error('No id line found:\n{}'.format('\n'.join(comments)))
        return None
    elif len(matches) > 1:
        warning('Expected one document id line, got {} (using last): {}'.format(
            len(matches), matches))
    m = EN_DOCID_COMMENT_RE.match(matches[-1])
    return m.group(1)


def en_get_document_class(comments):
    """Return document class from comments or None if not found or ambiguous."""
    doc_id = en_get_document_id(comments)
    matches = [c for c in comments if EN_ANY_CLASS_COMMENT_RE.match(c)]
    if not matches:
        error('No class label line found for {}:\n{}'.format(
            doc_id, '\n'.join(comments)))
        return None
    elif len(matches) > 1:
        warning('Expected one class label line, got {} for {} (using last): {}'\
                .format(len(matches), doc_id, matches))
    m = EN_TARGET_CLASS_COMMENT_RE.match(matches[-1])
    if not m:
        info('returning None class for class label line: {}'.format(matches[0]))
        return None
    return m.group(1)



def en_load_parsed_data(fn, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []
    sentences, class_, exclude = [], None, False
    for comments, sentence in load_conllu(fn):
        if en_is_new_document(comments):
            if class_ is not None and not exclude:
                assert sentences
                yield class_, sentences
            sentences = []
            class_ = en_get_document_class(comments)
            if class_ is not None:
                class_ = ENGLISH_MAIN_REGISTER[class_]
            class_ = CLASS_ABBREV_MAP[class_]
            exclude = en_get_document_id(comments) in exclude_ids
        sentences.append(sentence)
    if class_ is not None:
        assert sentences
        yield class_, sentences


def fi_get_class_from_comments(comments):
    class_ = None
    for comment in comments:
        m = FI_CLASS_COMMENT_RE.match(comment)
        if m:
            if class_:
                raise ValueError('duplicate class')
            class_ = m.group(1)
    return class_


def fi_load_conllu_with_class(fn):
    sentences, class_ = [], None
    for comments, sentence in load_conllu(fn):
        c = fi_get_class_from_comments(comments)
        if c is not None:
            if class_ is not None:
                raise ValueError('duplicate class')
            class_ = c
        sentences.append(sentence)
    if class_ is None:
        raise ValueError('missing class in {}'.format(fn))
    class_ = FINNISH_MAIN_REGISTER[class_]
    return sentences, CLASS_ABBREV_MAP[class_]


def fi_load_parsed_data(dirpath):
    parses, classes = [], []
    for fn in glob('{}/*.conllu'.format(dirpath)):
        sentences, class_ = fi_load_conllu_with_class(fn)
        if class_ is None:
            continue    # class doesn't map across languages
        yield class_, sentences
