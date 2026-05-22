#!/usr/bin/env python3
"""
0.10.py — Turkish Morphological Pipeline: Zemberek Simulation → NST Builder

Sprint 3.1: Simulates Zemberek morphological analysis output, constructs
Nested Semantic Trees from Turkish agglutinative morphology, and demonstrates
end-to-end search with precision/recall evaluation.

Key insight (from 0.4.md): Turkish agglutination encodes hierarchical
grammatical relations — each suffix adds scope, exactly like tree depth.

Morphological pipeline:
  1. Simulate Zemberek output (morpheme segmentation + grammatical tags)
  2. Build NST from morphological parse (each morpheme → tree node)
  3. Run subtree search queries against corpus
  4. Evaluate: Precision@k, Recall@k, F1, MRR

Grounded in:
  - 0.4.md: Cross-linguistic examples (Turkish, Mohawk, English)
  - 0.5.py: NST framework + matching engine
  - 0.9.py: Expanded corpus (12 documents, 5 languages)
"""

import sys
import json
from itertools import combinations
from collections import defaultdict


# ============================================================================
# 1. Nested Semantic Tree Framework (from 0.5.py, standalone)
# ============================================================================

class SemanticNode:
    __slots__ = ('id', 'label', 'category', 'parent_id', 'children', 'height',
                 'morphemes', 'gloss', 'pos')
    def __init__(self, nid, label, category, parent_id=None, height=0.0,
                 morphemes=None, gloss="", pos=""):
        self.id = nid
        self.label = label
        self.category = category
        self.parent_id = parent_id
        self.children = []
        self.height = height
        self.morphemes = morphemes or []
        self.gloss = gloss
        self.pos = pos


class NestedSemanticTree:
    def __init__(self, name="", language="unknown"):
        self.name = name
        self.language = language
        self.nodes = {}
        self.root = None
        self._depth = {}
        self._parent_jump = {}
        self._lca_preprocessed = False
        self._log_n = 0
        self._max_depth = 0

    def add_node(self, nid, label, category, parent_id=None, height=0.0,
                 morphemes=None, gloss="", pos=""):
        node = SemanticNode(nid, label, category, parent_id, height,
                            morphemes, gloss, pos)
        self.nodes[nid] = node
        if parent_id:
            self.nodes[parent_id].children.append(node)
        else:
            self.root = node
        return node

    def _assign_depths(self):
        if not self.root:
            return
        stack = [(self.root, 0)]
        self._depth[self.root.id] = 0
        self._max_depth = 0
        while stack:
            node, d = stack.pop()
            self._depth[node.id] = d
            self._max_depth = max(self._max_depth, d)
            for child in node.children:
                stack.append((child, d + 1))

    def _build_parent_jumps(self):
        log_n = max(1, (self._max_depth + 1).bit_length())
        up = {nid: [-1] * log_n for nid in self.nodes}
        for nid, node in self.nodes.items():
            up[nid][0] = node.parent_id if node.parent_id else -1
        for k in range(1, log_n):
            for nid in self.nodes:
                if up[nid][k - 1] != -1:
                    up[nid][k] = up[up[nid][k - 1]][k - 1]
        self._parent_jump = up
        self._log_n = log_n

    def preprocess_lca(self):
        self._assign_depths()
        self._build_parent_jumps()
        self._lca_preprocessed = True

    def lca(self, id1, id2):
        if not self._lca_preprocessed:
            self.preprocess_lca()
        d1, d2 = self._depth[id1], self._depth[id2]
        if d1 < d2:
            id1, id2 = id2, id1
            d1, d2 = d2, d1
        diff = d1 - d2
        for k in range(self._log_n):
            if (diff >> k) & 1:
                id1 = self._parent_jump[id1][k]
        if id1 == id2:
            return id1
        for k in range(self._log_n - 1, -1, -1):
            if self._parent_jump[id1][k] != self._parent_jump[id2][k]:
                id1 = self._parent_jump[id1][k]
                id2 = self._parent_jump[id2][k]
        return self._parent_jump[id1][0]

    def ultrametric_distance(self, id1, id2):
        return self.nodes[self.lca(id1, id2)].height

    def get_leaf_ids(self):
        return [nid for nid, n in self.nodes.items() if not n.children]

    def verify_ultrametric(self):
        leaves = self.get_leaf_ids()
        if len(leaves) < 3:
            return len(leaves), 0, 0
        violations, total = 0, 0
        for x, y, z in combinations(leaves, 3):
            total += 1
            if self.ultrametric_distance(x, z) > max(
                    self.ultrametric_distance(x, y),
                    self.ultrametric_distance(y, z)) + 1e-10:
                violations += 1
        return len(leaves), total, violations

    def get_yield_text(self, root_id=None):
        """Get the surface text (leaf morphemes concatenated)."""
        if root_id is None:
            root_id = self.root.id
        parts = []
        def collect(nid):
            node = self.nodes[nid]
            if not node.children:
                if node.label:
                    parts.append(node.label)
            else:
                for child in node.children:
                    collect(child.id)
        collect(root_id)
        return ' '.join(parts)


