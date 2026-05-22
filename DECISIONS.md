# Architecture Decision Records — Nested Semantic Graph

---

# ADR-0001: Use Ultrametric Tree as the Fundamental Data Structure

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

The ultrametric tree is the established data structure across the 2026-05 publication cluster: "Few Become One" uses it for cross-linguistic semantics, Q-PNA uses Bruhat-Tits trees for neural encoding, Tree Cophenetic formalizes cophenetic distance, and "The Tree Is Real" validates the structure computationally. The decision is to adopt this as the project's representation.

## Decision

We will use rooted trees as the fundamental data structure for semantic representation, with the ultrametric distance defined as the height of the lowest common ancestor: $d(x,y) = h(\text{LCA}(x,y))$, satisfying the strong triangle condition $d(x,z) \leq \max\{d(x,y), d(y,z)\}$. This follows Tree Cophenetic §2.

## Consequences

### What Becomes Easier
- Direct connection to the entire 2026-05 ultrametric publication cluster — same mathematics
- Q-PNA and ultrametric-ai-poc provide working implementations to build on
- Ultrametric distance computation is $O(\log n)$ with LCA data structures

### What Becomes Harder
- Non-hierarchical semantic relationships require auxiliary structures

### Risks Accepted
- As documented in Tree Cophenetic §7, the tree constraint may force representational choices

---

# ADR-0002: Versioned File Naming for All Content Files

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

Per Section 10 of the system prompt. The 7 mandatory documentation files are exempt.

## Decision

All content files use `MAJOR.MINOR[.PATCH].ext` naming. Publication-ready documents use descriptive filenames (per §11.1).

---

# ADR-0003: Explicitly Connect NSG to PILE OF BABEL's Rosetta Stone Architecture

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

PILE OF BABEL (2025-10) pioneered the "common representation beneath diverse surface forms" architecture — the Rosetta Stone / Crosswalk Mandate pattern. PILE OF BABEL maps physics jargon to circle/integer primitives; NSG maps natural languages to nested semantic graphs. Both are instances of the same architectural pattern.

## Decision

We will explicitly position the NSG as a linguistic instantiation of the Rosetta Stone architecture, acknowledging PILE OF BABEL as precedent. The Crosswalk Mandate ("Actively seek to identify and unify underlying concepts, even if they are presented with different terminology across domains") is adopted as a design principle.

---

# ADR-0004: Position Project as Computational Sequel to "Few Become One"

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

Due diligence discovered that "Few Become One: Polysynthetic Communication and the Ultrametric Architecture of Language" (DOI: 10.5281/zenodo.20328374, published 2026-05-22) IS the core conceptual paper on the nested semantic graph for cross-linguistic semantics — published on the same date this project was initiated. This means the project is not producing a novel conceptual argument from scratch; the conceptual foundation is already published.

## Decision

This project will be positioned as the **computational implementation sequel** to "Few Become One." The first versioned draft (0.1.md) will:
1. Cite "Few Become One" as the conceptual foundation (DOI: 10.5281/zenodo.20328374)
2. Focus on the sub-graph matching search architecture (Section IV of "Few Become One" gestures at this)
3. Provide Python prototypes: semantic tree parser, subgraph matcher, ultrametric ranking engine
4. Connect to the Q-PNA neural architecture (DOI: 10.5281/zenodo.20287742) for the encoding layer
5. Reference Language-Info-Architecture (DOI: 10.5281/zenodo.20137616) for quantitative grounding

## Consequences

### What Becomes Easier
- Don't need to re-establish the linguistic argument — it's done
- Can focus entirely on the engineering: algorithms, data structures, prototypes
- The publication can be shorter and more focused

### What Becomes Harder
- Must avoid redundancy with "Few Become One" while still being self-contained
- Must carefully articulate what is novel (search architecture) vs. what is established (tree representation)

### Risks Accepted
- The project's contribution may be seen as incremental rather than foundational — mitigated by making the computational architecture genuinely novel

---

*Generated from ADR-TEMPLATE.md v1.0.*
