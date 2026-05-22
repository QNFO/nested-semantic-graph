#!/usr/bin/env python3
"""
nst_core.py -- Shared Nested Semantic Tree Library

Provides the canonical implementation of:
  - SemanticNode: conceptual primitive
  - NestedSemanticTree: rooted ultrametric tree with LCA and distance
  - Subtree isomorphism matching (Type I/II)
  - Tree edit distance (Type III, Zhang-Shasha)
  - Full match_pipeline: Type I -> II -> III fallback

All other project scripts (0.5.py, 0.8-0.11.py) can import from here
to eliminate code duplication.

Grounded in:
  - 0.2.md (Formal Definitions)
  - 0.3.md (Search Specification)
  - Tree Distance Cophenetic (DOI: 10.5281/zenodo.20213043)
"""

from itertools import combinations


# ============================================================================
# 1. NODE AND TREE
# ============================================================================

class SemanticNode:
    """A conceptual primitive -- an atomic unit of meaning."""
    __slots__ = ('id', 'label', 'category', 'parent_id', 'children', 'height')

    def __init__(self, nid, label, category, parent_id=None, height=0.0):
        self.id = nid
        self.label = label            # concept label (language-neutral ID)
        self.category = category       # ENTITY, ACTION, TENSE, etc.
        self.parent_id = parent_id     # None for root
        self.children = []             # list of SemanticNode
        self.height = height           # 0 for leaves, max for root


class NestedSemanticTree:
    """
    Rooted tree where nodes are conceptual primitives and edges encode scope.
    Distance d(x,y) = h(LCA(x,y)) satisfies the ultrametric inequality.
    """

    def __init__(self, name="Unnamed", language="unknown"):
        self.name = name
        self.language = language
        self.nodes = {}            # id -> SemanticNode
        self.root = None
        # LCA preprocessing state
        self._depth = {}           # id -> depth from root
        self._parent_jump = {}     # id -> [2^k ancestors]
        self._lca_preprocessed = False
        self._log_n = 0
        self._max_depth = 0

    # --- Tree Construction ---

    def add_node(self, nid, label, category, parent_id=None, height=0.0):
        """Add a node. If parent_id given, attach as child."""
        node = SemanticNode(nid, label, category, parent_id, height)
        self.nodes[nid] = node
        if parent_id is not None:
            self.nodes[parent_id].children.append(node)
        else:
            self.root = node
        return node

    # --- LCA Preprocessing ---

    def _assign_depths(self):
        if self.root is None:
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
            up[nid][0] = node.parent_id if node.parent_id is not None else -1
        for k in range(1, log_n):
            for nid in self.nodes:
                if up[nid][k - 1] != -1:
                    up[nid][k] = up[up[nid][k - 1]][k - 1]
        self._parent_jump = up
        self._log_n = log_n

    def preprocess_lca(self):
        """Precompute depth and binary lifting table for O(log n) LCA."""
        self._assign_depths()
        self._build_parent_jumps()
        self._lca_preprocessed = True

    def lca(self, id1, id2):
        """O(log n) lowest common ancestor via binary lifting."""
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
        """d(x,y) = h(LCA(x,y)) -- the cophenetic distance."""
        return self.nodes[self.lca(id1, id2)].height

    # --- Queries ---

    def get_leaf_ids(self):
        return [nid for nid, n in self.nodes.items() if not n.children]

    def get_node_ids(self):
        return list(self.nodes.keys())

    # --- Verification ---

    def verify_ultrametric(self):
        """Check d(x,z) <= max(d(x,y), d(y,z)) for all leaf triples."""
        leaves = self.get_leaf_ids()
        violations, total = 0, 0
        for x, y, z in combinations(leaves, 3):
            total += 1
            if self.ultrametric_distance(x, z) > max(
                self.ultrametric_distance(x, y),
                self.ultrametric_distance(y, z)) + 1e-10:
                violations += 1
        return total, violations

    # --- Display ---

    def print_tree(self, node_id=None, indent=0):
        if node_id is None and self.root is not None:
            node_id = self.root.id
        if node_id is None:
            return
        node = self.nodes[node_id]
        print(f"{'  ' * indent}{node.label} ({node.category}, h={node.height:.1f})")
        for child in node.children:
            self.print_tree(child.id, indent + 1)


