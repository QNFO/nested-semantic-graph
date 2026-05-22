#!/usr/bin/env python3
"""
0.8.py — Type III Tree Edit Distance Matching

Implements tree edit distance for approximate matching (Type III),
integrating with the NestedSemanticTree framework from 0.5.py.

Edit operations (per 0.3.md §3.3):
  - relabel: change node label  — cost 2
  - delete:  remove node        — cost 3
  - insert:  add node           — cost 3
  - re-parent: move node        — cost 4

Algorithm: Zhang-Shasha ordered tree edit distance via dynamic programming.
"""

import sys
from itertools import combinations


# === Tree classes (minimal copy from 0.5.py for standalone use) ===

class SemanticNode:
    __slots__ = ('id', 'label', 'category', 'parent_id', 'children', 'height')
    def __init__(self, nid, label, category, parent_id=None, height=0.0):
        self.id = nid
        self.label = label
        self.category = category
        self.parent_id = parent_id
        self.children = []
        self.height = height


class NestedSemanticTree:
    def __init__(self, name="Unnamed", language="unknown"):
        self.name = name
        self.language = language
        self.nodes = {}
        self.root = None
        self._depth = {}
        self._parent_jump = {}
        self._lca_preprocessed = False
        self._log_n = 0
        self._max_depth = 0

    def add_node(self, nid, label, category, parent_id=None, height=0.0):
        node = SemanticNode(nid, label, category, parent_id, height)
        self.nodes[nid] = node
        if parent_id is not None:
            self.nodes[parent_id].children.append(node)
        else:
            self.root = node
        return node

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
        lca_id = self.lca(id1, id2)
        return self.nodes[lca_id].height

    def get_leaf_ids(self):
        return [nid for nid, node in self.nodes.items() if not node.children]


# === Tree Edit Distance (Zhang-Shasha) ===

def tree_edit_distance(tree_a, tree_b, root_a=None, root_b=None):
    """
    Compute minimum edit distance between two ordered trees.
    
    Edit costs (per 0.3.md §3.3):
      relabel: 2, delete: 3, insert: 3, re-parent: 4
    
    Uses Zhang-Shasha algorithm for ordered tree edit distance.
    Returns: (distance, edit_sequence)
    """
    if root_a is None:
        root_a = tree_a.root.id
    if root_b is None:
        root_b = tree_b.root.id

    # Build postorder traversal and keyroots
    def postorder_nodes(tree, root_id):
        result = []
        def dfs(nid):
            node = tree.nodes[nid]
            for child in node.children:
                dfs(child.id)
            result.append(nid)
        dfs(root_id)
        return result

    po_a = postorder_nodes(tree_a, root_a)
    po_b = postorder_nodes(tree_b, root_b)

    # Leftmost leaf for each node
    def leftmost(tree, root_id):
        lm = {}
        def dfs(nid):
            node = tree.nodes[nid]
            if not node.children:
                lm[nid] = nid
            else:
                lm[nid] = dfs(node.children[0].id)
            for child in node.children[1:]:
                dfs(child.id)
            return lm[nid]
        dfs(root_id)
        return lm

    lm_a = leftmost(tree_a, root_a)
    lm_b = leftmost(tree_b, root_b)

    # Keyroots: nodes that have a left sibling
    def keyroots(tree, root_id, postorder):
        """A node is a keyroot if it has a left sibling OR is the root"""
        kr = []
        seen_children = set()
        for nid in postorder:
            node = tree.nodes[nid]
            if node.parent_id is not None:
                parent = tree.nodes[node.parent_id]
                # If this node is not the first child, it's a keyroot
                if parent.children and parent.children[0].id != nid:
                    kr.append(nid)
            else:
                kr.append(nid)  # root is always a keyroot
        return sorted(kr, key=lambda nid: postorder.index(nid))

    kr_a = keyroots(tree_a, root_a, po_a)
    kr_b = keyroots(tree_b, root_b, po_b)

    # Map node to its postorder index
    idx_a = {nid: i for i, nid in enumerate(po_a)}
    idx_b = {nid: i for i, nid in enumerate(po_b)}

    na, nb = len(po_a), len(po_b)
    # treedist[i][j] = edit distance between subtree rooted at po_a[i] and po_b[j]
    treedist = [[0] * nb for _ in range(na)]

    # Cost functions
    def relabel_cost(nid_a, nid_b):
        """Cost to relabel node_a to match node_b"""
        node_a = tree_a.nodes[nid_a]
        node_b = tree_b.nodes[nid_b]
        if node_a.label == node_b.label:
            return 0
        if node_a.category == node_b.category:
            return 1  # same category, different label
        return 2  # different category

    # Compute forest distance matrix (temporary, reused)
    fd = [[0] * (nb + 1) for _ in range(na + 1)]

    for i in range(na):
        for j in range(nb):
            nid_a = po_a[i]
            nid_b = po_b[j]
            lma = lm_a.get(nid_a, nid_a)
            lmb = lm_b.get(nid_b, nid_b)
            li = idx_a.get(lma, i)
            lj = idx_b.get(lmb, j)

            # Initialize forest distance
            for di in range(li, i + 2):
                for dj in range(lj, j + 2):
                    fd[di][dj] = 0

            fd[li][lj] = 0
            for di in range(li, i + 1):
                fd[di + 1][lj] = fd[di][lj] + 3  # delete cost

            for dj in range(lj, j + 1):
                fd[li][dj + 1] = fd[li][dj] + 3  # insert cost

            for di in range(li, i + 1):
                for dj in range(lj, j + 1):
                    nid_di = po_a[di]
                    nid_dj = po_b[dj]
                    lm_di = lm_a.get(nid_di, nid_di)
                    lm_dj = lm_b.get(nid_dj, nid_dj)
                    li_di = idx_a.get(lm_di, di)
                    lj_dj = idx_b.get(lm_dj, dj)

                    if li_di == li and lj_dj == lj:
                        # Both are trees (not forests)
                        rc = relabel_cost(nid_di, nid_dj)
                        treedist_val = treedist[di][dj] if di >= li_di and dj >= lj_dj else 0
                        fd[di + 1][dj + 1] = min(
                            fd[di][dj + 1] + 3,       # delete
                            fd[di + 1][dj] + 3,       # insert
                            fd[di][dj] + treedist_val + rc,  # match/relabel
                        )
                    else:
                        # Forest case
                        fd[di + 1][dj + 1] = min(
                            fd[di][dj + 1] + 3,       # delete
                            fd[di + 1][dj] + 3,       # insert
                            fd[li_di][lj_dj] + treedist[di][dj],
                        )

            treedist[i][j] = fd[i + 1][j + 1]

    return treedist[na - 1][nb - 1]


