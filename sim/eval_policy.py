#!/usr/bin/env python
"""sim/eval_policy.py — 评测 reaching 策略：成功=末端进入目标 2cm 内

用法: python sim/eval_policy.py <模型路径|random> [回合数=50]
"""
import os, sys
os.environ['MUJOCO_GL'] = 'egl'
sys.path.insert(0, '/home/cloud-li/.openclaw/workspace/sim')
import numpy as np
from gym_env import ReachEnv

path = sys.argv[1] if len(sys.argv) > 1 else 'random'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
model = None
if path != 'random':
    from stable_baselines3 import PPO
    model = PPO.load(path, device='cpu')

env = ReachEnv(seed=123, max_steps=120, randomize=True)
succ = 0
dists = []
for ep in range(n):
    obs, _ = env.reset(seed=1000 + ep)
    done = trunc = False
    info = {'dist': 9}
    while not (done or trunc):
        if model is None:
            a = env.action_space.sample()
        else:
            a, _ = model.predict(obs, deterministic=True)
        obs, r, done, trunc, info = env.step(a)
    dists.append(info['dist'])
    if info['dist'] < 0.02:
        succ += 1
print(f'{path}: 成功 {succ}/{n} ({succ/n*100:.0f}%) | 末距均值 {np.mean(dists)*100:.1f}cm 中位 {np.median(dists)*100:.1f}cm')
