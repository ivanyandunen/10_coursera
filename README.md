# Coursera Dump

This script gets 20 random links from Coursera's list of courses
[here](https://www.coursera.org/sitemap~www~courses.xml).
Then it collects info about each course (Name, language, date of the beginning, duration and rating)
and save them. It saves to an Excel file 'courses_info.xlsx' in the same 
directory by default or in an xlsx file specified by user with -o(--outfile)
parameter.

# How to run

Python 3 has to be installed and modules from requirements.txt
You might have to run python3 instead of python depending on system.

```commandline
python coursera.py
python coursera.py -h
usage: coursera.py [-h] [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -o, --outfile OUTFILE
                        Path to xlsx file with information about
                        courses.Without it file will be saved to current
                        directory as courses_info.xlsx
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
