# Sprint Backlog — Sprint 1: Computational Architecture

**Sprint Goal:** Produce the computational specification and Python prototypes for sub-graph matching search on nested semantic graphs — the engineering sequel to "Few Become One."
**Started:** 2026-05-22
**Target End:** 2026-05-29
**Status:** Active

## Active Tasks

| ID | Task | DoD Criteria | Est. Effort | Status | Assignee |
|:---|:-----|:-------------|:------------|:-------|:---------|
| S0 | Internal Literature Review | Comprehensive due diligence report documenting ALL connections across the research corpus. | 4h | [x] | Agent |
| S1 | Formal Definitions & Grounding | **Read** Few Become One §V, Q-PNA §2-3, Tree Cophenetic §2. **Produce** LaTeX formalism for: nodes as conceptual primitives, edges as scope, ultrametric distance $d(x,y) = h(\text{LCA}(x,y))$, tree-alignment lattice for sub-graph matching. **Python** verify ultrametric property on example trees. | 3h | [x] | Agent |
| S2 | Sub-Graph Matching Search Spec | Specify the search problem: query graph $G_q$, document graph corpus $\{G_d\}$, matching criteria (subgraph isomorphism, approximate matching), ranking via ultrametric graph distance. Connect to Q-PNA's token encoding as the parser front-end. | 2h | [x] | Agent |
| S3 | Cross-Linguistic Examples | English "dog bit man yesterday" and Mohawk equivalent mapped to same semantic graph. Linearization rules for each language. Connect to Language-Info-Architecture's entropy gradient findings. | 2h | [x] | Agent |
| S4 | Python Prototype: Graph Parser & Matcher | Parse example sentences to trees, implement brute-force subgraph isomorphism for small graphs, compute ultrametric graph distance for ranking. | 3h | [x] | Agent |
| S5 | Computational Pathway | Component diagram connecting: morphological analyzer → semantic parser → graph encoder → index → query engine. Map to existing Q-PNA architecture. Feasibility assessment. | 2h | [ ] | Agent |
| S6 | Reader Testing & Revision | Blind reader test on draft (REVIEWER subagent). Address blocking/major issues. Polish for publication. | 2h | [ ] | Agent |

## Key Prior Work to Reference

| Reference | Path/DOI | Role |
|:----------|:---------|:-----|
| 0.1.md — Internal Literature Review | This project | Complete research landscape (35+ projects, 12 papers, 6 repos) |
| 0.2.md / 0.2.py — Formal Definitions | This project | Mathematical grounding, Python-verified |
| 0.3.md — Search Spec | This project | Sub-graph matching architecture |
| 0.4.md — Cross-Linguistic Examples | This project | English/Turkish/Mohawk isomorphism |
| Few Become One | 10.5281/zenodo.20328374 | Core conceptual paper |
| Q-PNA v2.0 | 10.5281/zenodo.20287742 | Neural architecture (encoder layer) |
| Language-Info-Architecture | 10.5281/zenodo.20137616 | Entropy gradient, mutual exclusion |
| Tree Cophenetic | 10.5281/zenodo.20213043 | Ultrametric inequality proof |

## Completed (Retained for Audit)

| ID | Task | Completed | Verification |
|:---|:-----|:----------|:-------------|
| S0 | Internal Literature Review | 2026-05-22 | **Test-Path:** `0.1.md` (53,983 bytes, 583 lines). Commit: `6b4380e`. Covers 35+ archived projects, 12 published papers, 6 GitHub repos. |
| S1 | Formal Definitions & Grounding | 2026-05-22 | **Test-Path:** `0.2.md` + `0.2.py`. Commit: `624b607`. 11 formal definitions, 2 theorems. Python verification: 22/22 ultrametric inequality, 22/22 triadic rigidity, language isomorphism PASS. |
| S2 | Sub-Graph Matching Search Spec | 2026-05-22 | **Test-Path:** `0.3.md` (20,946 bytes). Commit: `10a0ad2`. Three-tier matching criteria, RANK-AND-CLUSTER algorithm, Q-PNA integration, walked example. |
| S3 | Cross-Linguistic Examples | 2026-05-22 | **Test-Path:** `0.4.md`. Commit: `5575da8`. English, Turkish, Mohawk — isomorphic NSTs. Linearization algebra formalized. |
| S4 | Python Prototype | 2026-05-22 | **Test-Path:** `0.5.py` (560 lines). Commit: `e567b57`. Full pipeline: 5-doc corpus, 3-language search, 8/8 ultrametric, Type I/II matching, cluster detection. |

## Blocked

| ID | Task | Blocked By | Resolution |
|:---|:-----|:-----------|:-----------|
| — | — | — | — |

## Sprint Health

- Tasks completed: 5/7
- DoD verified: 5/7
- Blocked items: 0
- Retrospective filed: No

---
*Next: S1 — Formal Definitions & Grounding. SAY "WHAT'S NEXT? PROCEED" to continue.*
