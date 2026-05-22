#!/usr/bin/env python3
"""
0.11.py -- Expanded 25+ Document Corpus + Scalability Benchmarks (REFACTORED)

Now imports from nst_core.py (S5.1 shared library).
"""

import sys, time
from nst_core import (NestedSemanticTree, build_query_tree, build_doc,
                       match_pipeline, rank_results, detect_clusters)


def build_expanded_corpus():
    c = []
    def d(name, lang, nodes_spec):
        c.append(build_doc(name, lang, nodes_spec))

    # ENGLISH -- 8
    d("EN-01: Dog bit man yesterday [exact]", "English", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("y","YESTERDAY","LOCATIVE","p",0)])
    d("EN-02: Dog chased cat yesterday [diff action]", "English", [("c","CHASE","ACTION",None,4),("d","dog","ENTITY","c",0),("ct","cat","ENTITY","c",0),("p","PAST","TENSE","c",2),("y","YESTERDAY","LOCATIVE","p",0)])
    d("EN-03: Man bit dog [reversed]", "English", [("b","BITE","ACTION",None,4),("m","man","ENTITY","b",0),("dg","dog","ENTITY","b",0)])
    d("EN-04: Cat eats fish now [different]", "English", [("e","EAT","ACTION",None,4),("c","cat","ENTITY","e",0),("f","fish","ENTITY","e",0),("n","PRESENT","TENSE","e",2)])
    d("EN-05: Dog bit man in park yesterday [extended]", "English", [("b","BITE","ACTION",None,5),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("y","YESTERDAY","LOCATIVE","p",0),("pk","park","LOCATIVE","b",0)])
    d("EN-06: Dog bit man with stick [instrument]", "English", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("s","stick","ENTITY","b",0)])
    d("EN-07: Large brown dog bit old man [modified]", "English", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("EN-08: Dog bit man quickly [manner]", "English", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("q","quickly","MANNER","b",0),("p","PAST","TENSE","b",2)])

    # TURKISH -- 5
    d("TR-01: Kopek adami isirdi [exact, no yesterday]", "Turkish", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("TR-02: Kopek adami parkta isirdi [extended]", "Turkish", [("b","BITE","ACTION",None,5),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("pk","park","LOCATIVE","b",0)])
    d("TR-03: Kopek kediyi kovaladi [chase]", "Turkish", [("c","CHASE","ACTION",None,4),("d","dog","ENTITY","c",0),("ct","cat","ENTITY","c",0),("p","PAST","TENSE","c",2)])
    d("TR-04: Adam kopegi isirdi [reversed]", "Turkish", [("b","BITE","ACTION",None,4),("m","man","ENTITY","b",0),("dg","dog","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("TR-05: Kopek adami hizla isirdi [quickly]", "Turkish", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("q","quickly","MANNER","b",0),("p","PAST","TENSE","b",2)])

    # MOHAWK -- 3
    d("MH-01: Wahonwa'kahra'ko' [bite]", "Mohawk", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("MH-02: [with yesterday]", "Mohawk", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("y","YESTERDAY","LOCATIVE","p",0)])
    d("MH-03: [dog ran]", "Mohawk", [("r","RUN","ACTION",None,4),("d","dog","ENTITY","r",0),("p","PAST","TENSE","r",2)])

    # FINNISH -- 5
    d("FI-01: Koira puri miesta eilen [exact]", "Finnish", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("y","YESTERDAY","LOCATIVE","p",0)])
    d("FI-02: Koira juoksi [dog ran]", "Finnish", [("r","RUN","ACTION",None,4),("d","dog","ENTITY","r",0),("p","PAST","TENSE","r",2)])
    d("FI-03: Koira puri miesta [no yesterday]", "Finnish", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("FI-04: Mies puri koiraa [reversed]", "Finnish", [("b","BITE","ACTION",None,4),("m","man","ENTITY","b",0),("dg","dog","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("FI-05: Koira puri miesta puistossa [extended]", "Finnish", [("b","BITE","ACTION",None,5),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("pk","park","LOCATIVE","b",0)])

    # INUKTITUT -- 4
    d("IK-01: Qimmiq angutimik kiisijuq [exact]", "Inuktitut", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("IK-02: [with yesterday]", "Inuktitut", [("b","BITE","ACTION",None,4),("d","dog","ENTITY","b",0),("m","man","ENTITY","b",0),("p","PAST","TENSE","b",2),("y","YESTERDAY","LOCATIVE","p",0)])
    d("IK-03: Qimmiq qimmiq mik kiisijuq [dog bit dog]", "Inuktitut", [("b","BITE","ACTION",None,4),("d1","dog","ENTITY","b",0),("d2","dog","ENTITY","b",0),("p","PAST","TENSE","b",2)])
    d("IK-04: Qimmiq nirijuq [dog ate]", "Inuktitut", [("e","EAT","ACTION",None,4),("d","dog","ENTITY","e",0),("p","PAST","TENSE","e",2)])
    return c


def benchmark(corpus, query, sizes):
    for size in sizes:
        sub = corpus[:min(size, len(corpus))]
        start = time.time()
        for _ in range(10):
            for doc in sub:
                _ = match_pipeline(query, doc)
        ms = max(time.time() - start, 0.001) / (10 * len(sub)) * 1000
        print(f"  {len(sub):<8} {ms:<10.3f} ms/query")


def main():
    print("=" * 60)
    print("  EXPANDED CORPUS + BENCHMARKS (nst_core)")
    print("=" * 60)

    corpus = build_expanded_corpus()
    query = build_query_tree("English")

    langs = {}
    for t in corpus:
        langs[t.language] = langs.get(t.language, 0) + 1
    print(f"\n  Corpus: {len(corpus)} docs, {sum(len(t.nodes) for t in corpus)} nodes")
    for lang, count in sorted(langs.items()):
        print(f"    {lang}: {count}")

    all_ultra = all(t.verify_ultrametric()[1] == 0 for t in corpus)
    print(f"  All ultrametric: {'PASS' if all_ultra else 'FAIL'}")

    ranked = rank_results(query, corpus)
    print(f"  Top match: {ranked[0][1][:55]} ({ranked[0][2]}, {ranked[0][5]:.4f})")

    print(f"\n  [BENCHMARK] Query latency vs. corpus size:")
    benchmark(corpus, query, [5, 10, 15, 20, 25])

    print(f"\n  >> EXPANDED CORPUS (nst_core) <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
