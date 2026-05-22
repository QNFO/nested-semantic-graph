# Product Backlog — Nested Semantic Graph

**Last Updated:** 2026-05-22

## Priority Legend

| Priority | Meaning | When |
|:---------|:--------|:-----|
| **P0** | Must have now | Current or next sprint |
| **P1** | Should have soon | Within 3 sprints |
| **P2** | Could have later | Nice-to-have, not committed |
| **P3** | Won't have now | Deferred or rejected |

## Backlog

| Priority | Item | Description | Est. Effort | Dependencies | Status |
|:---------|:-----|:------------|:------------|:-------------|:-------|
| P0 | S5: Python Prototype: Graph Parser & Matcher | Parse sentences to trees, brute-force subgraph isomorphism, ultrametric ranking | 3h | S1, S3, S4 | Not Started |
| P0 | S6: Computational Pathway | Component diagram, feasibility assessment, Q-PNA interface mapping | 2h | S4, S5 | Not Started |
| P0 | S7: Reader Testing & Revision | Blind reader test, address issues, polish | 2h | All above | Not Started |
| P1 | Morphological Analyzer Survey | Survey existing tools for Inuktitut, Cree, Mohawk, Turkish | 3h | S3 | Not Started |
| P1 | Python Prototype: Graph Parser | Full parser that converts example sentences to graphs | 4h | S5 | Not Started |
| P1 | Python Prototype: Sub-Graph Matcher | Full subgraph isomorphism for larger graphs | 4h | S5 | Not Started |
| P2 | Cross-Linguistic Corpus | Collect parallel texts in English + polysynthetic languages | 8h | S3 | Not Started |
| P2 | Evaluation Framework | Define precision/recall metrics for sub-graph search | 3h | S5 | Not Started |
| P2 | Visualization Tool | Interactive tree viewer for nested semantic graphs | 5h | S1 | Not Started |
| P3 | Full-Scale Implementation | Production search engine on nested semantic graphs | 100h+ | All P1 | Not Started |
| P3 | Neural Semantic Parser | Train or fine-tune a parser for the common representation | 100h+ | P2 | Not Started |

## Completed (Retained for Audit)

| Priority | Item | Deliverable | Completed | Notes |
|:---------|:-----|:------------|:----------|:------|
| P0 | S0: Project Setup | 7 mandatory docs, git repo, due diligence | 2026-05-22 | Commits 38f119e through f0b5ab7 |
| P0 | S1: Formal Definitions | 0.2.md + 0.2.py | 2026-05-22 | 11 definitions, 2 theorems, 22/22 ultrametric verified |
| P0 | S2: Literature Grounding | 0.1.md Internal Literature Review | 2026-05-22 | 35+ archived projects, 12 papers, 6 GitHub repos |
| P0 | S3: Cross-Linguistic Examples | 0.4.md | 2026-05-22 | English, Turkish, Mohawk — isomorphic NSTs |
| P0 | S4: Search Architecture Spec | 0.3.md Sub-Graph Matching Search Spec | 2026-05-22 | Three-tier matching, RANK-AND-CLUSTER, Q-PNA pipeline |

---
*Last updated: 2026-05-22 (S0-S4 complete, S5 next)*
