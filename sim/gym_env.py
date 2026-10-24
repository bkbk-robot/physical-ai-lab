#!/usr/bin/env python
"""sim/gym_env.py — SO-101 仿真训练环境（Gymnasium 接口）

任务：到达（reaching）——把夹爪末端移到目标方块上方。
为什么先做这个：它是"找块 → 走过去"的基础技能，也是验证训练链路是否可用的最小任务。

观测(12)：6 关节角 + 末端 xyz + 目标块 xyz
动作(3)：pan / lift / elbow 的角度增量（限幅 ±0.05 rad）
奖励：-距离（到目标上方 3cm 处），成功判定 < 2cm
"""
import os
os.environ.setdefault('MUJOCO_GL', 'egl')
import numpy as np
import mujoco
import gymnasium as gym
from gymnasium import spaces

SO101 = '/home/cloud-li/SO-ARM100/Simulation/SO101/so101_new_calib.xml'
BLOCK = 0.02


def _scene_xml(include_path, block_pos):
    bx, by = block_pos
    return f'''<mujoco model="reach"><include file="{include_path}"/>
<asset><material name="w" rgba="0.95 0.95 0.95 1"/></asset>
<worldbody>
  <light pos="0 0 2" dir="0 0 -1" directional="true"/>
  <geom name="desk" type="box" size="0.45 0.35 0.01" pos="0.18 0.02 -0.01" rgba="0.55 0.42 0.3 1"/>
  <body name="block0" pos="{bx:.4f} {by:.4f} {BLOCK}">
    <freejoint/><geom type="box" size="{BLOCK/2} {BLOCK/2} {BLOCK/2}" material="w" mass="0.02"/>
  </body>
</worldbody></mujoco>'''


class ReachEnv(gym.Env):
    metadata = {'render_modes': []}

    def __init__(self, seed=0, max_steps=120, randomize=True):
        super().__init__()
        self.max_steps = max_steps
        self.randomize = randomize
        self.rng = np.random.default_rng(seed)
        self.include = SO101
        self.scene_path = SO101.rsplit('/', 1)[0] + '/_gym_scene.xml'
        self.observation_space = spaces.Box(-np.inf, np.inf, (12,), dtype=np.float32)
        self.action_space = spaces.Box(-1.0, 1.0, (3,), dtype=np.float32)
        self.model = None
        self.data = None
        self.steps = 0
        self.block_pos = np.array([0.20, 0.0, BLOCK])

    # ---------- internal ----------
    def _load(self, block_pos):
        if self.model is None:                      # 只编译一次模型，reset 只重置状态
            with open(self.scene_path, 'w') as f:
                f.write(_scene_xml(self.include, (0.20, 0.0)))
            self.model = mujoco.MjModel.from_xml_path(self.scene_path)
            self.data = mujoco.MjData(self.model)
            self._bid = self.model.body('block0').id
            self._jid = int(self.model.body_jntadr[self._bid])
            self._bq = int(self.model.jnt_qposadr[self._jid])
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[self._bq:self._bq + 3] = [block_pos[0], block_pos[1], BLOCK]
        self.data.qpos[self._bq + 3:self._bq + 7] = [1, 0, 0, 0]
        self.block_pos = np.array(block_pos)
        for _ in range(60):
            mujoco.mj_step(self.model, self.data)

    def _obs(self):
        d = self.data
        tcp = d.site_xpos[self.model.site('gripperframe').id].copy()
        b = d.xpos[self.model.body('block0').id].copy()
        return np.concatenate([d.qpos[:6].copy(), tcp, b]).astype(np.float32)

    def _target(self):
        b = self.data.xpos[self.model.body('block0').id]
        return np.array([b[0], b[1], b[2] + 0.03])

    # ---------- gym API ----------
    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        if self.randomize:
            bx = self.rng.uniform(0.14, 0.26)
            by = self.rng.uniform(-0.10, 0.06)
        else:
            bx, by = 0.20, 0.0
        self._load((bx, by))
        self.steps = 0
        return self._obs(), {}

    def step(self, action):
        a = np.clip(action, -1, 1) * 0.05
        self.data.ctrl[0] = self.data.qpos[0] + a[0]
        self.data.ctrl[1] = self.data.qpos[1] + a[1]
        self.data.ctrl[2] = self.data.qpos[2] + a[2]
        self.data.ctrl[3] = self.data.qpos[3]
        self.data.ctrl[4] = self.data.qpos[4]
        self.data.ctrl[5] = self.data.qpos[5]
        for _ in range(4):                      # 每个动作 4 个物理步
            mujoco.mj_step(self.model, self.data)
        tcp = self.data.site_xpos[self.model.site('gripperframe').id]
        dist = float(np.linalg.norm(tcp - self._target()))
        reward = -dist
        self.steps += 1
        done = dist < 0.02
        trunc = self.steps >= self.max_steps
        if done:
            reward += 2.0
        return self._obs(), reward, bool(done), bool(trunc), {'dist': dist}

    def render(self):
        return None


if __name__ == '__main__':
    env = ReachEnv(seed=1)
    obs, _ = env.reset()
    print('obs dim:', obs.shape, '| action dim:', env.action_space.shape)
    tot = 0.0
    for i in range(50):
        obs, r, d, t, info = env.step(env.action_space.sample() * 0.5)
        tot += r
        if d or t:
            break
    print('随机策略 50 步累计奖励:', round(tot, 2), '| 最后距离(m):', round(info['dist'], 3))
