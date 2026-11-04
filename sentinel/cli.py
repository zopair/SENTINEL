"""Command-line interface for local SENTINEL experiments."""
import argparse
import json

from sentinel.deception import AdaptiveLabyrinth, LabyrinthConfig
from sentinel.deception_lab import evaluate_profiles
from sentinel.engine import DeceptionEngine, EngineConfig
from sentinel.experiments import compare_policies, to_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Run bounded synthetic SENTINEL experiments")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="explore one synthetic deception graph")
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--steps", type=int, default=20)
    run.add_argument("--max-nodes", type=int, default=64)
    run.add_argument("--max-depth", type=int, default=8)
    run.add_argument("--branching-factor", type=int, default=3)
    run.add_argument("--policy", choices=("baseline", "adaptive"), default="baseline")

    labyrinth = sub.add_parser("labyrinth", help="run an adaptive synthetic labyrinth session")
    labyrinth.add_argument("--seed", type=int, default=7)
    labyrinth.add_argument("--steps", type=int, default=20)
    labyrinth.add_argument("--max-nodes", type=int, default=64)
    labyrinth.add_argument("--max-depth", type=int, default=8)
    labyrinth.add_argument("--branching-factor", type=int, default=3)
    labyrinth.add_argument("--actions", nargs="+",
        choices=("inspect", "follow", "enumerate", "verify", "collect", "wait"),
        default=["inspect", "follow", "verify", "enumerate"])

    profiles = sub.add_parser("profiles", help="evaluate scripted synthetic agent strategies")
    profiles.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 27])
    profiles.add_argument("--steps", type=int, default=12)
    profiles.add_argument("--max-nodes", type=int, default=64)
    profiles.add_argument("--max-depth", type=int, default=8)

    compare = sub.add_parser("compare", help="compare baseline and adaptive policies")
    compare.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 27])
    compare.add_argument("--steps", type=int, default=20)
    compare.add_argument("--max-nodes", type=int, default=64)
    compare.add_argument("--max-depth", type=int, default=8)
    compare.add_argument("--branching-factor", type=int, default=3)
    compare.add_argument("--jsonl", action="store_true")

    args = parser.parse_args()
    if args.command == "run":
        result = DeceptionEngine(EngineConfig(
            seed=args.seed, max_steps=args.steps, max_nodes=args.max_nodes,
            max_depth=args.max_depth, branching_factor=args.branching_factor,
        )).run(policy=args.policy)
    elif args.command == "labyrinth":
        result = AdaptiveLabyrinth(LabyrinthConfig(
            seed=args.seed, max_steps=args.steps, max_nodes=args.max_nodes,
            max_depth=args.max_depth, branching_factor=args.branching_factor,
        )).run(args.actions)
    elif args.command == "profiles":
        result = evaluate_profiles(
            args.seeds, max_nodes=args.max_nodes, max_depth=args.max_depth,
            max_steps=args.steps,
        )
    else:
        result = compare_policies(
            args.seeds, max_nodes=args.max_nodes, max_depth=args.max_depth,
            max_steps=args.steps, branching_factor=args.branching_factor,
        )
    if args.command == "compare" and args.jsonl:
        print(to_jsonl(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
