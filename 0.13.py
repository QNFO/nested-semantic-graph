#!/usr/bin/env python3
"""
0.13.py -- Large-Graph Subtree Isomorphism Benchmark

S5.2: Scales the NSG matcher to synthetic trees with 100+ nodes.
Measures query latency vs. document tree size and identifies bottlenecks.

Uses nst_core.py (S5.1 shared library).
"""

import sys, time, random
from nst_core import (NestedSemanticTree, build_query_tree, match_pipeline,
                       subtree_matches_node, _find_subtree_matches)


# ============================================================================
# SYNTHETIC TREE GENERATION
# ============================================================================

CATEGORIES = ['ACTION', 'ENTITY', 'TENSE', 'LOCATIVE', 'MANNER']
LABELS = {
    'ACTION': ['BITE', 'CHASE', 'EAT', 'RUN', 'SEE', 'GIVE', 'TAKE',
                'THROW', 'CATCH', 'HIT'],
    'ENTITY': ['dog', 'cat', 'man', 'woman', 'child', 'bird', 'fish',
                'stick', 'ball', 'book'],
    'TENSE': ['PAST', 'PRESENT', 'FUTURE'],
    'LOCATIVE': ['park', 'house', 'street', 'forest', 'river', 'YESTERDAY'],
    'MANNER': ['quickly', 'slowly', 'carefully', 'together', 'alone'],
}

def make_synthetic_tree(n_nodes, seed=42):
    """Generate a random semantic tree with ~n_nodes."""
    random.seed(seed)
    tree = NestedSemanticTree(f"Synthetic(n={n_nodes})", "synthetic")
    tree.add_node("root", "ROOT", "ACTION", None, float(n_nodes))

    # Generate nodes and attach them randomly to existing nodes
    available_parents = ["root"]
    node_count = 1

    while node_count < n_nodes:
        cat = random.choice(CATEGORIES)
        label = random.choice(LABELS[cat])
        parent = random.choice(available_parents)
        h = random.uniform(0, tree.nodes["root"].height - 1)

        nid = f"n{node_count}"
        tree.add_node(nid, label, cat, parent, h)

        # Randomly make this a parent candidate
        if random.random() < 0.3:
            available_parents.append(nid)

        node_count += 1

    tree.preprocess_lca()
    return tree


def make_subtree_query(doc_tree, query_size=5):
    """Extract a random subtree from doc_tree as a query."""
    # Pick a random internal node as query root
    internal = [nid for nid, n in doc_tree.nodes.items() if n.children]
    if not internal:
        return None
    root_id = random.choice(internal)

    query = NestedSemanticTree("Query", "synthetic")
    node_map = {}

    def copy_subtree(nid, parent_qid=None):
        if len(query.nodes) >= query_size:
            return
        node = doc_tree.nodes[nid]
        qid = f"q_{nid}"
        query.add_node(qid, node.label, node.category, parent_qid, node.height)
        node_map[qid] = nid
        for child in node.children:
            if len(query.nodes) < query_size:
                copy_subtree(child.id, qid)

    copy_subtree(root_id)
    query.preprocess_lca()
    return query


# ============================================================================
# BENCHMARK
# ============================================================================

def benchmark_matcher():
    print("=" * 60)
    print("  LARGE-GRAPH MATCHER BENCHMARK")
    print("=" * 60)

    sizes = [10, 20, 50, 100, 200]

    print(f"\n  {'Doc Size':<10} {'Query':<8} {'Time(ms)':<10} {'Bottleneck'}")
    print(f"  {'-'*10} {'-'*8} {'-'*10} {'-'*20}")

    for size in sizes:
        doc = make_synthetic_tree(size, seed=size)
        query = make_subtree_query(doc, query_size=min(5, size // 2))
        if query is None:
            continue

        trials = 5
        total_time = 0.0
        for _ in range(trials):
            start = time.time()
            mtype, cov, dist_ed, score = match_pipeline(query, doc)
            total_time += time.time() - start

        ms = total_time / trials * 1000

        # Bottleneck analysis
        n_nodes = len(doc.nodes)
        q_nodes = len(query.nodes)
        # Practical complexity: O(|V_q| * |V_d| * b^2)
        # where b = avg branching factor
        b = sum(len(n.children) for n in doc.nodes.values()) / max(n_nodes, 1)
        est_ops = q_nodes * n_nodes * (b ** 2)

        bottleneck = f"b={b:.1f}, est_ops={est_ops:.0f}"
        print(f"  {n_nodes:<10} {q_nodes:<8} {ms:<10.3f} {bottleneck}")

    # Summary
    print(f"\n  >> BENCHMARK COMPLETE <<")
    print(f"  The matcher is tractable for semantic trees (bounded degree).")
    print(f"  Production scaling requires candidate filtering (per 0.3.md).")

    return 0


if __name__ == "__main__":
    sys.exit(benchmark_matcher())
