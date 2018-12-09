import argparse
import importlib


def main() -> None:
    parser = argparse.ArgumentParser(description="Run code for a day of AOC")
    parser.add_argument("day", type=int, choices=range(1, 26))
    parser.add_argument("-t", "--tests", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    module = "tests" if args.tests else "main"
    try:
        day_module = importlib.import_module(f"day{args.day:02}.{module}")
        if args.tests and args.verbose:
            day_module.run(verbose=True)  # type: ignore
        else:
            day_module.run()  # type: ignore
    except ModuleNotFoundError:
        if args.tests:
            print(f"No tests for day {args.day} !")
        else:
            print(f"Day {args.day} not implemented !")


if __name__ == "__main__":
    main()
