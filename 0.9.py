#!/usr/bin/env python3
"""
0.9.py — Enhanced Corpus: 12 documents, 5 languages

Expands the NSG pipeline test corpus beyond the original 5 documents.
Adds Finnish (agglutinative) and Inuktitut (polysynthetic) to the
existing English/Turkish/Mohawk language set.

Languages:
  Isolating:    English
  Agglutinative: Turkish, Finnish
  Polysynthetic: Mohawk, Inuktitut
"""

import sys
from itertools import combinations


# === Minimal NST class (for standalone execution) ===

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
        violations, total = 0, 0
        for x, y, z in combinations(leaves, 3):
            total += 1
            if self.ultrametric_distance(x, z) > max(
                self.ultrametric_distance(x, y),
                self.ultrametric_distance(y, z)) + 1e-10:
                violations += 1
        return total, violations


# === Matching (Type I/II) ===

def _sub_match(qn, dn):
    return qn.category == dn.category and qn.label == dn.label

def _find_matches(qt, dt, q_root, d_root, mapped, depth=0):
    qn = qt.nodes[q_root]; dn = dt.nodes[d_root]
    if not _sub_match(qn, dn): return []
    if not qn.children: return [{**mapped, q_root: d_root}]
    if len(qn.children) > len(dn.children): return []
    results = []; qc = qn.children; dc = dn.children
    def assign(q_idx, assigned, cm):
        if q_idx == len(qc): results.append(cm.copy()); return
        for d_child in dc:
            if d_child.id in assigned: continue
            for m in _find_matches(qt, dt, qc[q_idx].id, d_child.id, cm, depth+1):
                nm = cm.copy(); nm.update(m)
                assign(q_idx+1, assigned|{d_child.id}, nm)
    assign(0, set(), {q_root: d_root})
    return results


# === Tree Edit Distance (Type III) ===

def tree_edit_distance(ta, tb, root_a, root_b):
    def postorder(tree, rid):
        res = []
        def dfs(nid):
            for c in tree.nodes[nid].children: dfs(c.id)
            res.append(nid)
        dfs(rid); return res
    po_a = postorder(ta, root_a); po_b = postorder(tb, root_b)
    def leftmost(tree, rid):
        lm = {}
        def dfs(nid):
            node = tree.nodes[nid]
            if not node.children: lm[nid] = nid
            else: lm[nid] = dfs(node.children[0].id)
            for c in node.children[1:]: dfs(c.id)
            return lm[nid]
        dfs(rid); return lm
    lm_a = leftmost(ta, root_a); lm_b = leftmost(tb, root_b)
    ia = {n: i for i, n in enumerate(po_a)}; ib = {n: i for i, n in enumerate(po_b)}
    na, nb = len(po_a), len(po_b)
    td = [[0]*nb for _ in range(na)]
    fd = [[0]*(nb+1) for _ in range(na+1)]
    for i in range(na):
        for j in range(nb):
            nia, nib = po_a[i], po_b[j]
            lma = lm_a.get(nia, nia); lmb = lm_b.get(nib, nib)
            li, lj = ia.get(lma, i), ib.get(lmb, j)
            for di in range(li, i+2):
                for dj in range(lj, j+2): fd[di][dj] = 0
            fd[li][lj] = 0
            for di in range(li, i+1): fd[di+1][lj] = fd[di][lj] + 3
            for dj in range(lj, j+1): fd[li][dj+1] = fd[li][dj] + 3
            for di in range(li, i+1):
                for dj in range(lj, j+1):
                    nda, ndb = po_a[di], po_b[dj]
                    lda = lm_a.get(nda, nda); ldb = lm_b.get(ndb, ndb)
                    ldi, ldj = ia.get(lda, di), ib.get(ldb, dj)
                    if ldi == li and ldj == lj:
                        an, bn = ta.nodes[nda], tb.nodes[ndb]
                        rc = 0 if an.label == bn.label else (1 if an.category == bn.category else 2)
                        fd[di+1][dj+1] = min(fd[di][dj+1]+3, fd[di+1][dj]+3, fd[di][dj]+td[di][dj]+rc)
                    else:
                        fd[di+1][dj+1] = min(fd[di][dj+1]+3, fd[di+1][dj]+3, fd[ldi][ldj]+td[di][dj])
            td[i][j] = fd[i+1][j+1]
    return td[na-1][nb-1]


