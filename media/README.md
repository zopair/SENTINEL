# SENTINEL cinematic explainer

This directory contains the source for the project's research explainer video.

## Rendering

The video is authored with Manim Community Edition (MIT) and FFmpeg. It uses no paid video API, hosted rendering service, or proprietary template.

Local setup (Python 3.11 recommended):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r media/requirements.txt
manim -pqh --fps 60 media/sentinel_explainer.py SentinelExplainer
```

For a faster draft, replace `-pqh` with `-pql`.

The GitHub Actions workflow `.github/workflows/render-explainer.yml` can render the same scene on demand and publish the MP4 as a workflow artifact. The rendered file is generated output; the Python scene remains the editable source of truth.

## Editorial and evidence rules

- All displayed counts, policy names, limits, and statistical methods must match the current repository implementation.
- The six policies are deterministic exploration policies, not six autonomous AI agents.
- The Adaptive policy is a hand-designed heuristic, not a trained model.
- The confidence interval is descriptive and normal-approximation based; permutation tests have assumptions.
- The lab's real-engine mode is local and loopback-bound to `127.0.0.1`.
- Do not imply that synthetic experiments prove real-world attacker diversion, production protection, permanent deception, or universal resistance.
- Keep the visual story focused on the research contribution: matched experiments, measurable behavior, explicit bounds, and reproducibility.

## Planned sequence

1. The problem: a decoy visit is not yet evidence of meaningful behavioral steering.
2. The synthetic labyrinth and six matched exploration policies.
3. Paired evidence: per-seed differences, descriptive intervals, sign-flip tests, and Holm adjustment.
4. Engineering discipline: resource ceilings and schema 2.0 telemetry.
5. Local research lab and the project’s evidence boundaries.
6. Closing identity: **SENTINEL — Don't just detect the path. Redesign the path.**


## Published visual assets

- `sentinel-visual.svg` is the lightweight hero illustration used by the project site and README.
- `SENTINEL-explainer.mp4` is the rendered 1080p/60fps explainer embedded on the GitHub Pages site. The render workflow refreshes this file from the editable Manim source.