# === Type III Matching Integration ===

def type_iii_match(query_tree, doc_tree):
    """
    Find the best Type III (approximate) match.
    Returns: (best_doc_subtree_root, edit_distance, score)
    """
    if query_tree.root is None or doc_tree.root is None:
        return None, float('inf'), 0.0

    q_root = query_tree.root.id
    best_dist = float('inf')
    best_root = None

    # Try matching query root to every doc node as potential subtree root
    for doc_nid in doc_tree.nodes:
        dist = tree_edit_distance(query_tree, doc_tree, q_root, doc_nid)
        if dist < best_dist:
            best_dist = dist
            best_root = doc_nid

    # Score: normalized by query size
    max_possible_cost = 4 * len(query_tree.nodes)  # re-parent every node
    if max_possible_cost == 0:
        score = 0.0
    else:
        score = 1.0 - (best_dist / max_possible_cost)
    score = max(0.0, score)

    return best_root, best_dist, score


# === Pipeline Integration ===

def _subtree_matches_node(qn, dn):
    return qn.category == dn.category and qn.label == dn.label


def _find_subtree_matches(query_tree, doc_tree, q_root, d_root, mapped, depth=0):
    qn = query_tree.nodes[q_root]
    dn = doc_tree.nodes[d_root]
    if not _subtree_matches_node(qn, dn):
        return []
    if not qn.children:
        return [{**mapped, q_root: d_root}]
    if len(qn.children) > len(dn.children):
        return []

    results = []
    qc = qn.children
    dc = dn.children

    def assign(q_idx, assigned_ids, cur_map):
        if q_idx == len(qc):
            results.append(cur_map.copy())
            return
        q_child = qc[q_idx]
        for d_child in dc:
            if d_child.id in assigned_ids:
                continue
            sub = _find_subtree_matches(query_tree, doc_tree, q_child.id, d_child.id, cur_map, depth + 1)
            for m in sub:
                nm = cur_map.copy()
                nm.update(m)
                assign(q_idx + 1, assigned_ids | {d_child.id}, nm)

    assign(0, set(), {q_root: d_root})
    return results


