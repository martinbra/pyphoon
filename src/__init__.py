#!/usr/bin/env python
"""
pyphoon - Phase of the Moon (Python version)
Igor Chubin <igor@chub.in>, 05.03.2016,

Based on the original version of Jef Poskanzer <jef@mail.acme.com>
written in Pascal in 1979 (and later translated to C)
"""


import sys
import os
import argparse
import datetime
import time
import locale
from math import cos, sqrt
import dateutil.parser


# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
# sys.path.append((os.path.dirname(os.path.dirname(__file__))))
from src.lib.astro import unix_to_julian, phase, phasehunt2
from src.lib.moons import background6, background18, background19, background21, background22, background23
from src.lib.moons import background24, background29, background32
from src.lib.rotate import rotate
from src.lib.translations import LITS

def fatal(message):
    """ Print error message and exit signaling failure
    """
    print(message, file=sys.stderr)
    sys.exit(1)

#
# Global defines and declarations.
#
SECSPERMINUTE = 60
SECSPERHOUR = (60 * SECSPERMINUTE)
SECSPERDAY = (24 * SECSPERHOUR)

PI = 3.1415926535897932384626433

DEFAULTNUMLINES = 23
DEFAULTNOTEXT = False
DEFAULTHEMISPHERE = 'north'

QUARTERLITLEN = 16
QUARTERLITLENPLUSONE = 17

# If you change the aspect ratio, the canned backgrounds won't work.
ASPECTRATIO = 0.5

def putseconds(secs):
    """ Create a datestring for format 'dd HH:MM:SS'
    """
    days = int(secs / SECSPERDAY)
    secs = int(secs - days * SECSPERDAY)
    hours = int(secs / SECSPERHOUR)
    secs = int(secs - hours * SECSPERHOUR)
    minutes = int(secs / SECSPERMINUTE)
    secs = int(secs - minutes * SECSPERMINUTE)

    return f"{days:d} {hours:2d}:{minutes:02d}:{secs:02d}"

