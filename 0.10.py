#!/usr/bin/env python3
"""
0.10.py -- Turkish Morphological Pipeline (REFACTORED)

Simulates Zemberek morphological analysis, builds NSTs from morpheme output.
Now imports from nst_core.py (S5.1 shared library).
"""

import sys, time
from nst_core import (NestedSemanticTree, match_pipeline, rank_results,
                       build_doc, build_query_tree)


def zemberek_parse(sentence, gloss):
    """Simulate Zemberek morphological analysis."""
    return gloss


def build_nst_from_morph(name, language, morphemes):
    """Build an NST from morphological analysis output."""
    tree = NestedSemanticTree(name, language)
    node_count = [0]
    def nid(pref="n"):
        node_count[0] += 1
        return f"{pref}{node_count[0]}"

    entities = []; action = None; tense = None; locative = None

    for morph, tags in morphemes:
        tag_set = set(tags.split('+'))
        if 'Verb' in tag_set:
            action = ('BITE' if 'isir' in morph else morph.upper(), morph)
        elif 'Noun' in tag_set and 'Acc' not in tag_set:
            entities.append(('dog' if 'kopek' in morph else 'man' if 'adam' in morph else morph, morph))
        elif 'Noun' in tag_set and 'Acc' in tag_set:
            entities.append(('man' if 'adam' in morph else 'cat' if 'kedi' in morph else morph, morph))
        elif 'Past' in tag_set:
            tense = ('PAST', morph)
        elif 'Time' in tag_set or ('Adv' in tag_set and 'dun' in morph):
            locative = ('YESTERDAY', morph)

    if action:
        aid = nid()
        tree.add_node(aid, action[0], "ACTION", None, 4.0)
        for elabel, eform in entities:
            tree.add_node(nid(), elabel, "ENTITY", aid, 0.0)
        if tense:
            tid = nid()
            tree.add_node(tid, tense[0], "TENSE", aid, 2.0)
            if locative:
                tree.add_node(nid(), locative[0], "LOCATIVE", tid, 0.0)

    tree.preprocess_lca()
    return tree


def compute_precision_recall(query, corpus, relevant_ids, k=5):
    """Precision@k, Recall@k, MRR."""
    results = rank_results(query, corpus)
    top_k = [r[0] for r in results[:k]]
    rel_in_k = len(set(top_k) & relevant_ids)
    precision = rel_in_k / k if k > 0 else 0.0
    recall = rel_in_k / len(relevant_ids) if relevant_ids else 0.0
    mrr = 0.0
    for rank, (idx, _, _, _, _, _) in enumerate(results):
        if idx in relevant_ids:
            mrr = 1.0 / (rank + 1)
            break
    return precision, recall, mrr


def main():
    print("=" * 60)
    print("  TURKISH MORPHOLOGICAL PIPELINE (nst_core)")
    print("=" * 60)

    # Build corpus via morphological pipeline
    c = []
    c.append(build_nst_from_morph("TR-1: kopek adami dun isirdi [exact]", "Turkish",
        zemberek_parse("kopek adami dun isirdi", [
            ("kopek","Noun+A3sg+Pnon+Nom"),("adam","Noun+A3sg+Pnon"),("-i","Acc"),
            ("dun","Adv+Time"),("isir","Verb+Pos"),("-di","Past+A3sg")])))
    c.append(build_nst_from_morph("TR-2: kopek adami isirdi [no yesterday]", "Turkish",
        zemberek_parse("kopek adami isirdi", [
            ("kopek","Noun+A3sg+Pnon+Nom"),("adam","Noun+A3sg+Pnon"),("-i","Acc"),
            ("isir","Verb+Pos"),("-di","Past+A3sg")])))
    c.append(build_nst_from_morph("TR-3: kopek kediyi kovaladi [chase]", "Turkish",
        zemberek_parse("kopek kediyi kovaladi", [
            ("kopek","Noun+A3sg+Pnon+Nom"),("kedi","Noun+A3sg+Pnon"),("-yi","Acc"),
            ("kovala","Verb+Pos"),("-di","Past+A3sg")])))

    all_ultra = all(t.verify_ultrametric()[1] == 0 for t in c)
    print(f"  All ultrametric: {'PASS' if all_ultra else 'FAIL'}")

    query = build_nst_from_morph("Query", "Turkish", zemberek_parse("kopek adami dun isirdi", [
        ("kopek","Noun+A3sg+Pnon+Nom"),("adam","Noun+A3sg+Pnon"),("-i","Acc"),
        ("dun","Adv+Time"),("isir","Verb+Pos"),("-di","Past+A3sg")]))

    ranked = rank_results(query, c)
    for rank, (idx, name, mt, _, _, sc) in enumerate(ranked):
        print(f"  {rank+1}: {mt} {sc:.4f} {name}")

    rel = {0, 1}
    for k_ in [1, 2, 3]:
        p, r_, m = compute_precision_recall(query, c, rel, k_)
        print(f"  P@{k_}={p:.3f} R@{k_}={r_:.3f} MRR={m:.3f}")

    print(f"\n  >> TURKISH PIPELINE (nst_core) <<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
