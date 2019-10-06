# pyphoon
ASCII Art Phase of the Moon (Python version)

![Screenshots](http://igor.chub.in/pyphoon/screenshot.png)

Based on the original version of Jef Poskanzer <jef@mail.acme.com> (Twitter: @jef_poskanzer) 
written in Pascal in 1979 (and later translated by himself into C, and now by me into Python).

# Usage

~~~~
$ pyphoon --help
usage: pyphoon [-h] [-n LINES] [-x] [-l [LANGUAGE]] [date]

Show Phase of the Moon

positional arguments:
  date                  Date for that the phase of the Moon must be shown.
                        Today by default

optional arguments:
  -h, --help            show this help message and exit
  -n LINES, --lines LINES
                        Number of lines to display (size of the moon)
  -x, --notext          Print no additional information, just the moon
  -l [LANGUAGE], --language [LANGUAGE]
                        locale for that the phase of the Moon must be shown.
                        English by default
~~~~

By default the number of lines is 30 and the date is today.

The Moon is (at the moment) shown only for the northern hemisphere.

Supported dateformats:

* 2016-Mar-01
* 2016-03-01
* 03-01-2016
* 03/01/2016
* etc.

Displayed information:

* time after the previous state (-)
* time to the next state (+)

# Dependencies

* dateutil

# Own changes

There are several changes in PyPhoon that were not present in the original Jef Pokazner's version of 1979:

* Localization: pyphoon is translated into many languages; language is configured using the system locale (`$LANG`)
