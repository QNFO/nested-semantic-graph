# Architecture Decision Records — Nested Semantic Graph

---

# ADR-0001: Use Ultrametric Tree as the Fundamental Data Structure

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

The user's proposal defines the nested semantic graph as a tree of conceptual primitives where distance between nodes satisfies the strong triangle condition (ultrametric property). Alternative representations were considered: flat feature vectors (standard in NLP), directed acyclic graphs (more general than trees), or general graphs without hierarchical constraints.

The user's existing corpus contains extensive work on ultrametric physics (2026-02 through 2026-05), establishing ultrametric trees as a unifying geometric object in quantum gravity, fault tolerance, and spacetime. Using the same formalism for linguistics creates a bridge between these domains.

## Decision

We will use rooted trees as the fundamental data structure for semantic representation, with the ultrametric distance defined as the height of the lowest common ancestor: $d(x,y) = \text{height}(\text{LCA}(x,y))$. This satisfies:

$$d(x,z) \leq \max\{d(x,y), d(y,z)\}$$

The tree is the canonical form. Graphs that appear non-tree-like (e.g., when a concept modifies multiple parents) will be resolved into trees by duplication or by selecting a primary attachment, with cross-references handled as a secondary indexing layer.

## Consequences

### What Becomes Easier
- Direct connection to the existing ultrametric physics corpus — same mathematics, different domain
- Ultrametric distance computation is $O(\log n)$ with appropriate LCA data structures
- Tree edit distance and tree alignment have well-studied algorithms
- The strong triangle condition guarantees metric properties that simplify clustering and ranking

### What Becomes Harder
- Representing non-hierarchical semantic relationships (e.g., coreference across branches, symmetric relations)
- Some linguistic phenomena (control structures, long-distance dependencies) require tree-to-tree mappings rather than simple subtree matching
- The tree constraint may force representational choices that are not universally agreed upon in linguistics

### Risks Accepted
- We accept that some semantic relationships will require auxiliary structures beyond the primary tree
- We accept that the choice between competing tree representations for the same sentence is a research question to be addressed, not a solved problem

---

# ADR-0002: Versioned File Naming for All Content Files

**Status:** Accepted
**Date:** 2026-05-22
**Supersedes:** None
**Superseded by:** None

## Context

Per Section 10 of the system prompt, all content/output files must use versioned filenames (`MAJOR.MINOR.ext`). This ensures chronological audit trail and provenance. The 7 mandatory documentation files are exempt per §10.2 Rule 0.

## Decision

All content files (drafts, code, data, figures) will use `MAJOR.MINOR[.PATCH].ext` naming:
- First draft: `0.1.md`
- Supporting Python: `0.1.py`
- Publication-ready documents use descriptive filenames (per §11.1) when moved to releases

## Consequences

### What Becomes Easier
- Full audit trail from git log + version numbers
- Trivial cross-referencing between document and its supporting code/data
- No namespace collisions from descriptive names

### What Becomes Harder
- Must run Python scan before creating any new file to determine next version
- Descriptive filenames only appear at publication time

### Risks Accepted
- Version numbers alone don't convey content — mitigated by README.md and CHANGELOG.md

---

*Generated from ADR-TEMPLATE.md v1.0. For index, see docs/adr/README.md*
