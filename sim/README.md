# sim — SO-101 simulation stack (working, reusable)

A separate system from the teleoperation data pipeline. Purpose: train and evaluate control
skills without the physical arm.

## Status
- MuJoCo 3.17, headless rendering (EGL) on RTX 5060 Ti
- Model: official `SO-ARM100/Simulation/SO101/so101_new_calib.xml`
- Scene: desk + randomized blocks + black tray + overhead camera
- Training: PPO (stable-baselines3) reaches ~1800 env-steps/s

## Files
| File | Purpose |
|---|---|
| `gym_env.py` | Gymnasium env: reaching task (6 joints + TCP + block -> delta joint actions) |
| `train_ppo.py` | PPO training with checkpoints every 50k steps |
| `eval_policy.py` | Success-rate evaluation (success = TCP within 2 cm of target) |

## Quick start
```bash
python sim/gym_env.py                      # smoke test
python sim/train_ppo.py 2000000            # ~18 min
python sim/eval_policy.py sim/models/ppo_reach.zip 50
```

## Measured so far
| Policy | Success (30 episodes) | Mean final distance |
|---|---|---|
| random | 0/30 | 20.7 cm |
| PPO 20k steps | 0/30 | 15.8 cm |

Learning is visible in the distance metric; the task needs longer training before success.

## Notes / limits
- The gripper in the official MJCF does not pinch (it rotates about its own axis). Grasping in sim
  therefore uses a simplified attach at the moment the jaws close. Documented, not hidden.
- Scene cameras are not yet calibrated against the physical setup; sim images are not used for
  vision policies yet.
- Physics: default MuJoCo parameters, no system identification against the real arm.
