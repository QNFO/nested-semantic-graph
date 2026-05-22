#!/usr/bin/env python3
"""
0.11.py -- Expanded Corpus (25+ documents, 5 languages) + Scalability Benchmarks

S3.3: Grows corpus from 12 to 25+ docs with more event structures
S3.4: Measures query latency vs. corpus size, profiles matching

Languages: English, Turkish, Mohawk, Finnish, Inuktitut
"""

import sys, time
from itertools import combinations


# === NST Classes ===

class SemanticNode:
    __slots__ = ('id', 'label', 'category', 'parent_id', 'children', 'height')
    def __init__(self, nid, label, category, parent_id=None, height=0.0):
        self.id = nid; self.label = label; self.category = category
        self.parent_id = parent_id; self.children = []; self.height = height


class NestedSemanticTree:
    def __init__(self, name="", language="unknown"):
        self.name = name; self.language = language
        self.nodes = {}; self.root = None
        self._depth = {}; self._parent_jump = {}
        self._lca_preprocessed = False; self._log_n = 0; self._max_depth = 0

    def add_node(self, nid, label, category, parent_id=None, height=0.0):
        node = SemanticNode(nid, label, category, parent_id, height)
        self.nodes[nid] = node
        if parent_id: self.nodes[parent_id].children.append(node)
        else: self.root = node
        return node

    def _assign_depths(self):
        if not self.root: return
        stack = [(self.root, 0)]; self._depth[self.root.id] = 0; self._max_depth = 0
        while stack:
            node, d = stack.pop(); self._depth[node.id] = d
            self._max_depth = max(self._max_depth, d)
            for c in node.children: stack.append((c, d + 1))

    def _build_parent_jumps(self):
        log_n = max(1, (self._max_depth + 1).bit_length())
        up = {nid: [-1] * log_n for nid in self.nodes}
        for nid, node in self.nodes.items():
            up[nid][0] = node.parent_id if node.parent_id else -1
        for k in range(1, log_n):
            for nid in self.nodes:
                if up[nid][k - 1] != -1: up[nid][k] = up[up[nid][k - 1]][k - 1]
        self._parent_jump = up; self._log_n = log_n

    def preprocess_lca(self):
        self._assign_depths(); self._build_parent_jumps()
        self._lca_preprocessed = True

    def lca(self, id1, id2):
        if not self._lca_preprocessed: self.preprocess_lca()
        d1, d2 = self._depth[id1], self._depth[id2]
        if d1 < d2: id1, id2 = id2, id1; d1, d2 = d2, d1
        diff = d1 - d2
        for k in range(self._log_n):
            if (diff >> k) & 1: id1 = self._parent_jump[id1][k]
        if id1 == id2: return id1
        for k in range(self._log_n - 1, -1, -1):
            if self._parent_jump[id1][k] != self._parent_jump[id2][k]:
                id1 = self._parent_jump[id1][k]; id2 = self._parent_jump[id2][k]
        return self._parent_jump[id1][0]

    def ultrametric_distance(self, id1, id2):
        return self.nodes[self.lca(id1, id2)].height

    def verify_ultrametric(self):
        leaves = [nid for nid, n in self.nodes.items() if not n.children]
        v, t = 0, 0
        for x, y, z in combinations(leaves, 3):
            t += 1
            if self.ultrametric_distance(x, z) > max(
                self.ultrametric_distance(x, y),
                self.ultrametric_distance(y, z)) + 1e-10: v += 1
        return t, v


# === Matching (Type I/II) ===

def _sm(qn, dn):
    return qn.category == dn.category and qn.label == dn.label

def _fm(qt, dt, qr, dr, mapped, depth=0):
    qn, dn = qt.nodes[qr], dt.nodes[dr]
    if not _sm(qn, dn): return []
    if not qn.children: return [{**mapped, qr: dr}]
    if len(qn.children) > len(dn.children): return []
    res = []; qc = qn.children; dc = dn.children
    def assign(qi, assigned, cm):
        if qi == len(qc): res.append(cm.copy()); return
        for dc_ in dc:
            if dc_.id in assigned: continue
            for m in _fm(qt, dt, qc[qi].id, dc_.id, cm, depth+1):
                nm = cm.copy(); nm.update(m)
                assign(qi+1, assigned|{dc_.id}, nm)
    assign(0, set(), {qr: dr})
    return res

