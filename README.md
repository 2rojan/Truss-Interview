# Truss Interview



This script parses through an input csv file and provides output to stdout

## Functionality Implemented:
Timestamp to US/Eastern
ZipCodes 5 digits, leading 0's
Name Column Converted to UpperCase.
FooDuration and BarDuration columns converted to seconds w/float
Total column is sum of FooDuration and BarDuration columns

## Directions:

Clone this repo.

Requirements:
Python3
pandas 
```
pip install pandas
```

Run this app as follows:
```
python norm.py < ../sample.csv > ../out.csv
```