# ============================================================================
# 2. Zemberek Morphological Analyzer Simulator
# ============================================================================

class ZemberekSimulator:
    """
    Simulates Zemberek morphological analysis for Turkish.
    
    Zemberek (https://github.com/ahmetaa/zemberek-nlp) is a Turkish NLP
    library that performs morphological analysis, returning morpheme-level
    segmentation with grammatical tags.
    
    Real Zemberek output example:
      "kadina" → [kadin:Noun] + [A3sg] + [Dat]
      "aldim"  → [al:Verb] + [Past] + [A1sg]
    
    This simulator produces equivalent output for a curated set of Turkish
    sentences covering the same propositions as 0.4.md's cross-linguistic
    examples, plus additional query-relevant sentences.
    """
    
    # Turkish morphological lexicon: surface → (stem, POS, morphemes)
    LEXICON = {
        # Nouns
        'kadin':    ('kadin', 'Noun', [('kadin', 'ROOT', 'woman')]),
        'kadinin':  ('kadin', 'Noun', [('kadin', 'ROOT', 'woman'), ('in', 'GEN', 'of')]),
        'kadina':   ('kadin', 'Noun', [('kadin', 'ROOT', 'woman'), ('a', 'DAT', 'to')]),
        'ekmek':    ('ekmek', 'Noun', [('ekmek', 'ROOT', 'bread')]),
        'ekmegi':   ('ekmek', 'Noun', [('ekmek', 'ROOT', 'bread'), ('i', 'ACC', 'OBJ')]),
        'ekmekten': ('ekmek', 'Noun', [('ekmek', 'ROOT', 'bread'), ('ten', 'ABL', 'from')]),
        'dun':      ('dun', 'Noun', [('dun', 'ROOT', 'yesterday')]),
        'dukkan':   ('dukkan', 'Noun', [('dukkan', 'ROOT', 'store')]),
        'dukkanda': ('dukkan', 'Noun', [('dukkan', 'ROOT', 'store'), ('da', 'LOC', 'at')]),
        'dukkandan':('dukkan', 'Noun', [('dukkan', 'ROOT', 'store'), ('dan', 'ABL', 'from')]),
        'adam':     ('adam', 'Noun', [('adam', 'ROOT', 'man')]),
        'adamlar':  ('adam', 'Noun', [('adam', 'ROOT', 'man'), ('lar', 'PL', 'plural')]),
        'adamin':   ('adam', 'Noun', [('adam', 'ROOT', 'man'), ('in', 'GEN', 'of')]),
        'cocuk':    ('cocuk', 'Noun', [('cocuk', 'ROOT', 'child')]),
        'cocuklar': ('cocuk', 'Noun', [('cocuk', 'ROOT', 'child'), ('lar', 'PL', 'plural')]),
        'cocuga':   ('cocuk', 'Noun', [('cocuk', 'ROOT', 'child'), ('a', 'DAT', 'to')]),
        'kitap':    ('kitap', 'Noun', [('kitap', 'ROOT', 'book')]),
        'kitabi':   ('kitap', 'Noun', [('kitap', 'ROOT', 'book'), ('i', 'ACC', 'OBJ')]),
        'kitaptan': ('kitap', 'Noun', [('kitap', 'ROOT', 'book'), ('tan', 'ABL', 'from')]),
        'su':       ('su', 'Noun', [('su', 'ROOT', 'water')]),
        'sut':      ('sut', 'Noun', [('sut', 'ROOT', 'milk')]),
        'para':     ('para', 'Noun', [('para', 'ROOT', 'money')]),
        'parayi':   ('para', 'Noun', [('para', 'ROOT', 'money'), ('yi', 'ACC', 'OBJ')]),
        'ev':       ('ev', 'Noun', [('ev', 'ROOT', 'house')]),
        'eve':      ('ev', 'Noun', [('ev', 'ROOT', 'house'), ('e', 'DAT', 'to')]),
        'evden':    ('ev', 'Noun', [('ev', 'ROOT', 'house'), ('den', 'ABL', 'from')]),
        'pencere':  ('pencere','Noun', [('pencere','ROOT', 'window')]),
        'pencereyi':('pencere','Noun', [('pencere','ROOT', 'window'), ('yi', 'ACC', 'OBJ')]),
        
        # Verbs
        'aldi':     ('al', 'Verb', [('al', 'ROOT', 'buy'), ('di', 'PAST', 'PAST')]),
        'aldim':    ('al', 'Verb', [('al', 'ROOT', 'buy'), ('di', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'aldin':    ('al', 'Verb', [('al', 'ROOT', 'buy'), ('di', 'PAST', 'PAST'), ('n', 'A2SG', 'you')]),
        'alacak':   ('al', 'Verb', [('al', 'ROOT', 'buy'), ('acak', 'FUT', 'will')]),
        'aliyor':   ('al', 'Verb', [('al', 'ROOT', 'buy'), ('iyor', 'PROG', 'ing')]),
        'geldi':    ('gel', 'Verb', [('gel', 'ROOT', 'come'), ('di', 'PAST', 'PAST')]),
        'geldim':   ('gel', 'Verb', [('gel', 'ROOT', 'come'), ('di', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'geliyor':  ('gel', 'Verb', [('gel', 'ROOT', 'come'), ('iyor', 'PROG', 'ing')]),
        'gitti':    ('git', 'Verb', [('git', 'ROOT', 'go'), ('ti', 'PAST', 'PAST')]),
        'gidiyor':  ('git', 'Verb', [('git', 'ROOT', 'go'), ('iyor', 'PROG', 'ing')]),
        'verdi':    ('ver', 'Verb', [('ver', 'ROOT', 'give'), ('di', 'PAST', 'PAST')]),
        'verdim':   ('ver', 'Verb', [('ver', 'ROOT', 'give'), ('di', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'gordu':    ('gor', 'Verb', [('gor', 'ROOT', 'see'), ('du', 'PAST', 'PAST')]),
        'gordum':   ('gor', 'Verb', [('gor', 'ROOT', 'see'), ('du', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'gosterdi': ('goster','Verb', [('goster','ROOT', 'show'), ('di', 'PAST', 'PAST')]),
        'yapti':    ('yap', 'Verb', [('yap', 'ROOT', 'do'), ('ti', 'PAST', 'PAST')]),
        'yaptim':   ('yap', 'Verb', [('yap', 'ROOT', 'do'), ('ti', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'icti':     ('ic', 'Verb', [('ic', 'ROOT', 'drink'), ('ti', 'PAST', 'PAST')]),
        'ictim':    ('ic', 'Verb', [('ic', 'ROOT', 'drink'), ('ti', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'yedi':     ('ye', 'Verb', [('ye', 'ROOT', 'eat'), ('di', 'PAST', 'PAST')]),
        'yedim':    ('ye', 'Verb', [('ye', 'ROOT', 'eat'), ('di', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        'kirdi':    ('kir', 'Verb', [('kir', 'ROOT', 'break'), ('di', 'PAST', 'PAST')]),
        'acti':     ('ac', 'Verb', [('ac', 'ROOT', 'open'), ('ti', 'PAST', 'PAST')]),
        'actim':    ('ac', 'Verb', [('ac', 'ROOT', 'open'), ('ti', 'PAST', 'PAST'), ('m', 'A1SG', 'I')]),
        
        # Postpositions / Particles
        'icin':     ('icin', 'Postp', [('icin', 'POSTP', 'for')]),
        'ile':      ('ile', 'Postp', [('ile', 'POSTP', 'with')]),
        've':       ('ve', 'Conj', [('ve', 'CONJ', 'and')]),
        'ama':      ('ama', 'Conj', [('ama', 'CONJ', 'but')]),
        'sonra':    ('sonra', 'Postp', [('sonra', 'POSTP', 'after')]),
        
        # Pronouns
        'ben':      ('ben', 'Pron', [('ben', 'ROOT', 'I')]),
        'sen':      ('sen', 'Pron', [('sen', 'ROOT', 'you')]),
        'o':        ('o', 'Pron', [('o', 'ROOT', 'he/she/it')]),
        'biz':      ('biz', 'Pron', [('biz', 'ROOT', 'we')]),
        'onlar':    ('onlar', 'Pron', [('on', 'ROOT', 'they'), ('lar', 'PL', 'plural')]),
        'bana':     ('ben', 'Pron', [('ben', 'ROOT', 'I'), ('a', 'DAT', 'to')]),
    }
    
    @classmethod
    def analyze(cls, word):
        """Return Zemberek-style morphological analysis for a Turkish word."""
        word_lower = word.lower().rstrip('.!,?')
        if word_lower in cls.LEXICON:
            stem, pos, morphemes = cls.LEXICON[word_lower]
            return {
                'surface': word_lower,
                'stem': stem,
                'pos': pos,
                'morphemes': morphemes,  # [(surface, tag, gloss), ...]
                'analysis': f"[{stem}:{pos}]" + ''.join(f"+[{m}:{t}]" for m, t, g in morphemes[1:]),
            }
        else:
            # Unknown word — return surface as-is
            return {
                'surface': word_lower,
                'stem': word_lower,
                'pos': 'Unknown',
                'morphemes': [(word_lower, 'ROOT', word_lower)],
                'analysis': f"[{word_lower}:Unknown]",
            }
    
    @classmethod
    def analyze_sentence(cls, sentence):
        """Analyze a full Turkish sentence, returning list of word analyses."""
        words = sentence.strip().split()
        return [cls.analyze(w) for w in words]


# ============================================================================
# 3. NST Builder from Morphological Parse
# ============================================================================

def build_nst_from_morphology(sentence, analyses, sentence_id=""):
    """
    Build a Nested Semantic Tree from Zemberek-style morphological analyses.
    
    Tree structure:
      SENTENCE (root)
        ├── VERB_PHRASE
        │   ├── VERB: [stem]
        │   │   ├── TENSE: [past/fut/prog]
        │   │   └── PERSON: [1sg/2sg/3sg]
        │   └── OBJECT (if ACC/DAT present)
        │       └── NOUN: [stem]
        └── SUBJECT (if present)
            └── NOUN: [stem]
        └── ADJUNCT (locative/temporal)
            └── NOUN: [stem]
    
    Each morpheme becomes a node. Height increases with morphological depth.
    """
    nst = NestedSemanticTree(name=sentence_id, language="Turkish")
    
    # Root
    nst.add_node("ROOT", "S", "SENTENCE", parent_id=None, height=10.0)
    
    node_idx = [0]  # mutable counter
    
    def next_id():
        node_idx[0] += 1
        return f"n{node_idx[0]}"
    
    verb = None
    subject = None
    object_noun = None
    adjuncts = []
    postpositions = []
    
    # Classify words by grammatical role
    for ana in analyses:
        pos = ana['pos']
        morphs = ana['morphemes']
        surface = ana['surface']
        
        if pos == 'Verb':
            verb = ana
        elif pos == 'Noun':
            # Check case marking for role
            tags = [t for _, t, _ in morphs]
            if 'ACC' in tags:
                object_noun = ana
            elif 'DAT' in tags or 'LOC' in tags or 'ABL' in tags:
                adjuncts.append(ana)
            elif 'GEN' in tags:
                pass  # Possessor — skip for now
            else:
                # Nominative — could be subject
                if subject is None:
                    subject = ana
                else:
                    adjuncts.append(ana)
        elif pos == 'Pron':
            # Check case marking
            tags = [t for _, t, _ in morphs]
            if 'DAT' in tags:
                adjuncts.append(ana)
            else:
                subject = ana if subject is None else None
        elif pos == 'Postp':
            postpositions.append(ana)
        elif pos == 'Conj':
            pass  # Conjunctions don't create nodes
        else:
            adjuncts.append(ana)
    
    # Build VERB_PHRASE subtree
    if verb:
        vp_id = next_id()
        nst.add_node(vp_id, "VP", "VERB_PHRASE", parent_id="ROOT", height=9.0)
        
        # Verb root
        v_id = next_id()
        v_morphs = verb['morphemes']
        v_root = v_morphs[0]
        nst.add_node(v_id, v_root[0], f"VERB:{verb['pos']}", parent_id=vp_id, 
                     height=8.0, morphemes=[v_root], gloss=v_root[2])
        
        # Tense node (second morpheme if exists)
        if len(v_morphs) > 1:
            t_morph = v_morphs[1]
            if t_morph[1] in ('PAST', 'FUT', 'PROG'):
                t_id = next_id()
                nst.add_node(t_id, t_morph[0], f"TENSE:{t_morph[1]}", 
                            parent_id=v_id, height=7.0, morphemes=[t_morph],
                            gloss=t_morph[2])
                
                # Person agreement (third morpheme)
                if len(v_morphs) > 2:
                    p_morph = v_morphs[2]
                    p_id = next_id()
                    nst.add_node(p_id, p_morph[0], f"AGR:{p_morph[1]}",
                                parent_id=t_id, height=6.0,
                                morphemes=[p_morph], gloss=p_morph[2])
        
        # Object subtree
        if object_noun:
            obj_id = next_id()
            obj_morphs = object_noun['morphemes']
            obj_root = obj_morphs[0]
            nst.add_node(obj_id, obj_root[0], f"OBJ:{object_noun['pos']}",
                        parent_id=vp_id, height=8.0,
                        morphemes=[obj_root], gloss=obj_root[2])
            # Case morpheme
            if len(obj_morphs) > 1:
                case_morph = obj_morphs[1]
                c_id = next_id()
                nst.add_node(c_id, case_morph[0], f"CASE:{case_morph[1]}",
                            parent_id=obj_id, height=7.0,
                            morphemes=[case_morph], gloss=case_morph[2])
    
    # Build SUBJECT subtree
    if subject:
        subj_id = next_id()
        subj_morphs = subject['morphemes']
        subj_root = subj_morphs[0]
        nst.add_node(subj_id, subj_root[0], f"SUBJ:{subject['pos']}",
                    parent_id="ROOT", height=9.0,
                    morphemes=[subj_root], gloss=subj_root[2])
        # Plural suffix
        for m in subj_morphs[1:]:
            if m[1] in ('PL', 'GEN'):
                pl_id = next_id()
                nst.add_node(pl_id, m[0], f"AGR:{m[1]}",
                            parent_id=subj_id, height=8.0,
                            morphemes=[m], gloss=m[2])
    
    # Build ADJUNCT subtrees
    for adj in adjuncts:
        adj_id = next_id()
        adj_morphs = adj['morphemes']
        adj_root = adj_morphs[0]
        adj_type = "LOC" if any(t in ('LOC',) for _, t, _ in adj_morphs) else \
                   "TEMP" if adj_root[2] in ('yesterday', 'today', 'tomorrow') else \
                   "ADJUNCT"
        nst.add_node(adj_id, adj_root[0], f"ADJ:{adj_type}",
                    parent_id="ROOT", height=9.0,
                    morphemes=[adj_root], gloss=adj_root[2])
        # Case morpheme
        for m in adj_morphs[1:]:
            if m[1] in ('LOC', 'DAT', 'ABL', 'ACC'):
                c_id = next_id()
                nst.add_node(c_id, m[0], f"CASE:{m[1]}",
                            parent_id=adj_id, height=8.0,
                            morphemes=[m], gloss=m[2])
    
    # Postpositions
    for pp in postpositions:
        pp_id = next_id()
        pp_morphs = pp['morphemes']
        nst.add_node(pp_id, pp_morphs[0][0], f"POSTP",
                    parent_id="ROOT", height=9.0,
                    morphemes=pp_morphs, gloss=pp_morphs[0][2])
    
    nst.preprocess_lca()
    return nst


# ============================================================================
# 4. Turkish Corpus (15 sentences covering varied propositions)
# ============================================================================

TURKISH_CORPUS = [
    # Proposition cluster A: Buying/purchasing
    ("D1", "Kadin dun ekmek aldi", "Woman yesterday bread bought", 
     "The woman bought bread yesterday"),
    ("D2", "Adam dukkandan ekmek aldi", "Man store-from bread bought",
     "The man bought bread from the store"),
    ("D3", "Kadin dun dukkanda ekmek aldi", "Woman yesterday store-at bread bought",
     "The woman bought bread at the store yesterday"),
    ("D4", "Ben ekmek aldim", "I bread bought-1SG",
     "I bought bread"),
    ("D5", "Adam para verdi", "Man money gave",
     "The man gave money"),
    
    # Proposition cluster B: Movement
    ("D6", "Kadin eve geldi", "Woman house-to came",
     "The woman came to the house"),
    ("D7", "Adam dukkana gitti", "Man store-to went",
     "The man went to the store"),
    ("D8", "Cocuklar eve geldi", "Children house-to came",
     "The children came to the house"),
    
    # Proposition cluster C: Perception/seeing
    ("D9", "Kadin adami gordu", "Woman man-ACC saw",
     "The woman saw the man"),
    ("D10", "Adam cocugu gordu", "Man child-ACC saw",
     "The man saw the child"),
    ("D11", "Ben kadini dukkanda gordum", "I woman-ACC store-at saw-1SG",
     "I saw the woman at the store"),
    
    # Proposition cluster D: Other actions
    ("D12", "Cocuk sut icti", "Child milk drank",
     "The child drank milk"),
    ("D13", "Kadin kitabi acti", "Woman book-ACC opened",
     "The woman opened the book"),
    ("D14", "Adam pencereyi acti", "Man window-ACC opened",
     "The man opened the window"),
    ("D15", "Kadin cocuga kitap verdi", "Woman child-DAT book gave",
     "The woman gave the book to the child"),
]

# Ground truth: for each query proposition, which documents are relevant?
# Query: "woman bought bread" → D1, D3, D4
# Query: "man bought bread" → D2
# Query: "X gave Y to Z" → D5, D15
# Query: "X came to Y" → D6, D8
# Query: "X went to Y" → D7
# Query: "X saw Y" → D9, D10, D11
# Query: "X opened Y" → D13, D14

GROUND_TRUTH = {
    "Q_buy_bread": {
        "query_text": "ekmek aldi",  # "bought bread"
        "relevant": ["D1", "D2", "D3", "D4"],
    },
    "Q_woman_buy": {
        "query_text": "kadin ekmek aldi",  # "woman bought bread"
        "relevant": ["D1", "D3"],
    },
    "Q_man_buy": {
        "query_text": "adam ekmek aldi",  # "man bought bread"
        "relevant": ["D2"],
    },
    "Q_give": {
        "query_text": "verdi",  # "gave"
        "relevant": ["D5", "D15"],
    },
    "Q_come": {
        "query_text": "geldi",  # "came"
        "relevant": ["D6", "D8"],
    },
    "Q_go": {
        "query_text": "gitti",  # "went"
        "relevant": ["D7"],
    },
    "Q_see": {
        "query_text": "gordu",  # "saw"
        "relevant": ["D9", "D10", "D11"],
    },
    "Q_open": {
        "query_text": "acti",  # "opened"
        "relevant": ["D13", "D14"],
    },
    "Q_woman_see_man": {
        "query_text": "kadin adam gordu",  # "woman saw man"
        "relevant": ["D9"],
    },
    "Q_store": {
        "query_text": "dukkan",  # "store"
        "relevant": ["D2", "D3", "D7", "D11"],
    },
}


# ============================================================================
# 5. Subtree Search (Type I + II matching)
# ============================================================================

def _node_matches(q_node, d_node):
    """Exact match on category."""
    return q_node.category == d_node.category


def _node_partial_matches(q_node, d_node):
    """Partial match: category OR label overlap."""
    if q_node.category == d_node.category:
        return True
    q_cat_parts = set(q_node.category.lower().replace(':', ' ').split())
    d_cat_parts = set(d_node.category.lower().replace(':', ' ').split())
    return bool(q_cat_parts & d_cat_parts)


def find_exact_matches(query_tree, doc_tree, min_nodes=1):
    """
    Type I: Find all exact subtree isomorphisms of query in document.
    Returns list of matching root nodes in doc_tree.
    """
    matches = []
    q_root = query_tree.root.id
    
    for d_nid in doc_tree.nodes:
        if _node_matches(query_tree.nodes[q_root], doc_tree.nodes[d_nid]):
            mapping = _subtree_match(query_tree, doc_tree, q_root, d_nid, {})
            if mapping and len(mapping) >= min_nodes:
                matches.append((d_nid, len(mapping)))
    
    # Sort by match size descending
    matches.sort(key=lambda x: -x[1])
    return matches


def _subtree_match(qt, dt, q_nid, d_nid, mapping):
    """Recursive subtree isomorphism check."""
    qn = qt.nodes[q_nid]
    dn = dt.nodes[d_nid]
    
    if not _node_matches(qn, dn):
        return None
    
    new_map = mapping.copy()
    new_map[q_nid] = d_nid
    
    if not qn.children:
        return new_map
    
    # Match each query child to a distinct doc child
    qc = qn.children
    dc = list(dn.children)
    
    if len(qc) > len(dc):
        return None
    
    # Try all permutations of qc → dc assignment
    from itertools import permutations
    for perm in permutations(range(len(dc)), len(qc)):
        success = True
        temp_map = new_map.copy()
        for i, dc_idx in enumerate(perm):
            result = _subtree_match(qt, dt, qc[i].id, dc[dc_idx].id, temp_map)
            if result is None:
                success = False
                break
            temp_map.update(result)
        if success:
            return temp_map
    
    return None


def search_corpus(query_text, corpus_trees, query_id=""):
    """
    Search corpus for a query text using morphological analysis + subtree matching.
    Returns ranked list of (doc_id, score, details).
    """
    # Analyze query morphologically
    query_analyses = ZemberekSimulator.analyze_sentence(query_text)
    query_tree = build_nst_from_morphology(query_text, query_analyses, f"Q_{query_id}")
    
    results = []
    for doc_id, doc_tree in corpus_trees.items():
        matches = find_exact_matches(query_tree, doc_tree, min_nodes=2)
        if matches:
            top_match = matches[0]
            # Score = fraction of query nodes matched
            q_node_count = len(query_tree.nodes)
            score = top_match[1] / q_node_count if q_node_count > 0 else 0
            results.append((doc_id, score, top_match[1], q_node_count))
    
    # Sort by score descending
    results.sort(key=lambda x: -x[1])
    return results


# ============================================================================
# 6. Evaluation Metrics
# ============================================================================

def precision_at_k(retrieved, relevant, k):
    """P@k: fraction of top-k results that are relevant."""
    if k <= 0:
        return 0.0
    top_k = retrieved[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / k


def recall_at_k(retrieved, relevant, k):
    """R@k: fraction of relevant documents found in top-k."""
    if not relevant:
        return 1.0
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / len(relevant)


def f1_at_k(retrieved, relevant, k):
    """F1@k: harmonic mean of P@k and R@k."""
    p = precision_at_k(retrieved, relevant, k)
    r = recall_at_k(retrieved, relevant, k)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def mean_reciprocal_rank(retrieved, relevant):
    """MRR: average of 1/rank of first relevant document."""
    for i, doc in enumerate(retrieved):
        if doc in relevant:
            return 1.0 / (i + 1)
    return 0.0


def evaluate_searches(corpus_trees, ground_truth):
    """
    Run all queries in ground_truth against corpus, compute evaluation metrics.
    Returns dict with per-query and aggregate metrics.
    """
    results = {}
    all_p5, all_r5, all_f5, all_mrr = [], [], [], []
    
    for qid, gt in sorted(ground_truth.items()):
        query_text = gt['query_text']
        relevant = set(gt['relevant'])
        
        search_results = search_corpus(query_text, corpus_trees, qid)
        retrieved = [doc_id for doc_id, score, n, total in search_results]
        
        p5 = precision_at_k(retrieved, relevant, 5)
        r5 = recall_at_k(retrieved, relevant, 5)
        f5 = f1_at_k(retrieved, relevant, 5)
        mrr = mean_reciprocal_rank(retrieved, relevant)
        
        all_p5.append(p5)
        all_r5.append(r5)
        all_f5.append(f5)
        all_mrr.append(mrr)
        
        results[qid] = {
            'query': query_text,
            'relevant': sorted(relevant),
            'retrieved': retrieved[:5],
            'P@5': p5,
            'R@5': r5,
            'F1@5': f5,
            'MRR': mrr,
        }
    
    # Aggregate
    n = len(all_p5)
    results['AGGREGATE'] = {
        'num_queries': n,
        'mean_P@5': sum(all_p5) / n if n else 0,
        'mean_R@5': sum(all_r5) / n if n else 0,
        'mean_F1@5': sum(all_f5) / n if n else 0,
        'mean_MRR': sum(all_mrr) / n if n else 0,
    }
    
    return results


# ============================================================================
# 7. Demo: End-to-End Pipeline
# ============================================================================

def demo():
    print("=" * 70)
    print("0.10.py — Turkish Morphological Pipeline")
    print("Zemberek Simulation → NST Builder → Search → Evaluation")
    print("=" * 70)
    
    # Step 1: Analyze all corpus sentences
    print("\n[1] Morphological Analysis (Zemberek Simulation)")
    print("-" * 50)
    corpus_analyses = {}
    for doc_id, sentence, gloss, english in TURKISH_CORPUS:
        analyses = ZemberekSimulator.analyze_sentence(sentence)
        corpus_analyses[doc_id] = (sentence, analyses, english)
        
        print(f"\n{doc_id}: {sentence}")
        print(f"   English: {english}")
        for ana in analyses:
            if ana['pos'] != 'Conj':
                print(f"   {ana['surface']:15s} → {ana['analysis']}")
    
    # Step 2: Build NSTs
    print("\n\n[2] NST Construction from Morphological Parse")
    print("-" * 50)
    corpus_trees = {}
    for doc_id, (sentence, analyses, english) in corpus_analyses.items():
        nst = build_nst_from_morphology(sentence, analyses, doc_id)
        corpus_trees[doc_id] = nst
        leaves, triples, violations = nst.verify_ultrametric()
        print(f"  {doc_id}: {len(nst.nodes)} nodes, {leaves} leaves, "
              f"{triples} triples, {violations} violations "
              f"[{'PASS' if violations == 0 else 'FAIL'}]")
    
    # Step 3: Run queries
    print("\n\n[3] Search Results")
    print("-" * 50)
    
    # Step 4: Evaluate
    print("\n\n[4] Evaluation Metrics")
    print("-" * 50)
    eval_results = evaluate_searches(corpus_trees, GROUND_TRUTH)
    
    # Print per-query results
    print(f"\n{'Query':<20s} {'P@5':>6s} {'R@5':>6s} {'F1@5':>6s} {'MRR':>6s}  Retrieved")
    print("-" * 80)
    for qid in sorted(GROUND_TRUTH.keys()):
        r = eval_results[qid]
        print(f"{qid:<20s} {r['P@5']:6.3f} {r['R@5']:6.3f} {r['F1@5']:6.3f} {r['MRR']:6.3f}  "
              f"{r['retrieved'][:3]}")
    
    # Print aggregate
    agg = eval_results['AGGREGATE']
    print("=" * 80)
    print(f"{'AGGREGATE':<20s} {agg['mean_P@5']:6.3f} {agg['mean_R@5']:6.3f} "
          f"{agg['mean_F1@5']:6.3f} {agg['mean_MRR']:6.3f}")
    print(f"\n  {agg['num_queries']} queries across 15 Turkish documents")
    
    # Step 5: Detailed query example
    print("\n\n[5] Detailed Example: 'kadin ekmek aldi' (woman bought bread)")
    print("-" * 50)
    example_results = search_corpus("kadin ekmek aldi", corpus_trees, "example")
    relevant_set = set(GROUND_TRUTH['Q_woman_buy']['relevant'])
    for rank, (doc_id, score, n_matched, n_total) in enumerate(example_results):
        marker = "[RELEVANT]" if doc_id in relevant_set else ""
        sentence = corpus_analyses[doc_id][0]
        english = corpus_analyses[doc_id][2]
        print(f"  #{rank+1}: {doc_id} ({english}) — score={score:.2f} "
              f"({n_matched}/{n_total} nodes) {marker}")
    
    # Step 6: Ultrametric verification summary
    print("\n\n[6] Ultrametric Property Verification")
    print("-" * 50)
    all_pass = True
    for doc_id, nst in corpus_trees.items():
        leaves, triples, violations = nst.verify_ultrametric()
        status = "PASS" if violations == 0 else "FAIL"
        if violations > 0:
            all_pass = False
        print(f"  {doc_id}: {triples} triples, {violations} violations — {status}")
    print(f"\n  ALL PASS: {all_pass}")
    
    return eval_results, corpus_trees


if __name__ == "__main__":
    eval_results, corpus_trees = demo()
    print("\nDone.")
