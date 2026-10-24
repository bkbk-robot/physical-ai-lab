# How We Work — a human + AI engineering loop

> Scope: **engineering collaboration only.** This document describes how a one-person lab and its AI
> agent divide work, verify claims, and measure progress. It deliberately contains no personal notes,
> no credentials, and no internal infrastructure details.

## Roles

| Layer | Human | AI agent |
|---|---|---|
| Direction | chooses the problem, the trade-offs, the deadline | proposes options with cost/risk, never decides alone |
| Physical world | places objects, powers hardware, watches the arm | scripts motion, parses sensors, flags anomalies |
| Model work | defines what "working" means | trains, evaluates, writes the tooling |
| Acceptance | final judgement (eyes on the robot) | supplies the numbers that make judgement cheap |

## Verification protocol

1. **No claim without a number.** "Better" is not accepted; a metric or a log line is.
2. **Reproduce before believing.** Every result must be re-runnable from a documented command.
3. **Instrument first.** When a metric is missing, the next task is building the instrument, not guessing.
4. **Cross-check sources.** Log values are compared against raw state where possible; a mismatch means
   the parser is wrong before it means the model is wrong.

## Change discipline

- Back up working code before modifying it; keep a one-command rollback.
- One variable per experiment; if two things change, the result cannot be attributed.
- Roadmap decisions get written down, then executed; they are not re-litigated mid-run.
- Fixed launch procedure for every physical test: preflight checks, reset, capture before/after evidence.

## Growth metric

Progress is plotted, not narrated:

- success rate per iteration (objects placed / objects present)
- time-to-completion per run
- number of failure modes eliminated (with the instrument that detects each one)

A flat curve is treated as information, not as a reason to tweak parameters.

## Boundaries

- Safety-relevant actions stay with the human (power, workspace, motion limits).
- Credentials never enter shared channels or public repositories.
- The agent may propose; the human commits.

## Case notes (what the loop actually catches)

**1. A parser bug that looked like a model failure.** Per-joint action ranges were read from a log column
order that did not match the print order, producing a confident but wrong diagnosis ("the arm is
extrapolating far outside the training range"). Cross-checking the same log against raw state values
showed the arm had stayed inside the demonstrated range the whole time. Fix: print with explicit labels.

**2. A hardware fault masked as a policy problem.** Several "the policy cannot grasp" runs were measured
while one or two servos were intermittently dropping off the serial bus. A six-motor preflight check now
runs before every trial, so a bad arm can no longer be mistaken for a bad model.

**3. A configuration default that silently blocks learning.** The default fine-tune keeps the
vision-language backbone frozen (`train_expert_only=true`). This is invisible in the training logs but
explains why the policy grounds objects only where they appeared during data collection. The finding came
from reading the checkpoint config rather than re-tuning hyperparameters.

Each case follows the same pattern: **the human suspects the story is wrong, the agent produces the
measurement that settles it.**