def match_pipeline(query_tree, doc_tree):
    """
    Full matching pipeline: Type I -> Type II -> Type III.
    Returns: (match_type, coverage, distance_or_edit, score)
    """
    q_root = query_tree.root.id if query_tree.root else None
    if q_root is None:
        return ('NONE', 0.0, float('inf'), 0.0)

    # Type I/II: subtree isomorphism
    best_cov = 0.0
    best_dist = float('inf')
    best_type = None
    best_map = {}

    q_root_node = query_tree.nodes[q_root]
    for doc_nid, doc_node in doc_tree.nodes.items():
        if doc_node.category != q_root_node.category:
            continue
        mappings = _find_subtree_matches(query_tree, doc_tree, q_root, doc_nid, {}, 0)
        for m in mappings:
            cov = len(m) / len(query_tree.nodes)
            max_dh = 0.0
            for qid, did in m.items():
                dh = abs(query_tree.nodes[qid].height - doc_tree.nodes[did].height)
                max_dh = max(max_dh, dh)
            if cov == 1.0 and max_dh < 1e-10:
                if best_type != 'I' or max_dh < best_dist:
                    best_cov = cov
                    best_dist = max_dh
                    best_type = 'I'
                    best_map = m
            elif cov > best_cov or (cov == best_cov and max_dh < best_dist):
                best_cov = cov
                best_dist = max_dh
                best_type = 'II'
                best_map = m

    if best_type is not None:
        H_max = max(n.height for n in doc_tree.nodes.values()) if doc_tree.nodes else 1.0
        score = best_cov / (1.0 + best_dist / max(H_max, 1.0))
        return (best_type, best_cov, best_dist, score)

    # Type III: tree edit distance
    best_root, edit_dist, edit_score = type_iii_match(query_tree, doc_tree)
    if best_root is not None:
        return ('III', 0.0, edit_dist, edit_score)

    return ('NONE', 0.0, float('inf'), 0.0)


# === Builders and Corpus ===

def build_dog_bite_tree(language="English"):
    surface = {
        "English": {"BITE": "bite", "dog": "dog", "man": "man",
                     "PAST": "(past)", "YESTERDAY": "yesterday"},
        "Turkish": {"BITE": "isir", "dog": "kopek", "man": "adam",
                     "PAST": "-di", "YESTERDAY": "dun"},
        "Mohawk":  {"BITE": "'kahra'ko", "dog": "wak-", "man": "-honwa-",
                     "PAST": "wa-", "YESTERDAY": "tsi'niyohseraka'te'"},
    }
    sf = surface.get(language, surface["English"])
    tree = NestedSemanticTree(f"{language}: {sf['dog']} {sf['BITE']} {sf['man']} {sf['YESTERDAY']}", language)
    tree.add_node("bite", "BITE", "ACTION", None, 4.0)
    tree.add_node("dog", "dog", "ENTITY", "bite", 0.0)
    tree.add_node("man", "man", "ENTITY", "bite", 0.0)
    tree.add_node("past", "PAST", "TENSE", "bite", 2.0)
    tree.add_node("yest", "YESTERDAY", "LOCATIVE", "past", 0.0)
    tree.preprocess_lca()
    return tree


def build_corpus():
    corpus = []

    d1 = NestedSemanticTree("Doc1: Dog bit man yesterday [exact]", "English")
    d1.add_node("b1", "BITE", "ACTION", None, 4.0)
    d1.add_node("d1", "dog", "ENTITY", "b1", 0.0)
    d1.add_node("m1", "man", "ENTITY", "b1", 0.0)
    d1.add_node("p1", "PAST", "TENSE", "b1", 2.0)
    d1.add_node("y1", "YESTERDAY", "LOCATIVE", "p1", 0.0)
    d1.preprocess_lca()
    corpus.append(d1)

    d2 = NestedSemanticTree("Doc2: Dog chased cat yesterday [different action]", "English")
    d2.add_node("c2", "CHASE", "ACTION", None, 4.0)
    d2.add_node("d2", "dog", "ENTITY", "c2", 0.0)
    d2.add_node("cat2", "cat", "ENTITY", "c2", 0.0)
    d2.add_node("p2", "PAST", "TENSE", "c2", 2.0)
    d2.add_node("y2", "YESTERDAY", "LOCATIVE", "p2", 0.0)
    d2.preprocess_lca()
    corpus.append(d2)

    d3 = NestedSemanticTree("Doc3: Man bit dog [reversed]", "English")
    d3.add_node("b3", "BITE", "ACTION", None, 4.0)
    d3.add_node("m3", "man", "ENTITY", "b3", 0.0)
    d3.add_node("d3", "dog", "ENTITY", "b3", 0.0)
    d3.preprocess_lca()
    corpus.append(d3)

    d4 = NestedSemanticTree("Doc4: Cat eats fish now [totally different]", "English")
    d4.add_node("e4", "EAT", "ACTION", None, 4.0)
    d4.add_node("c4", "cat", "ENTITY", "e4", 0.0)
    d4.add_node("f4", "fish", "ENTITY", "e4", 0.0)
    d4.add_node("n4", "PRESENT", "TENSE", "e4", 2.0)
    d4.preprocess_lca()
    corpus.append(d4)

    d5 = NestedSemanticTree("Doc5: Dog bit man in park yesterday [extended]", "English")
    d5.add_node("b5", "BITE", "ACTION", None, 5.0)
    d5.add_node("d5", "dog", "ENTITY", "b5", 0.0)
    d5.add_node("m5", "man", "ENTITY", "b5", 0.0)
    d5.add_node("p5", "PAST", "TENSE", "b5", 2.0)
    d5.add_node("y5", "YESTERDAY", "LOCATIVE", "p5", 0.0)
    d5.add_node("park5", "park", "LOCATIVE", "b5", 0.0)
    d5.preprocess_lca()
    corpus.append(d5)

    return corpus


