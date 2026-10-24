# bench - objective evaluation

No subjective judgement: an overhead camera counts how many objects sit inside the tray.

## Files
- `score_scene.py` - captures the overhead view, returns `(in_tray, on_desk)`
  - fixed ROI for tray and desk (camera is static)
  - no reference frame required, robust to lighting changes
- `bench.py` - runs N trials, scores before/after each, writes `results.json`

## Metric
`gained = after_tray - before_tray` per trial; success rate = mean gained over trials.

## Usage
    python score_scene.py                 # current counts
    python bench.py <ckpt_dir> 3 150      # 3 trials x 150 s

## Why this exists
Open-loop action error was a poor predictor of real performance here: the checkpoint with the lowest
offline error was not the one that grasped best. Counting objects in the tray was the only metric that
matched observations on the robot.
