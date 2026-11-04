"""Command-line interface for local SENTINEL experiments."""
import argparse
import json

from sentinel.engine import DeceptionEngine, EngineConfig
from sentinel.experiments import compare_policies, to_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run bounded synthetic SENTINEL experiments"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="explore one synthetic deception graph")
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--steps", type=int, default=20)
    run.add_argument("--max-nodes", type=int, default=64)
    run.add_argument("--max-depth", type=int, default=8)
    run.add_argument("--branching-factor", type=int, default=3)
    run.add_argument("--policy", choices=("baseline", "adaptive"), default="baseline")

    compare = sub.add_parser(
        "compare", help="compare baseline and adaptive policies across seeds"
    )
    compare.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 27])
    compare.add_argument("--steps", type=int, default=20)
    compare.add_argument("--max-nodes", type=int, default=64)
    compare.add_argument("--max-depth", type=int, default=8)
    compare.add_argument("--branching-factor", type=int, default=3)
    compare.add_argument("--jsonl", action="store_true", help="emit JSON Lines records")

    args = parser.parse_args()
    if args.command == "run":
        result = DeceptionEngine(EngineConfig(
            seed=args.seed,
            max_steps=args.steps,
            max_nodes=args.max_nodes,
            max_depth=args.max_depth,
            branching_factor=args.branching_factor,
        )).run(policy=args.policy)
        print(json.dumps(result, indent=2))
        return

    result = compare_policies(
        args.seeds,
        max_nodes=args.max_nodes,
        max_depth=args.max_depth,
        max_steps=args.steps,
        branching_factor=args.branching_factor,
    )
    print(to_jsonl(result) if args.jsonl else json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
