#!/usr/bin/env python
"""sim/train_ppo.py — 在仿真里训练 reaching 技能（PPO）

用法: python sim/train_ppo.py [总步数=500000] [保存前缀=sim/models/ppo_reach]
"""
import os, sys, time
os.environ['MUJOCO_GL'] = 'egl'
sys.path.insert(0, '/home/cloud-li/.openclaw/workspace')
sys.path.insert(0, '/home/cloud-li/.openclaw/workspace/sim')
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from gym_env import ReachEnv

steps = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
prefix = sys.argv[2] if len(sys.argv) > 2 else 'sim/models/ppo_reach'
os.makedirs(os.path.dirname(prefix), exist_ok=True)

env = ReachEnv(seed=0, max_steps=120, randomize=True)
model = PPO('MlpPolicy', env, verbose=1, n_steps=1024, batch_size=256,
            learning_rate=3e-4, gamma=0.95, ent_coef=0.005,
            policy_kwargs=dict(net_arch=[128, 128]), device='cuda',
            tensorboard_log=None)
cb = CheckpointCallback(save_freq=50_000, save_path=os.path.dirname(prefix),
                        name_prefix=os.path.basename(prefix))
t0 = time.time()
model.learn(total_timesteps=steps, callback=cb, log_interval=5)
model.save(prefix)
dt = time.time() - t0
print(f'训练完成: {steps} 步 / {dt:.0f}s ({steps/dt:.0f} 步/秒)')
