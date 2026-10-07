
#!/usr/bin/env python3
"""fireflavortax - price any food per 1,000 tasty calories.

Treats flavor as the thing you are actually buying. A pint of ice cream
and a sack of rice both cost money, but they deliver very different
amounts of the stuff you crave. This script prices them on the same
scale: dollars per 1,000 calories, then scales that by a flavor factor
you assign each food.

Usage:
    python3 fireflavortax.py FOOD PRICE SERVINGS CAL_PER_SERVING [FLAVOR]
    python3 fireflavortax.py --compare FILE

FOOD    name, quoted if it has spaces
PRICE   what you paid, in dollars
SERVINGS servings in the package (may be fractional)
CAL_PER_SERVING calories per serving, from the label
FLAVOR  optional 1-10 rating of how much you crave it (default 5)

With FLAVOR set, the price is also shown as a flavor-adjusted rate:
a 10/10 craving food at $2.00 costs the same per point as a 5/5 food
at $1.00. Use --compare with a CSV (name,price,servings,cal,flavor) to
rank a whole shopping list. Exit code 0 always; bad rows are reported,
not fatal, in compare mode.

Examples:
    python3 fireflavortax.py "Ice cream pint" 5.49 4 1000 9
    python3 fireflavortax.py "Brown rice 5lb" 8.99 50 320 3
    python3 fireflavortax.py --compare list.csv
"""
import csv
import sys


def flavor_rate(price, servings, cal, flavor):
    """Return (plain_rate, flavor_rate) in dollars per 1,000 calories.

    plain_rate: price / (total calories / 1000)
    flavor_rate: plain_rate * 5 / flavor, so a default 5/5 food is
    unchanged and a 10/10 craving halves the rate.

    >>> plain, fr = flavor_rate(5.49, 4, 1000, 9)
    >>> round(plain, 3)
    1.373
    >>> round(fr, 3)
    0.763
    >>> flavor_rate(4.0, 2, 2000, 5)[0]
    1.0
    >>> flavor_rate(4.0, 2, 2000, 10)[1]
    0.5
    """
    total_cal = servings * cal
    if total_cal <= 0:
        raise ValueError("calories must be positive")
    plain = price / (total_cal / 1000.0)
    flavor = max(1, min(10, flavor))
    return plain, plain * 5.0 / flavor


def main(argv):
    if len(argv) >= 2 and argv[1] == "--compare":
        if len(argv) < 3:
            print("usage: fireflavortax.py --compare FILE", file=sys.stderr)
            return 2
        rows = []
        with open(argv[2], newline="") as fh:
            for row in csv.reader(fh):
                if not row or row[0].startswith("#"):
                    continue
                try:
                    name, price, servings, cal, flavor = row[0], float(row[1]), float(row[2]), float(row[3]), int(float(row[4]))
                    plain, fr = flavor_rate(price, servings, cal, flavor)
                    rows.append((fr, plain, name))
                except (ValueError, IndexError) as exc:
                    print(f"skip {row!r}: {exc}", file=sys.stderr)
        rows.sort()
        for fr, plain, name in rows:
            print(f"{name}: ${plain:.2f}/1000cal, flavor-adjusted ${fr:.2f}")
        return 0

    if len(argv) < 5:
        print(__doc__, file=sys.stderr)
        return 2
    name = argv[1]
    price = float(argv[2])
    servings = float(argv[3])
    cal = float(argv[4])
    flavor = int(argv[5]) if len(argv) >= 6 else 5
    plain, fr = flavor_rate(price, servings, cal, flavor)
    print(f"{name}: ${plain:.2f} per 1,000 calories")
    if flavor != 5:
        print(f"  flavor {flavor}/10 -> flavor-adjusted ${fr:.2f} per 1,000 tasty calories")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
