#!/usr/bin/env python3
"""
0.8.py -- Type III Tree Edit Distance Matching (REFACTORED)

Implements tree edit distance for approximate matching.
Now imports from nst_core.py (S5.1 shared library).
"""

import sys
from nst_core import (NestedSemanticTree, build_query_tree, build_doc,
                       match_pipeline, rank_results, detect_clusters,
                       tree_edit_distance, type_iii_match)


def build_corpus():
    """5-document test corpus."""
    c = []
    c.append(build_doc("Doc1: Dog bit man yesterday [exact]", "English", [
        ("b1","BITE","ACTION",None,4), ("d1","dog","ENTITY","b1",0),
        ("m1","man","ENTITY","b1",0), ("p1","PAST","TENSE","b1",2),
        ("y1","YESTERDAY","LOCATIVE","p1",0)]))
    c.append(build_doc("Doc2: Dog chased cat yesterday [diff action]", "English", [
        ("c2","CHASE","ACTION",None,4), ("d2","dog","ENTITY","c2",0),
        ("cat","cat","ENTITY","c2",0), ("p2","PAST","TENSE","c2",2),
        ("y2","YESTERDAY","LOCATIVE","p2",0)]))
    c.append(build_doc("Doc3: Man bit dog [reversed]", "English", [
        ("b3","BITE","ACTION",None,4), ("m3","man","ENTITY","b3",0),
        ("d3","dog","ENTITY","b3",0)]))
    c.append(build_doc("Doc4: Cat eats fish [different]", "English", [
        ("e4","EAT","ACTION",None,4), ("c4","cat","ENTITY","e4",0),
        ("f4","fish","ENTITY","e4",0), ("n4","PRESENT","TENSE","e4",2)]))
    c.append(build_doc("Doc5: Dog bit man in park yesterday [extended]", "English", [
        ("b5","BITE","ACTION",None,5), ("d5","dog","ENTITY","b5",0),
        ("m5","man","ENTITY","b5",0), ("p5","PAST","TENSE","b5",2),
        ("y5","YESTERDAY","LOCATIVE","p5",0), ("pk","park","LOCATIVE","b5",0)]))
    return c


def main():
    print("=" * 60)
    print("  TYPE III TREE EDIT DISTANCE (nst_core)")
    print("=" * 60)

    query = build_query_tree("English")
    corpus = build_corpus()

    # Verify ultrametric
    for doc in corpus:
        n, v = doc.verify_ultrametric()
        print(f"  {'PASS' if v==0 else 'FAIL'} {doc.name} ({n} triples)")

    # Full pipeline
    print(f"\n  {'Type':<6} {'Score':<8} {'Document'}")
    results = []
    for i, doc in enumerate(corpus):
        mtype, cov, ed, score = match_pipeline(query, doc)
        results.append((i, doc.name, mtype, cov, ed, score))
        print(f"  {mtype:<6} {score:<8.4f} {doc.name}")

    ranked = rank_results(query, corpus)
    dist = {}
    for _, _, mt, _, _, _ in ranked:
        dist[mt] = dist.get(mt, 0) + 1
    print(f"\n  Pipeline: {dist}")
    print(f"  >> TYPE III INTEGRATED (nst_core) <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