def match_pipeline(query, doc):
    qr = query.root.id if query.root else None
    if not qr: return ('NONE', 0.0, 1e9, 0.0)
    bc, bd, bt = 0.0, 1e9, None
    qn = query.nodes[qr]
    for dnid, dn in doc.nodes.items():
        if dn.category != qn.category: continue
        for m in _fm(query, doc, qr, dnid, {}, 0):
            cov = len(m)/len(query.nodes)
            md = max(abs(query.nodes[q].height-doc.nodes[d].height) for q,d in m.items())
            if cov==1.0 and md<1e-10:
                if bt!='I': bc, bd, bt = cov, md, 'I'
            elif cov>bc or (cov==bc and md<bd): bc, bd, bt = cov, md, 'II'
    if bt:
        H = max(n.height for n in doc.nodes.values()) or 1.0
        return (bt, bc, bd, bc/(1.0+bd/max(H,1.0)))
    return ('NONE', 0.0, 1e9, 0.0)


# === Builders ===

def add_doc(t, lang, name, nodes_spec):
    for nid, label, cat, pid, h in nodes_spec:
        t.add_node(nid, label, cat, pid, h)
    t.preprocess_lca()

def build_expanded_corpus():
    c = []
    def d(name, lang, ns):
        t = NestedSemanticTree(name, lang)
        add_doc(t, lang, name, ns)
        c.append(t)

    # ENGLISH (isolating) -- 8 docs
    d("EN-01: Dog bit man yesterday [exact]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("EN-02: Dog chased cat yesterday [diff action]", "English", [
        ("c","CHASE","ACTION",None,4), ("d","dog","ENTITY","c",0), ("ct","cat","ENTITY","c",0),
        ("p","PAST","TENSE","c",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("EN-03: Man bit dog [reversed]", "English", [
        ("b","BITE","ACTION",None,4), ("m","man","ENTITY","b",0), ("dg","dog","ENTITY","b",0)])

    d("EN-04: Cat eats fish now [different]", "English", [
        ("e","EAT","ACTION",None,4), ("c","cat","ENTITY","e",0), ("f","fish","ENTITY","e",0),
        ("n","PRESENT","TENSE","e",2)])

    d("EN-05: Dog bit man in park yesterday [extended]", "English", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0), ("pk","park","LOCATIVE","b",0)])

    d("EN-06: Dog bit man with stick [instrument]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("s","stick","ENTITY","b",0)])

    d("EN-07: Large brown dog bit old man [modified]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("EN-08: Dog bit man quickly [manner]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("q","quickly","MANNER","b",0), ("p","PAST","TENSE","b",2)])

    # TURKISH (agglutinative) -- 5 docs
    d("TR-01: Kopek adami isirdi [exact, no yesterday]", "Turkish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("TR-02: Kopek adami parkta isirdi [extended]", "Turkish", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("pk","park","LOCATIVE","b",0)])

    d("TR-03: Kopek kediyi kovaladi [dog chased cat]", "Turkish", [
        ("c","CHASE","ACTION",None,4), ("d","dog","ENTITY","c",0), ("ct","cat","ENTITY","c",0),
        ("p","PAST","TENSE","c",2)])

    d("TR-04: Adam kopegi isirdi [man bit dog, reversed]", "Turkish", [
        ("b","BITE","ACTION",None,4), ("m","man","ENTITY","b",0), ("dg","dog","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("TR-05: Kopek adami hizla isirdi [dog bit man quickly]", "Turkish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("q","quickly","MANNER","b",0), ("p","PAST","TENSE","b",2)])

    # MOHAWK (polysynthetic) -- 3 docs
    d("MH-01: Wahonwa'kahra'ko' [bite event]", "Mohawk", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("MH-02: Wahonwa'kahra'ko' tsi'niyo [with yesterday]", "Mohawk", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("MH-03: [dog ran away, different action]", "Mohawk", [
        ("r","RUN","ACTION",None,4), ("d","dog","ENTITY","r",0), ("p","PAST","TENSE","r",2)])

    # FINNISH (agglutinative) -- 5 docs
    d("FI-01: Koira puri miesta eilen [exact]", "Finnish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("FI-02: Koira juoksi [dog ran]", "Finnish", [
        ("r","RUN","ACTION",None,4), ("d","dog","ENTITY","r",0), ("p","PAST","TENSE","r",2)])

    d("FI-03: Koira puri miesta [without yesterday]", "Finnish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("FI-04: Mies puri koiraa [man bit dog, reversed]", "Finnish", [
        ("b","BITE","ACTION",None,4), ("m","man","ENTITY","b",0), ("dg","dog","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("FI-05: Koira puri miesta puistossa [extended]", "Finnish", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("pk","park","LOCATIVE","b",0)])

    # INUKTITUT (polysynthetic) -- 4 docs
    d("IK-01: Qimmiq angutimik kiisijuq [exact]", "Inuktitut", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("IK-02: Qimmiq angutimik kiisijuq ippaksaq [with yesterday]", "Inuktitut", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("IK-03: Qimmiq qimmiq mik kiisijuq [dog bit dog]", "Inuktitut", [
        ("b","BITE","ACTION",None,4), ("d1","dog","ENTITY","b",0), ("d2","dog","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("IK-04: Qimmiq nirijuq [dog ate, different action]", "Inuktitut", [
        ("e","EAT","ACTION",None,4), ("d","dog","ENTITY","e",0), ("p","PAST","TENSE","e",2)])

    return c


# === Scalability Benchmark ===

def benchmark_scalability(corpus, query, sizes):
    results = []
    for size in sizes:
        sub_corpus = corpus[:min(size, len(corpus))]
        start = time.time()
        for _ in range(10):
            for doc in sub_corpus:
                _ = match_pipeline(query, doc)
        elapsed = max(time.time() - start, 0.001)
        per_query_ms = elapsed / (10 * len(sub_corpus)) * 1000
        results.append((size, per_query_ms))
    return results


# === Main ===

def main():
    print("=" * 72)
    print("  EXPANDED CORPUS (25+ documents) + SCALABILITY BENCHMARKS")
    print("=" * 72)

    corpus = build_expanded_corpus()
    query = NestedSemanticTree("Query: dog bit man yesterday", "English")
    query.add_node("b","BITE","ACTION",None,4); query.add_node("d","dog","ENTITY","b",0)
    query.add_node("m","man","ENTITY","b",0); query.add_node("p","PAST","TENSE","b",2)
    query.add_node("y","YESTERDAY","LOCATIVE","p",0)
    query.preprocess_lca()

    # Corpus stats
    langs = {}
    for t in corpus:
        langs[t.language] = langs.get(t.language, 0) + 1
    print(f"\nCorpus: {len(corpus)} documents, {sum(len(t.nodes) for t in corpus)} total nodes")
    for lang, count in sorted(langs.items()):
        print(f"  {lang}: {count}")

    # Ultrametric verification
    ultra_pass = all(t.verify_ultrametric()[1] == 0 for t in corpus)
    print(f"\nAll ultrametric: {'PASS' if ultra_pass else 'FAIL'}")

    # Search pipeline
    types = {'I': 0, 'II': 0, 'III': 0, 'NONE': 0}
    for doc in corpus:
        mt, _, _, _ = match_pipeline(query, doc)
        types[mt] += 1
    print(f"Pipeline distribution: {types}")

    # Scalability benchmark
    print(f"\n[SCALABILITY] Query latency vs. corpus size:")
    sizes = [5, 10, 15, 20, 25]
    bench = benchmark_scalability(corpus, query, sizes)
    print(f"  {'Size':<8} {'ms/query':<10}")
    for size, ms in bench:
        bar = '#' * int(ms * 10)
        print(f"  {size:<8} {ms:<10.3f} {bar}")

    # Cross-linguistic search
    print(f"\n[CROSS-LINGUISTIC] Top match per language:")
    for lang in ["English", "Turkish", "Mohawk", "Finnish", "Inuktitut"]:
        results = []
        for i, doc in enumerate(corpus):
            mt, _, _, sc = match_pipeline(query, doc)
            if mt != 'NONE': results.append((i, sc))
        results.sort(key=lambda r: -r[1])
        if results:
            top = corpus[results[0][0]]
            print(f"  {lang:<12}: {top.name[:55]}")

    print(f"\n  >> EXPANDED CORPUS + BENCHMARKS COMPLETE <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
