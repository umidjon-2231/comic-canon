# Agents

Automation for the writing loop that is **not tied to any one AI tool**. The design is two
layers:

- **Deterministic core (Python, in `tools/`)** — retrieval and checking that must be exact:
  `pack.py` (assemble a scene's context) and `lint.py` (machine-checkable continuity rules).
  No model, no randomness.
- **Agents (portable prompt specs, here in `agents/`)** — the steps that need judgement, written
  as plain-Markdown role specs with a strict input/output contract. Each one is **model- and
  tool-agnostic**: paste it into any chat AI (Claude, GPT, Gemini, a local model), or wire it into
  any SDK/orchestrator. There is no Claude-Code-specific format here on purpose.

The agents call the deterministic tools instead of re-deriving facts in the prompt — so grounding
happens once, in code, and every model gets the same canon.

## The loop, automated

```
            ┌─────────────┐   context bundle   ┌────────────────┐   draft scene   ┌──────────────┐
  scene id →│  pack.py    │ ─────────────────► │ scene-drafter  │ ──────────────► │  lint.py +   │
            │ (tools/)    │                    │ (agents/)      │                 │  reviewer    │
            └─────────────┘                    └────────────────┘                 └──────┬───────┘
                                                                                          │ findings
                                                                              fix, then   ▼
                                                                                   ┌──────────────┐
                                                                          lock →   │ canon-keeper │  write state_changes back
                                                                                   └──────────────┘
```

## Roster

| Agent | Status | Consumes | Produces |
|-------|--------|----------|----------|
| [`scene-drafter`](./scene-drafter.md) | ✅ ready | `pack.py <id>` bundle | a drafted scene (panels + `state_changes`) |
| [`continuity-reviewer`](./continuity-reviewer.md) | ✅ ready | `pack.py <id> --review` + `lint.py` | E-coded findings for the rules the linter can't judge (R2/R5/R6/R7/R8/R11) |
| [`canon-keeper`](./canon-keeper.md) | ✅ ready | a locked scene's `state_changes` | edits to timeline / character logs / intervals / item state / ledger |

## How to run an agent with any AI

1. **Get the context:** `python tools/pack.py S01-007 --root path/to/story > bundle.md`
2. **Run the agent:** give the model the agent's spec (e.g. `agents/scene-drafter.md`) as its
   instructions and `bundle.md` as its input. In a chat UI that's two pastes; via an SDK it's a
   system prompt + a user message; in an orchestrator it's one node.
3. **Check the result:** save the draft into `scenes/`, then `python tools/lint.py path/to/story`
   and apply `continuity-reviewer` for the human-judgement rules.

The contract each agent declares (its **Inputs** and **Output** sections) is what makes it portable
— honor those and the surrounding tooling doesn't care which model produced the text.
