# How We Work — a human + AI engineering loop

> Scope: engineering collaboration only. This document describes how a one-person lab and its AI agent
> divide work, check claims, and track progress. It contains no personal notes, no credentials, and no
> internal infrastructure details.

## Roles

| Layer | Human | AI agent |
|---|---|---|
| Direction | chooses the problem, trade-offs, deadline | proposes options with cost and risk |
| Physical world | places objects, powers hardware, observes the arm | scripts motion, parses sensors, flags anomalies |
| Model work | defines what "working" means | trains, evaluates, writes tooling |
| Acceptance | final judgement on the robot | supplies numbers that make judgement cheap |

## Checking protocol

1. No conclusion without a number; "better" is not accepted as a result.
2. Results must be re-runnable from a documented command.
3. When a metric is missing, building the instrument comes before drawing conclusions.
4. Log values are cross-checked against raw state; a mismatch indicates a parsing problem before a model problem.

## Change discipline

- Working code is backed up before modification, with a one-command rollback.
- One variable per experiment; two simultaneous changes make the result unattributable.
- Physical tests follow a fixed procedure: preflight checks, reset, before/after evidence.

## Progress measure

- success rate per iteration (objects placed / objects present)
- time to completion per run
- list of failure modes eliminated, with the instrument that detects each one

A flat curve is recorded as information rather than followed by parameter changes.

## Boundaries

- Safety-relevant actions stay with the human (power, workspace, motion limits).
- Credentials are not stored in shared channels or public repositories.
- The agent proposes; the human decides.

## Case notes

**1. Log column order.** Per-joint action ranges were read with a column order that did not match the
print order. The resulting diagnosis (motion far outside the training range) was incorrect; comparing the
same log against raw state values showed the arm had stayed inside the demonstrated range. Log output was
changed to labelled columns.

**2. Servo dropouts.** Some evaluation runs took place while one or two servos were intermittently
dropping off the serial bus, which affected the measurements. A six-motor preflight check now runs before
each trial.

**3. Backbone training flag.** The default fine-tune keeps the vision-language backbone frozen
(`train_expert_only=true`). This does not appear in training logs but is consistent with the policy
grounding objects only where they appeared during data collection. The setting was found by reading the
checkpoint config.
