from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Training entrypoint for modern Graph2Plan stack")
    parser.add_argument("--dataset", type=str, required=True, help="Path to canonical dataset")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("[stub] training bootstrap")
    print(
        f"dataset={args.dataset} epochs={args.epochs} batch_size={args.batch_size} lr={args.lr}"
    )


if __name__ == "__main__":
    main()
