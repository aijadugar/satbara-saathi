"""Evaluation harness – compare extraction against ground-truth JSON."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True)
    parser.add_argument("--threshold", type=float, default=0.85)
    args = parser.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"Fixtures dir not found: {fixtures}")
        sys.exit(1)

    print("Evaluation harness – add ground-truth JSON + images to run.")
    print(f"Threshold: {args.threshold}")


if __name__ == "__main__":
    main()
