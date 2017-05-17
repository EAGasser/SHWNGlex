from lingpy import *
from sys import argv

if 'help' in argv or len(argv) < 2:
    print('Usage python nexus.py INFILE')

Wordlist(argv[1]).output('paps.nex', 
        filename=argv[1],
        ref='lexstatid', # cognate sets are here!
        missing='?'
        )
