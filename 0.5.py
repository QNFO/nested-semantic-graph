#!/usr/bin/env python3
"""
0.5.py -- Python Prototype: Graph Parser, Matcher & Ranking Engine

REFACTORED to import from nst_core.py (S5.1).

Brings together the full pipeline:
  1. Build Nested Semantic Trees from sentence specifications
  2. Build a document corpus (5 documents)
  3. Subtree isomorphism search (Type I/II)
  4. Ranking using ultrametric graph distance
  5. End-to-end demonstration across languages

Grounded in: 0.2.md, 0.3.md, nst_core.py
"""

import sys
from nst_core import (NestedSemanticTree, build_query_tree, build_doc,
                       match_pipeline, rank_results, detect_clusters)


# ============================================================================
# CORPUS (5 documents)
# ============================================================================

def build_document_corpus():
    c = []
    c.append(build_doc("Doc1: Dog bit man yesterday [exact]", "English", [
        ("b1","BITE","ACTION",None,4), ("d1","dog","ENTITY","b1",0),
        ("m1","man","ENTITY","b1",0), ("p1","PAST","TENSE","b1",2),
        ("y1","YESTERDAY","LOCATIVE","p1",0)]))
    c.append(build_doc("Doc2: Dog chased cat yesterday [partial]", "English", [
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


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("  NSG PIPELINE PROTOTYPE (using nst_core library)")
    print("=" * 60)

    corpus = build_document_corpus()
    query = build_query_tree("English")

    # Verify
    for i, doc in enumerate(corpus):
        n, v = doc.verify_ultrametric()
        ok = "PASS" if v == 0 else f"FAIL({v})"
        print(f"  [{i}] {doc.name}: {ok}")

    # Search
    print(f"\n  Query: dog bit man yesterday")
    ranked = rank_results(query, corpus)

    print(f"  {'Rank':<5} {'Type':<6} {'Score':<8} {'Document'}")
    for rank, (idx, name, mtype, cov, dist_ed, score) in enumerate(ranked):
        print(f"  {rank+1:<5} {mtype:<6} {score:<8.4f} {name}")

    cuts = detect_clusters(ranked)
    if cuts:
        print(f"\n  Cluster boundaries after ranks: {cuts}")

    print(f"\n  >> PIPELINE WORKING via nst_core <<")
    return 0

if __name__ == "__main__":
    sys.exit(main())
