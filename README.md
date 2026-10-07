# fireflavortax

Price any food per 1,000 tasty calories. One Python file, standard library only.

Ice cream and rice do not belong on the same dollars-per-calorie chart, because
cravings are part of what you are buying. Give each food a flavor rating from 1
to 10 and the script reports the plain rate plus a flavor-adjusted rate, so a
9/10 pint at $5.49 and a 3/10 sack of rice at $8.99 can be compared on one
number.

I run a FIRE math site and kept doing this arithmetic in a spreadsheet, so it
became a file. Method notes and the spending-fear piece live at
[FireNomics](https://firenomics.com).

## Usage

    python3 fireflavortax.py "Ice cream pint" 5.49 4 1000 9
    python3 fireflavortax.py "Brown rice 5lb" 8.99 50 320 3
    python3 fireflavortax.py --compare list.csv

Compare mode reads CSV rows of `name,price,servings,cal_per_serving,flavor`
and ranks the whole list by the flavor-adjusted rate.

## Why flavor

The plain dollars-per-1,000-calories rate says rice wins every time, which is
true and useless the moment you are standing in front of the freezer case. The
flavor factor just scales the rate: a 10/10 food counts half the rate of a 5/5
food at the same price. Pick the numbers honestly and the ranking tells you
which craving is actually the cheap one.

## License

MIT