# ============================================================================
# 2. SUBTREE ISOMORPHISM MATCHING (Type I / Type II)
# ============================================================================

def subtree_matches_node(query_node, doc_node, check_label=True):
    """Check if query_node matches doc_node (category match, optional label)."""
    if query_node.category != doc_node.category:
        return False
    if check_label and query_node.label != doc_node.label:
        return False
    return True


def _find_subtree_matches(query_tree, doc_tree, q_root, d_root, mapped, check_label=True, depth=0):
    """Recursively find all subtree isomorphisms rooted at given nodes."""
    qn = query_tree.nodes[q_root]
    dn = doc_tree.nodes[d_root]

    if not subtree_matches_node(qn, dn, check_label):
        return []

    if not qn.children:
        return [{**mapped, q_root: d_root}]

    if len(qn.children) > len(dn.children):
        return []

    results = []
    qc = qn.children
    dc = dn.children

    def assign(q_idx, assigned_ids, current_map):
        if q_idx == len(qc):
            results.append(current_map.copy())
            return
        q_child = qc[q_idx]
        for d_child in dc:
            if d_child.id in assigned_ids:
                continue
            sub = _find_subtree_matches(
                query_tree, doc_tree, q_child.id, d_child.id,
                current_map, check_label, depth + 1
            )
            for m in sub:
                nm = current_map.copy()
                nm.update(m)
                assign(q_idx + 1, assigned_ids | {d_child.id}, nm)

    assign(0, set(), {q_root: d_root})
    return results


def find_best_match(query_tree, doc_tree, query_root_id=None, check_label=True):
    """
    Find the best Type I/II match of query_tree within doc_tree.
    Returns: (match_type, mapping_dict, coverage, distance)
    """
    if query_root_id is None and query_tree.root is not None:
        query_root_id = query_tree.root.id
    if query_root_id is None:
        return (None, {}, 0.0, float('inf'))

    best_cov = 0.0
    best_dist = float('inf')
    best_type = None
    best_map = {}

    q_root_node = query_tree.nodes[query_root_id]
    for doc_nid, doc_node in doc_tree.nodes.items():
        if doc_node.category != q_root_node.category:
            continue
        mappings = _find_subtree_matches(
            query_tree, doc_tree, query_root_id, doc_nid, {}, check_label, 0
        )
        for m in mappings:
            cov = len(m) / len(query_tree.nodes)
            mdh = max(
                abs(query_tree.nodes[q].height - doc_tree.nodes[d].height)
                for q, d in m.items()
            )
            if cov == 1.0 and mdh < 1e-10:
                best_cov = cov
                best_dist = mdh
                best_type = 'I'
                best_map = m
            elif cov > best_cov or (cov == best_cov and mdh < best_dist):
                best_cov = cov
                best_dist = mdh
                best_type = 'II'
                best_map = m

    return (best_type, best_map, best_cov, best_dist)


# ============================================================================
# 3. TREE EDIT DISTANCE (Type III, Zhang-Shasha)
# ============================================================================

