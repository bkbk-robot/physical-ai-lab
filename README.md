## Status

| Date | Capability | Success (objects in tray) | Next |
|---|---|---|---|
| 2026-10-24 | pick-and-place inside demonstrated workspace | baseline recorded (0-1 / 3 per run) | evaluate VLM-unfrozen checkpoint |

# Physical AI Lab Notes

Daily, reproducible notes from a one-person physical-AI lab: fine-tuning vision-language-action
models on a real 6-DoF arm (SO-101), and documenting **what fails and why**.

## What is here
- `logs/YYYY-MM-DD.md` — one entry per working day: config, loss, success rate, failure attribution
- `bench/` — objective evaluation tooling (no "feels better", only numbers)
- `issues/` — upstream bug reports filed from this work

## Philosophy
Every claim in these logs is paired with a number and a way to reproduce it.
Negative results are published, because they are the expensive part.