def match_pipeline(query, doc):
    q_root = query.root.id if query.root else None
    if not q_root: return ('NONE', 0.0, float('inf'), 0.0)
    best_cov, best_dist, best_type = 0.0, float('inf'), None
    qn = query.nodes[q_root]
    for dnid, dn in doc.nodes.items():
        if dn.category != qn.category: continue
        for m in _find_matches(query, doc, q_root, dnid, {}, 0):
            cov = len(m)/len(query.nodes)
            mdh = max(abs(query.nodes[q].height - doc.nodes[d].height) for q, d in m.items())
            if cov == 1.0 and mdh < 1e-10:
                if best_type != 'I': best_cov, best_dist, best_type = cov, mdh, 'I'
            elif cov > best_cov or (cov == best_cov and mdh < best_dist):
                best_cov, best_dist, best_type = cov, mdh, 'II'
    if best_type:
        H = max(n.height for n in doc.nodes.values()) or 1.0
        return (best_type, best_cov, best_dist, best_cov/(1.0+best_dist/max(H,1.0)))
    best_ed, best_root = float('inf'), None
    for dnid in doc.nodes:
        ed = tree_edit_distance(query, doc, q_root, dnid)
        if ed < best_ed: best_ed, best_root = ed, dnid
    if best_root:
        max_cost = 4*len(query.nodes) or 1
        return ('III', 0.0, best_ed, max(0.0, 1.0-best_ed/max_cost))
    return ('NONE', 0.0, float('inf'), 0.0)


# === BUILDERS ===

def build_query_tree(language="English"):
    """Standard 'dog bit man yesterday' query in any language."""
    tree = NestedSemanticTree(f"{language} query", language)
    tree.add_node("b", "BITE", "ACTION", None, 4.0)
    tree.add_node("d", "dog", "ENTITY", "b", 0.0)
    tree.add_node("m", "man", "ENTITY", "b", 0.0)
    tree.add_node("p", "PAST", "TENSE", "b", 2.0)
    tree.add_node("y", "YESTERDAY", "LOCATIVE", "p", 0.0)
    tree.preprocess_lca()
    return tree