def putmoon(datetimeobj, numlines, atfiller, notext, lang, hemisphere):  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """ Print the moon
    """
    output = [""]
    def putchar(char):
        output[0] += char
    def fputs(string):
        output[0] += string

    if not lang:
        try:
            lang = locale.getdefaultlocale()[0]
        except IndexError:
            lang = 'en'

    if lang not in LITS and '_' in lang:
        lang = lang.split('_', 1)[0]

    lits = LITS.get(lang, LITS.get('en'))
    qlits = [x + " +" for x in lits]
    nqlits = [x + " -" for x in lits]

    # Find the length of the atfiller string
    atflrlen = len(atfiller)

    # Figure out the phase
    juliandate = unix_to_julian(datetimeobj)
    pctphase, _, _, _, _, _, _ = phase(juliandate)
    
    # Fix waxes and wanes direction for south hemisphere
    if hemisphere == 'south':
        pctphase = 1 - pctphase
        
    angphase = pctphase * 2.0 * PI
    mcap = -cos(angphase)

    # Figure out how big the moon is
    yrad = numlines / 2.0
    xrad = yrad / ASPECTRATIO

    # Figure out some other random stuff
    midlin = int(numlines / 2)
    phases, which = phasehunt2(juliandate)

    # Now output the moon, a slice at a time
    atflridx = 0
    lin = 0
    while lin < numlines:
        # Compute the edges of this slice
        ycoord = lin + 0.5 - yrad
        xright = xrad * sqrt(1.0 - (ycoord * ycoord) / (yrad * yrad))
        xleft = -xright
        if PI > angphase >= 0.0:
            xleft = mcap * xleft
        else:
            xright = mcap * xright

        colleft = int(xrad + 0.5) + int(xleft + 0.5)
        colright = int(xrad + 0.5) + int(xright + 0.5)

        # Now output the slice
        col = 0
        while col < colleft:
            putchar(' ')
            col += 1
        while col <= colright:
            if hemisphere == 'north':
                # north - read moons from upper-left to bottom-right
                if numlines == 6:
                    char = background6[lin][col]
                elif numlines == 18:
                    char = background18[lin][col]
                elif numlines == 19:
                    char = background19[lin][col]
                elif numlines == 21:
                    char = background21[lin][col]
                elif numlines == 22:
                    char = background22[lin][col]
                elif numlines == 23:
                    char = background23[lin][col]
                elif numlines == 24:
                    char = background24[lin][col]
                elif numlines == 29:
                    char = background29[lin][col]
                elif numlines == 32:
                    char = background32[lin][col]
                else:
                    char = '@'
            else: 
                # south - read moons from bottom-right to upper-left
                # equivalent to rotate 180 degress or turn upside-down
                if numlines == 6:
                    char = background6[-1-lin][-col]
                elif numlines == 18:
                    char = background18[-1-lin][-col]
                elif numlines == 19:
                    char = background19[-1-lin][-col]
                elif numlines == 21:
                    char = background21[-1-lin][-col]
                elif numlines == 22:
                    char = background22[-1-lin][-col]
                elif numlines == 23:
                    char = background23[-1-lin][-col]
                elif numlines == 24:
                    char = background24[-1-lin][-col]
                elif numlines == 29:
                    char = background29[-1-lin][-col]
                elif numlines == 32:
                    char = background32[-1-lin][-col]
                else:
                    char = '@'
                
                #rotate char upside-down if needed
                char = rotate(char)
                
            if char != '@':
                putchar(char)
            else:
                putchar(atfiller[atflridx])
                atflridx = (atflridx + 1) % atflrlen
            col += 1

        if (numlines <= 27 and not notext):
            # Output the end-of-line information, if any
            fputs("\t ")
            if lin == midlin - 2:
                fputs(qlits[int(which[0] * 4.0 + 0.001)])
            elif lin == midlin - 1:
                fputs(putseconds(int((juliandate - phases[0]) * SECSPERDAY)))
            elif lin == midlin:
                fputs(nqlits[int(which[1] * 4.0 + 0.001)])
            elif lin == midlin + 1:
                fputs(putseconds(int((phases[1] - juliandate) * SECSPERDAY)))

        putchar('\n')
        lin += 1

    return output[0]


def main():
    """ Main entry point

        :param args: argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='Show Phase of the Moon')
    parser.add_argument(
        '-n', '--lines',
        help='Number of lines to display (size of the moon)',
        required=False,
        default=DEFAULTNUMLINES
    )
    parser.add_argument(
        '-x', '--notext',
        help='Print no additional information, just the moon',
        required=False,
        default=DEFAULTNOTEXT,
        action="store_true"
    )
    parser.add_argument(
        'date',
        help='Date for that the phase of the Moon must be shown. Today by default',
        nargs='?',
        default=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    parser.add_argument(
        '-l', '--language',
        help='locale for that the phase of the Moon must be shown. English by default',
        nargs='?',
        default=None
    )
    parser.add_argument(
        '-s', '--hemisphere',
        help='Hemisphere from where to show moon [north/south]. North by default',
        required=False,
        choices=['north', 'south'],
        default=DEFAULTHEMISPHERE
    )
    
    
    
    
    args = vars(parser.parse_args())

    try:
        dateobj = time.mktime(dateutil.parser.parse(args['date']).timetuple())
    except Exception as err:  # pylint: disable=broad-except
        fatal(f"Can't parse date: {args['date']}")

    try:
        numlines = int(args['lines'])
        lang = args['language']
    except Exception as err:  # pylint: disable=broad-except
        print(err)
        fatal("Number of lines must be integer")

    try:
        notext = bool(args['notext'])
    except Exception as err:  # pylint: disable=broad-except
        print(err)
        
    try:
        hemisphere = str(args['hemisphere'])
    except Exception as err:  # pylint: disable=broad-except
        print(err)

    print(putmoon(dateobj, numlines, '@', notext, lang, hemisphere))
    
main()