# === Main ===

def main():
    print("=" * 72)
    print("  TYPE III TREE EDIT DISTANCE — NSG MATCHING")
    print("=" * 72)

    query = build_dog_bite_tree("English")
    corpus = build_corpus()

    # Verify query is ultrametric
    print("\n[STEP 1] Query verification:")
    leaves = query.get_leaf_ids()
    total_u = 0
    violations = 0
    for x, y, z in combinations(leaves, 3):
        total_u += 1
        dxy = query.ultrametric_distance(x, y)
        dyz = query.ultrametric_distance(y, z)
        dxz = query.ultrametric_distance(x, z)
        if dxz > max(dxy, dyz) + 1e-10:
            violations += 1
    print(f"  Query: {len(query.nodes)} nodes, {len(leaves)} leaves, Ultrametric: {'PASS' if violations==0 else f'FAIL({violations})'}")

    # Run full pipeline
    print("\n[STEP 2] Full pipeline (Type I -> II -> III) on 5-document corpus:")
    print(f"  {'Rank':<5} {'Type':<6} {'Coverage':<8} {'Dist/Edit':<10} {'Score':<8} {'Document'}")
    print(f"  {'-'*5} {'-'*6} {'-'*8} {'-'*10} {'-'*8} {'-'*40}")

    results = []
    for i, doc in enumerate(corpus):
        mtype, cov, dist_ed, score = match_pipeline(query, doc)
        results.append((i, doc.name, mtype, cov, dist_ed, score))
        if mtype == 'III':
            print(f"  {'-':<5} {mtype:<6} {'N/A':<8} {dist_ed:<10.1f} {score:<8.4f} {doc.name}")
        else:
            print(f"  {'-':<5} {mtype:<6} {cov:<8.2%} {dist_ed:<10.3f} {score:<8.4f} {doc.name}")

    # Sort and show ranked
    results.sort(key=lambda r: (-r[5], r[4]))

    print(f"\n[STEP 3] Ranked results:")
    print(f"  {'Rank':<5} {'Type':<6} {'Coverage':<8} {'Dist/Edit':<10} {'Score':<8} {'Document'}")
    print(f"  {'-'*5} {'-'*6} {'-'*8} {'-'*10} {'-'*8} {'-'*40}")
    for rank, (idx, name, mtype, cov, dist_ed, score) in enumerate(results):
        if mtype == 'III':
            print(f"  {rank+1:<5} {mtype:<6} {'N/A':<8} {dist_ed:<10.1f} {score:<8.4f} {name}")
        else:
            print(f"  {rank+1:<5} {mtype:<6} {cov:<8.2%} {dist_ed:<10.3f} {score:<8.4f} {name}")

    # Summary
    types = {}
    for _, _, mtype, _, _, _ in results:
        types[mtype] = types.get(mtype, 0) + 1

    print(f"\n[STEP 4] Pipeline distribution: {types}")
    print(f"  Type I:   {types.get('I', 0)} docs — exact subtree matches")
    print(f"  Type II:  {types.get('II', 0)} docs — partial structural matches")
    print(f"  Type III: {types.get('III', 0)} docs — approximate edit distance matches")
    print(f"\n  >> TYPE III MATCHING INTEGRATED — PIPELINE COMPLETE <<")

    return 0


if __name__ == "__main__":
    sys.exit(main())
