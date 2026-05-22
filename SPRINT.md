# Sprint Backlog — Sprint 1: Computational Architecture

**Sprint Goal:** Produce a first versioned draft and Python prototypes specifying the sub-graph matching search architecture — the computational sequel to "Few Become One."
**Started:** 2026-05-22
**Target End:** 2026-05-29
**Status:** Active

## Active Tasks

| ID | Task | DoD Criteria | Est. Effort | Status | Assignee |
|:---|:-----|:-------------|:------------|:-------|:---------|
| S0 | Revised Setup & Scope | DOCUMENTATION: All 7 docs updated reflecting the full due diligence (11 published papers, 5 GitHub repos, 3 archived projects). Project correctly positioned as computational sequel to "Few Become One." | 2h | [~] | Agent |
| S1 | Formal Definitions & Grounding | **Read** Few Become One §III-IV, Q-PNA §2-3, Tree Cophenetic §2. **Produce** LaTeX formalism for: nodes as conceptual primitives, edges as scope, ultrametric distance $d(x,y) = h(\text{LCA}(x,y))$, tree-alignment lattice for sub-graph matching. **Python** verify ultrametric property on example trees. | 3h | [ ] | Agent |
| S2 | Sub-Graph Matching Search Spec | Specify the search problem: query graph $G_q$, document graph corpus $\{G_d\}$, matching criteria (subgraph isomorphism, approximate matching), ranking via ultrametric graph distance. Connect to Q-PNA's token encoding as the parser front-end. | 2h | [ ] | Agent |
| S3 | Cross-Linguistic Examples | English "dog bit man yesterday" and Mohawk equivalent mapped to same semantic graph. Linearization rules for each language. Connect to Language-Info-Architecture's entropy gradient findings. | 2h | [ ] | Agent |
| S4 | Python Prototype: Graph Parser & Matcher | Parse example sentences to trees, implement brute-force subgraph isomorphism for small graphs, compute ultrametric graph distance for ranking. | 3h | [ ] | Agent |
| S5 | Computational Pathway | Component diagram connecting: morphological analyzer → semantic parser → graph encoder → index → query engine. Map to existing Q-PNA architecture. Feasibility assessment. | 2h | [ ] | Agent |
| S6 | Reader Testing & Revision | Blind reader test on v0.1.md (REVIEWER subagent). Address blocking/major issues. | 2h | [ ] | Agent |

## Key Prior Work to Reference

| Paper | DOI | Section to Reference |
|:------|:----|:---------------------|
| Few Become One | 10.5281/zenodo.20328374 | All — the foundation |
| Q-PNA v2.0 | 10.5281/zenodo.20287742 | §2 (math), §3 (architecture), §5 (token calculus) |
| Language-Info-Architecture | 10.5281/zenodo.20137616 | Mutual exclusion, entropy gradient |
| Tree Cophenetic | 10.5281/zenodo.20213043 | §2 (ultrametric inequality proof) |
| How Geometry Creates Memory | 10.5281/zenodo.20061155 | §5 (Threshold Principle) |

## Completed (Retained for Audit)

| ID | Task | Completed | Verification |
|:---|:-----|:----------|:-------------|
| — | — | — | — |

## Blocked

| ID | Task | Blocked By | Resolution |
|:---|:-----|:-----------|:-----------|
| — | — | — | — |

## Sprint Health

- Tasks completed: 0/7
- DoD verified: 0/7
- Blocked items: 0
- Retrospective filed: No

---
*Updated after third-pass due diligence. Project repositioned as computational sequel.*
