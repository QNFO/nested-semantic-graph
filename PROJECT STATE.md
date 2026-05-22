# PROJECT STATE — Nested Semantic Graph

**Last Updated:** 2026-05-22
**Active Branch:** `feature/initial-setup`
**Current Phase:** P1 Planning (Initiation complete)

## What This Project Is

This project develops the **computational architecture** for sub-graph matching search on nested semantic graphs — the engineering sequel to the "Few Become One" conceptual paper (DOI: 10.5281/zenodo.20328374, published 2026-05-22). Where "Few Become One" argues *that* language is an ultrametric tree, this project specifies *how* to build search, ranking, and matching systems on that tree. The project bridges the published ultrametric-language framework with the Q-PNA neural architecture specification (DOI: 10.5281/zenodo.20287742) and the ultrametric-ai-poc GitHub implementation.

## Current Status

**Active task:** S2 — Sub-Graph Matching Search Spec
**Last completed:** S1 — Formal Definitions & Grounding (2026-05-22)
**Blocked?** No

### Due Diligence Results (2026-05-22, Third Pass)

#### Critical: 2026-05 Ultrametric-Language Publication Cluster
The user has produced an extensive body of published work (all with DOIs) in May 2026 that directly addresses the nested semantic graph concept:

| Paper | Date | DOI | Role |
|:------|:-----|:----|:-----|
| **Few Become One: Polysynthetic Communication and the Ultrametric Architecture of Language** | 2026-05-22 | 10.5281/zenodo.20328374 | **CORE PAPER** — Same concept as this project. Argues for nested ultrametric trees as cross-linguistic architecture. |
| **Language as Information Architecture** | 2026-05-12 | 10.5281/zenodo.20137616 | Quantitative foundation: entropy gradient, mutual exclusion principle |
| **Q-PNA Research Specification v2.0** | 2026-05-19 | 10.5281/zenodo.20287742 | Neural architecture: p-adic valuation encoding, ultrametric attention, token calculus |
| **The Tree at the Bottom of Thought** | 2026-05-21 | 10.5281/zenodo.20329583 | Synthesis: ultrametric branching across all domains including language |
| **The Tree Is Real** | 2026-05-21 | 10.5281/zenodo.20325850 | Computational validation: 649 triples, all ultrametric |
| **Convergence, Consilience** | 2026-05-20 | 10.5281/zenodo.20302276 | Meta-analysis of convergence/consilience as hierarchical signatures |
| **Ultrametric Geometry as Common Structure** | 2026-05-18 | 10.5281/zenodo.20265907 | Cross-domain: ultrametric trees in 5 domains |
| **Tree Distance Cophenetic** | 2026-05-15 | 10.5281/zenodo.20213043 | Mathematical formalization of cophenetic distance |
| **How Geometry Creates Memory** | 2026-05-06 | 10.5281/zenodo.20061155 | Threshold Principle: ultrametric containment |
| **TREE OF FREQUENCIES** | 2026-05-06 | 10.5281/zenodo.20049051 | Physical/computational tree |
| **Symmetry as a Grammatical Function** | 2026-05-08 | 10.5281/zenodo.20089746 | Symmetry emerging from grammatical constraints |

#### GitHub Repositories
| Repository | Purpose |
|:-----------|:--------|
| github.com/rwnq8/ultrametric-ai-poc | Working PoC for ultrametric AI |
| github.com/rwnq8/language-info-architecture | Language info architecture pipeline |
| github.com/rwnq8/quantum-laws-of-form | Distinction calculus implementation |
| github.com/rwnq8/verb-lexicon | Verb lexicon for semantic parsing |
| github.com/QNFO/Q-PNA | Q-PNA neural architecture |

#### Archived Projects (2025)
| Project | Relevance |
|:--------|:----------|
| **PILE OF BABEL** | Rosetta Stone architecture — common representation beneath diverse surface forms |
| **Semantic Observatory** | Semantic field concept, 5-layer stack |
| **Grammar of Interaction** | Graph formalism with "grammar" metaphors |

### Revised Project Positioning

**"Few Become One" IS the nested semantic graph paper — published today.** This project is therefore a **computational sequel**, not a new conceptual work. It focuses on:
1. The sub-graph matching search architecture (Section IV of "Few Become One" gestures at this but doesn't specify)
2. Python prototypes for semantic tree parsing, encoding, matching, and ranking
3. Connection to the Q-PNA neural architecture for the encoding layer
4. Operationalizing the theoretical framework into executable code

## Next Agent Handoff

1. Read SPRINT.md → identify active task
2. Read LEARNINGS.md → avoid past mistakes
3. Read the key prior papers (Few Become One, Q-PNA spec) for grounding
4. Execute task through Phase 0-5 pipeline
5. Update documentation and commit

## Constraints

| Constraint | Value |
|:-----------|:------|
| Write sandbox | `G:\My Drive\projects\nested-semantic-graph\` |
| Branch | `feature/initial-setup` |
| Merge target | `main` |
| Session limit | None |
| Version naming | `MAJOR.MINOR.ext` per §10 |
| Git discipline | Feature branches only, `-C` flag for project repo |

## Dependencies

| Dependency | Type | Status | Blocking? |
|:-----------|:-----|:-------|:----------|
| Few Become One (DOI: 10.5281/zenodo.20328374) | Input | Published | No — read-only |
| Q-PNA Spec (DOI: 10.5281/zenodo.20287742) | Input | Published | No — read-only |
| Language-Info-Architecture (DOI: 10.5281/zenodo.20137616) | Input | Published | No — read-only |
| Tree Cophenetic (DOI: 10.5281/zenodo.20213043) | Input | Published | No — read-only |
| ultrametric-ai-poc GitHub | Input | Published | No — read-only |
| AMR / UD literature | External | Not imported | No — secondary |

## Files Modified This Session

| File | Action | Status |
|:-----|:-------|:-------|
| `README.md` | CREATE → EDIT × 2 | Complete rewrite pending commit |
| `PROJECT STATE.md` | CREATE → EDIT × 2 | Major update pending commit |
| `SPRINT.md` | CREATE → EDIT | Scope adjusted pending commit |
| `CHANGELOG.md` | CREATE → EDIT | Updated pending commit |
| `BACKLOG.md` | CREATE | Committed |
| `LEARNINGS.md` | CREATE | Committed |
| `DECISIONS.md` | CREATE → EDIT | ADR-0003 added, more needed |

## Open Issues

- None — project scoping refined after due diligence.

## Active Risks

| Risk ID | Description | Status | Last Reviewed |
|:--------|:------------|:-------|:--------------|
| R1 | Gap between ultrametric physics formalism and linguistics application — mitigated by extensive published work bridging the gap | Mitigated | 2026-05-22 |
| R2 | External linguistics/AI literature not yet imported — mitigated by Language-Info-Architecture and Few Become One covering this ground | Mitigated | 2026-05-22 |
| R3 | Must correctly position project as computational sequel to Few Become One, not as novel conceptual work | Active | 2026-05-22 |

---

*Last updated: 2026-05-22*
