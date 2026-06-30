---
name: Continuity rule proposal
about: Propose a new or changed continuity rule that catches a scenario error
title: "[rule] "
labels: rules
---

<!-- Remember the three-views contract: a rule (R#), the error it catches (E#), and any schema
     constraint are three views of the same thing. Address all three below. -->

## The scenario error it catches

<!-- What goes wrong in a story if this rule doesn't exist? Map it to an existing error code
     in CHEATSHEET.md §2 (E1–E12), or propose a new E# and describe it. -->

## The rule

<!-- State it in R# style, like the entries in validation/continuity-rules.md.
     e.g. "R13 · <name> (E##) — <what must hold>." -->

## How a linter could check it

- [ ] **Machine-checkable** — describe the check (which fields/files it reads, what it compares).
- [ ] **Manual only** — explain why it can't be automated (yet).

## Schema / doc changes this implies

<!-- Which schema/*.json, validation/continuity-rules.md, and CHEATSHEET.md §2 edits would land
     alongside this rule to keep the three views in sync? -->
