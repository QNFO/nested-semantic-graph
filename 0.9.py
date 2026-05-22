#!/usr/bin/env python3
"""
0.9.py -- Enhanced Corpus (12 documents, 5 languages) (REFACTORED)

Now imports from nst_core.py (S5.1 shared library).
"""

import sys
from nst_core import (NestedSemanticTree, build_query_tree, build_doc,
                       match_pipeline, rank_results, detect_clusters)


def build_expanded_corpus():
    c = []
    # ENGLISH (isolating) -- 6 docs
    c.append(build_doc("EN-1: Dog bit man yesterday [exact]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)]))
    c.append(build_doc("EN-2: Dog chased cat yesterday [diff action]", "English", [
        ("c","CHASE","ACTION",None,4), ("d","dog","ENTITY","c",0), ("ct","cat","ENTITY","c",0),
        ("p","PAST","TENSE","c",2), ("y","YESTERDAY","LOCATIVE","p",0)]))
    c.append(build_doc("EN-3: Man bit dog [reversed]", "English", [
        ("b","BITE","ACTION",None,4), ("m","man","ENTITY","b",0), ("dg","dog","ENTITY","b",0)]))
    c.append(build_doc("EN-4: Cat eats fish now [different]", "English", [
        ("e","EAT","ACTION",None,4), ("c","cat","ENTITY","e",0), ("f","fish","ENTITY","e",0),
        ("n","PRESENT","TENSE","e",2)]))
    c.append(build_doc("EN-5: Dog bit man in park yesterday [extended]", "English", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0), ("pk","park","LOCATIVE","b",0)]))
    c.append(build_doc("EN-6: Dog bit man with stick [instrument]", "English", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("s","stick","ENTITY","b",0)]))
    # TURKISH -- 2 docs
    c.append(build_doc("TR-1: Kopek adami isirdi [exact, no yesterday]", "Turkish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)]))
    c.append(build_doc("TR-2: Kopek adami parkta isirdi [extended]", "Turkish", [
        ("b","BITE","ACTION",None,5), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("pk","park","LOCATIVE","b",0)]))
    # MOHAWK -- 1 doc
    c.append(build_doc("MH-1: Wahonwa'kahra'ko' [bite event]", "Mohawk", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)]))
    # FINNISH -- 2 docs
    c.append(build_doc("FI-1: Koira puri miesta eilen [exact]", "Finnish", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2), ("y","YESTERDAY","LOCATIVE","p",0)]))
    c.append(build_doc("FI-2: Koira juoksi [dog ran, minimal]", "Finnish", [
        ("r","RUN","ACTION",None,4), ("d","dog","ENTITY","r",0), ("p","PAST","TENSE","r",2)]))
    # INUKTITUT -- 1 doc
    c.append(build_doc("IK-1: Qimmiq angutimik kiisijuq [exact]", "Inuktitut", [
        ("b","BITE","ACTION",None,4), ("d","dog","ENTITY","b",0), ("m","man","ENTITY","b",0),
        ("p","PAST","TENSE","b",2)]))
    return c


def main():
    print("=" * 60)
    print("  ENHANCED CORPUS (nst_core)")
    print("=" * 60)

    corpus = build_expanded_corpus()
    query = build_query_tree("English")

    # Verify
    all_ultra = all(t.verify_ultrametric()[1] == 0 for t in corpus)
    print(f"  All ultrametric: {'PASS' if all_ultra else 'FAIL'} ({len(corpus)} docs)")

    # Cross-linguistic search
    langs = {}
    for t in corpus:
        langs[t.language] = langs.get(t.language, 0) + 1
    print(f"  Languages: {dict(sorted(langs.items()))}")

    from nst_core import build_query_tree as bqt
    for lang in ["English","Turkish","Mohawk","Finnish","Inuktitut"]:
        q = bqt(lang)
        r = rank_results(q, corpus)
        if r:
            print(f"  {lang:<12}: top match = {r[0][1][:50]}")

    print(f"\n  >> ENHANCED CORPUS (nst_core) <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
