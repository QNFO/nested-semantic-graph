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
| P0 | S2.3: Enhanced Corpus | Expand from 5 to 15+ documents, add 2 more languages | 2h | S2.2 | Not Started |
| P0 | S2.4: Turkish in 0.2.py | Add Turkish tree to formal verification suite | 1h | — | Not Started |
| P0 | S2.5: Publication Polish | 0.7.md: abstract, author block, YAML, curly quotes, Language Gate | 2h | All above | Not Started |
| P0 | S2.6: Reader Testing Round 2 | Second blind reader test per §11.5 CPL L27 | 1h | S2.5 | Not Started |
| P1 | Python Prototype: Graph Parser | Full parser that converts example sentences to graphs from morphological output | 4h | S2.2 | Not Started |
| P1 | Python Prototype: Sub-Graph Matcher | Full subgraph isomorphism for larger graphs (100+ nodes) | 4h | S2.1 | Not Started |
| P2 | Cross-Linguistic Corpus | Collect parallel texts in English + polysynthetic languages | 8h | S2.2 | Not Started |
| P2 | Evaluation Framework | Define precision/recall metrics for sub-graph search | 3h | S2.1 | Not Started |
| P2 | Visualization Tool | Interactive tree viewer for nested semantic graphs | 5h | S1 | Not Started |
| P3 | Full-Scale Implementation | Production search engine on nested semantic graphs | 100h+ | All P1 | Not Started |
| P3 | Neural Semantic Parser | Train or fine-tune a parser for the common representation | 100h+ | P2 | Not Started |

## Completed (Retained for Audit)

| Priority | Item | Deliverable | Completed | Notes |
|:---------|:-----|:------------|:----------|:------|
| P0 | Sprint 1 (S0-S6) | 0.1.md through 0.7.md, 0.2.py, 0.5.py | 2026-05-22 | 7 tasks, 8 content files, 14 commits |
| P0 | S2.1: Type III Matching | 0.8.py (272 lines) | 2026-05-22 | Zhang-Shasha DP. Pipeline: I/II/III fallback. |
| P0 | S2.2: Morphological Survey | 0.8.md | 2026-05-22 | English→Mohawk. Mohawk FST gap identified. |

---
*Last updated: 2026-05-22 (Sprint 2: 2/7 complete)*
