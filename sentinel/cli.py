"""Command-line interface for local SENTINEL experiments."""
import argparse
import json

from sentinel.engine import DeceptionEngine, EngineConfig


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a bounded synthetic SENTINEL experiment")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="explore a synthetic deception graph")
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--steps", type=int, default=20)
    run.add_argument("--max-nodes", type=int, default=64)
    run.add_argument("--max-depth", type=int, default=8)
    run.add_argument("--branching-factor", type=int, default=3)
    args = parser.parse_args()
    result = DeceptionEngine(EngineConfig(
        seed=args.seed, max_steps=args.steps, max_nodes=args.max_nodes,
        max_depth=args.max_depth, branching_factor=args.branching_factor,
    )).run()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