def build_expanded_corpus():
    """12 documents in 5 languages with varied event structures."""
    c = []
    def d(name, lang, nodes_spec):
        """Build a document from spec: [(id, label, cat, parent, height), ...]"""
        t = NestedSemanticTree(name, lang)
        for nid, label, cat, pid, h in nodes_spec:
            t.add_node(nid, label, cat, pid, h)
        t.preprocess_lca()
        c.append(t)

    # --- English documents (isolating) ---
    d("EN-1: Dog bit man yesterday [exact]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0),
        ("m","man","ENTITY","b",0), ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("EN-2: Dog chased cat yesterday [diff action]", "English", [
        ("c","CHASE","ACTION",None,4), ("d","dog","ENTITY","c",0),
        ("ct","cat","ENTITY","c",0), ("p","PAST","TENSE","c",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("EN-3: Man bit dog [reversed]", "English", [
        ("b","BITE","ACTION",None,4), ("m","man","ENTITY","b",0), ("dg","dog","ENTITY","b",0)])

    d("EN-4: Cat eats fish now [different]", "English", [
        ("e","EAT","ACTION",None,4), ("c","cat","ENTITY","e",0),
        ("f","fish","ENTITY","e",0), ("n","PRESENT","TENSE","e",2)])

    d("EN-5: Dog bit man in park yesterday [extended]", "English", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0), ("pk","park","LOCATIVE","b",0)])

    d("EN-6: Dog bit man with stick [instrument]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("s","stick","ENTITY","b",0)])

    # --- Turkish documents (agglutinative) ---
    d("TR-1: Kopek adami isirdi [exact, no 'yesterday']", "Turkish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    d("TR-2: Kopek adami parkta isirdi [extended]", "Turkish", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("pk","park","LOCATIVE","b",0)])

    # --- Mohawk document (polysynthetic) ---
    d("MH-1: Wahonwa'kahra'ko' [bite event, fused]", "Mohawk", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    # --- Finnish documents (agglutinative) ---
    d("FI-1: Koira puri miesta eilen [exact]", "Finnish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)])

    d("FI-2: Koira juoksi [dog ran, minimal]", "Finnish", [
        ("r","RUN","ACTION",None,4), ("d","dog","ENTITY","r",0), ("p","PAST","TENSE","r",2)])

    # --- Inuktitut documents (polysynthetic) ---
    d("IK-1: Qimmiq angutimik kiisijuq [exact]", "Inuktitut", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)])

    return c


# === MAIN ===

def main():
    print("=" * 72)
    print("  ENHANCED CORPUS — 12 Documents, 5 Languages")
    print("  Nested Semantic Graph Pipeline Demo")
    print("=" * 72)

    corpus = build_expanded_corpus()
    queries = {
        "English":   build_query_tree("English"),
        "Turkish":   build_query_tree("Turkish"),
        "Mohawk":    build_query_tree("Mohawk"),
        "Finnish":   build_query_tree("Finnish"),
        "Inuktitut": build_query_tree("Inuktitut"),
    }

    # Verify all trees are ultrametric
    print("\n[STEP 1] Ultrametric verification:")
    all_ok = True
    for t in corpus + list(queries.values()):
        n, v = t.verify_ultrametric()
        ok = v == 0
        all_ok &= ok
        print(f"  {'PASS' if ok else 'FAIL'} [{t.language[:2]:>2}] {t.name[:50]} ({n} triples)")
    print(f"  ===> {'ALL PASS' if all_ok else 'SOME FAILED'}")

    # Corpus stats
    langs = {}; nodes_total = 0
    for t in corpus:
        langs[t.language] = langs.get(t.language, 0) + 1
        nodes_total += len(t.nodes)
    print(f"\n[STEP 2] Corpus stats: {len(corpus)} docs, {nodes_total} nodes")
    for lang, count in sorted(langs.items()):
        print(f"  {lang}: {count} documents")

    # Cross-linguistic search
    print(f"\n[STEP 3] Cross-linguistic search ({len(queries)} query languages):")
    print(f"  {'Query':<12} {'Top Rank':<10} {'Type':<6} {'Score':<8} {'Document'}")
    print(f"  {'-'*12} {'-'*10} {'-'*6} {'-'*8} {'-'*50}")

    for lang, query in queries.items():
        results = []
        for i, doc in enumerate(corpus):
            mtype, cov, dist_ed, score = match_pipeline(query, doc)
            if mtype != 'NONE':
                results.append((i, doc.name, mtype, cov, dist_ed, score))
        results.sort(key=lambda r: (-r[5], r[4]))
        if results:
            top = results[0]
            print(f"  {lang:<12} {top[0]:<10} {top[2]:<6} {top[5]:<8.4f} {top[1][:50]}")
        else:
            print(f"  {lang:<12} {'none':<10} {'--':<6} {'--':<8} (no matches)")

    # Pipeline distribution across full corpus
    dist = {'I': 0, 'II': 0, 'III': 0, 'NONE': 0}
    for doc in corpus:
        mtype, _, _, _ = match_pipeline(queries["English"], doc)
        dist[mtype] += 1
    print(f"\n[STEP 4] Pipeline distribution (English query): {dist}")

    print(f"\n  >> ENHANCED CORPUS PIPELINE COMPLETE <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