def tree_edit_distance(tree_a, tree_b, root_a=None, root_b=None):
    """
    Zhang-Shasha ordered tree edit distance.
    Edit costs: relabel=1 or 2, delete=3, insert=3.
    """
    if root_a is None and tree_a.root is not None:
        root_a = tree_a.root.id
    if root_b is None and tree_b.root is not None:
        root_b = tree_b.root.id
    if root_a is None or root_b is None:
        return float('inf')

    # Postorder traversal
    def postorder(tree, rid):
        res = []
        def dfs(nid):
            for c in tree.nodes[nid].children:
                dfs(c.id)
            res.append(nid)
        dfs(rid)
        return res

    po_a = postorder(tree_a, root_a)
    po_b = postorder(tree_b, root_b)

    # Leftmost leaf for each node
    def leftmost(tree, rid):
        lm = {}
        def dfs(nid):
            node = tree.nodes[nid]
            lm[nid] = nid if not node.children else dfs(node.children[0].id)
            for c in node.children[1:]:
                dfs(c.id)
            return lm[nid]
        dfs(rid)
        return lm

    lm_a = leftmost(tree_a, root_a)
    lm_b = leftmost(tree_b, root_b)

    # Postorder index
    ia = {n: i for i, n in enumerate(po_a)}
    ib = {n: i for i, n in enumerate(po_b)}
    na, nb = len(po_a), len(po_b)

    # relabel cost
    def rc(nid_a, nid_b):
        a = tree_a.nodes[nid_a]
        b = tree_b.nodes[nid_b]
        if a.label == b.label:
            return 0
        if a.category == b.category:
            return 1
        return 2

    td = [[0] * nb for _ in range(na)]
    fd = [[0] * (nb + 1) for _ in range(na + 1)]

    for i in range(na):
        for j in range(nb):
            nia, nib = po_a[i], po_b[j]
            lma = lm_a.get(nia, nia)
            lmb = lm_b.get(nib, nib)
            li, lj = ia.get(lma, i), ib.get(lmb, j)

            # Reset forest distance submatrix
            for di in range(li, i + 2):
                for dj in range(lj, j + 2):
                    fd[di][dj] = 0
            fd[li][lj] = 0
            for di in range(li, i + 1):
                fd[di + 1][lj] = fd[di][lj] + 3  # delete
            for dj in range(lj, j + 1):
                fd[li][dj + 1] = fd[li][dj] + 3  # insert

            for di in range(li, i + 1):
                for dj in range(lj, j + 1):
                    nda, ndb = po_a[di], po_b[dj]
                    lda = lm_a.get(nda, nda)
                    ldb = lm_b.get(ndb, ndb)
                    ldi, lj2 = ia.get(lda, di), ib.get(ldb, dj)

                    if ldi == li and lj2 == lj:
                        # Both are trees
                        fd[di + 1][dj + 1] = min(
                            fd[di][dj + 1] + 3,
                            fd[di + 1][dj] + 3,
                            fd[di][dj] + td[di][dj] + rc(nda, ndb),
                        )
                    else:
                        fd[di + 1][dj + 1] = min(
                            fd[di][dj + 1] + 3,
                            fd[di + 1][dj] + 3,
                            fd[ldi][lj2] + td[di][dj],
                        )
            td[i][j] = fd[i + 1][j + 1]

    return td[na - 1][nb - 1]


def type_iii_match(query_tree, doc_tree, query_root_id=None):
    """Find best Type III match via tree edit distance."""
    if query_root_id is None and query_tree.root is not None:
        query_root_id = query_tree.root.id
    if query_root_id is None:
        return (None, float('inf'), 0.0)

    best_ed, best_root = float('inf'), None
    for dnid in doc_tree.nodes:
        ed = tree_edit_distance(query_tree, doc_tree, query_root_id, dnid)
        if ed < best_ed:
            best_ed = ed
            best_root = dnid

    if best_root is None:
        return (None, float('inf'), 0.0)

    max_cost = 4 * len(query_tree.nodes) or 1
    score = max(0.0, 1.0 - best_ed / max_cost)
    return (best_root, best_ed, score)


# ============================================================================
# 4. FULL MATCH PIPELINE (Type I -> II -> III)
# ============================================================================

def match_pipeline(query_tree, doc_tree, check_label=True):
    """
    Full matching pipeline: Type I (exact) -> Type II (partial) -> Type III (edit).

    Returns: (match_type, coverage, distance_or_edit, score)
    """
    # Try Type I/II
    mtype, mapping, coverage, distance = find_best_match(
        query_tree, doc_tree, check_label=check_label
    )

    if mtype is not None:
        H_max = max(n.height for n in doc_tree.nodes.values()) or 1.0
        score = coverage / (1.0 + distance / H_max)
        return (mtype, coverage, distance, score)

    # Fallback to Type III
    best_root, edit_dist, edit_score = type_iii_match(query_tree, doc_tree)
    if best_root is not None:
        return ('III', 0.0, edit_dist, edit_score)

    return ('NONE', 0.0, float('inf'), 0.0)


# ============================================================================
# 5. COMMON BUILDERS
# ============================================================================

NODE_CATEGORIES = {
    'ENTITY', 'ACTION', 'TENSE', 'ASPECT', 'EVIDENTIAL',
    'LOCATIVE', 'MANNER', 'LOGICAL'
}

