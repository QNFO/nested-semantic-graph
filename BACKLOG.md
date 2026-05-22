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
| P0 | S0: Project Setup & Initial Draft | Create all docs, produce v0.1 first draft | 2h | None | In Progress |
| P0 | S1: Formal Definitions | LaTeX formalism for nodes, edges, ultrametric distance | 3h | S0 | Not Started |
| P0 | S2: Literature Grounding | Import and connect AMR, UD, dependency grammar literature | 2h | S0 | Not Started |
| P0 | S3: Linguistic Examples | English/Mohawk/Turkish mapped to same graph | 2h | S1, S2 | Not Started |
| P0 | S4: Sub-Graph Matching Search | Formal spec of search problem and ranking metric | 2h | S1 | Not Started |
| P0 | S5: Computational Pathway | Component diagram and feasibility assessment | 2h | S1, S2 | Not Started |
| P0 | S6: Reader Testing & Revision | Blind reader test and polish for publication | 2h | S3, S4, S5 | Not Started |
| P1 | Morphological Analyzer Survey | Survey existing tools for Inuktitut, Cree, Mohawk, Turkish | 3h | S2 | Not Started |
| P1 | Python Prototype: Graph Parser | Minimal parser that converts example sentences to graphs | 4h | S3 | Not Started |
| P1 | Python Prototype: Ultrametric Distance | Implement ultrametric distance on graph-alignment lattice | 3h | S1 | Not Started |
| P1 | Python Prototype: Sub-Graph Matcher | Brute-force subgraph isomorphism for small graphs | 4h | S4 | Not Started |
| P2 | Cross-Linguistic Corpus | Collect parallel texts in English + polysynthetic languages | 8h | S3 | Not Started |
| P2 | Evaluation Framework | Define precision/recall metrics for sub-graph search | 3h | S4 | Not Started |
| P2 | Visualization Tool | Interactive tree viewer for nested semantic graphs | 5h | S1 | Not Started |
| P3 | Full-Scale Implementation | Production search engine on nested semantic graphs | 100h+ | All P1 | Not Started |
| P3 | Neural Semantic Parser | Train or fine-tune a parser for the common representation | 100h+ | P2 | Not Started |

## Completed (Retained for Audit)

| Priority | Item | Completed | Notes |
|:---------|:-----|:----------|:------|
| — | — | — | — |

---
*Generated from PRODUCT-BACKLOG-TEMPLATE.md v1.0*
