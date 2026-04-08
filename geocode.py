#!/usr/bin/env python
import argparse
import sys
from pathlib import Path

# Prepend src/ so the geocode package is found before this script.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from geocode import GeocodeError, geocode


def main() -> None:
    parser = argparse.ArgumentParser(description="Geocode an address.")
    parser.add_argument("address", help="Address to geocode")
    args = parser.parse_args()

    try:
        lat, lon = geocode(args.address)
        print(f"({lat}, {lon})")
    except GeocodeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