CATEGORY_COLORS = {
    'ACTION': '#e94560', 'ENTITY': '#0f3460', 'TENSE': '#f0a500',
    'LOCATIVE': '#00b894', 'MANNER': '#6c5ce7', 'ASPECT': '#a29bfe',
    'EVIDENTIAL': '#fd79a8', 'LOGICAL': '#636e72',
}

SURFACE_FORMS = {
    "English":    {"BITE": "bite",    "dog": "dog",    "man": "man",
                   "PAST": "(past)",  "YESTERDAY": "yesterday", "CHASE": "chase"},
    "Turkish":    {"BITE": "isir",    "dog": "kopek",  "man": "adam",
                   "PAST": "-di",     "YESTERDAY": "dun",       "CHASE": "kovala"},
    "Mohawk":     {"BITE": "'kahra'ko", "dog": "wak-", "man": "-honwa-",
                   "PAST": "wa-",     "YESTERDAY": "tsi'niyo"},
    "Finnish":    {"BITE": "puri",     "dog": "koira",  "man": "mies",
                   "PAST": "-i",       "YESTERDAY": "eilen"},
    "Inuktitut":  {"BITE": "kiisijuq", "dog": "qimmiq", "man": "anguti",
                   "PAST": "-juq",     "YESTERDAY": "ippaksaq"},
}


def build_query_tree(language="English"):
    """Standard 'dog bit man yesterday' query NST."""
    sf = SURFACE_FORMS.get(language, SURFACE_FORMS["English"])
    tree = NestedSemanticTree(
        f"{language}: {sf['dog']} {sf['BITE']} {sf['man']} {sf['YESTERDAY']}",
        language
    )
    tree.add_node("b", "BITE", "ACTION", None, 4.0)
    tree.add_node("d", "dog", "ENTITY", "b", 0.0)
    tree.add_node("m", "man", "ENTITY", "b", 0.0)
    tree.add_node("p", "PAST", "TENSE", "b", 2.0)
    tree.add_node("y", "YESTERDAY", "LOCATIVE", "p", 0.0)
    tree.preprocess_lca()
    return tree


def build_doc(name, lang, nodes_spec):
    """Build a document NST from [(id, label, cat, parent, height), ...]."""
    tree = NestedSemanticTree(name, lang)
    for nid, label, cat, pid, h in nodes_spec:
        tree.add_node(nid, label, cat, pid, h)
    tree.preprocess_lca()
    return tree


def rank_results(query_tree, corpus, check_label=True):
    """Rank all corpus documents by match score against query."""
    results = []
    for idx, doc in enumerate(corpus):
        mtype, cov, dist_ed, score = match_pipeline(query_tree, doc, check_label)
        if mtype != 'NONE':
            results.append((idx, doc.name, mtype, cov, dist_ed, score))
    results.sort(key=lambda r: (-r[5], r[4]))
    return results


def detect_clusters(ranked, threshold=0.15):
    """Detect natural cluster boundaries in ranked results."""
    cuts = []
    for i in range(1, len(ranked)):
        if ranked[i - 1][5] - ranked[i][5] > threshold:
            cuts.append(i)
    return cuts


# ============================================================================
# 6. SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("nst_core.py — Shared NST Library")
    print(f"  Node categories: {sorted(NODE_CATEGORIES)}")
    print(f"  Surface form languages: {sorted(SURFACE_FORMS.keys())}")

    # Quick smoke test
    t = build_query_tree("English")
    assert len(t.nodes) == 5
    assert t.root.label == "BITE"
    tv, vv = t.verify_ultrametric()
    assert vv == 0, f"Ultrametric check failed: {vv} violations"

    # Test distance
    d = t.ultrametric_distance("d", "m")
    assert abs(d - 4.0) < 1e-10, f"Expected d=4.0, got {d}"

    # Test matching on trivial corpus
    d1 = build_doc("TestDoc", "English", [
        ("b1","BITE","ACTION",None,4), ("d1","dog","ENTITY","b1",0),
        ("m1","man","ENTITY","b1",0), ("p1","PAST","TENSE","b1",2),
        ("y1","YESTERDAY","LOCATIVE","p1",0)
    ])
    mtype, cov, dist_ed, score = match_pipeline(t, d1)
    assert mtype == 'I', f"Expected Type I match, got {mtype}"
    assert abs(score - 1.0) < 1e-10, f"Expected score 1.0, got {score}"

    print("  All self-tests PASSED")
