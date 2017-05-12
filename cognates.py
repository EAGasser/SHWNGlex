from lingpy import *
from lingpy.evaluate.acd import bcubes
from sys import argv

if len(argv) < 2:
    print('usage python cognates.py')
    
try:
    lex = LexStat('wordlist.bin.tsv', segments='segments')
except:
    lex = LexStat('wordlist-short.tsv', segments='segments')
    lex.get_scorer(runs=10000)
    lex.output('tsv', filename='wordlist.bin')


lex.cluster(method='lexstat', cluster_method='infomap', threshold=0.55)

p, r, f = bcubes(lex, 'cogid', 'lexstatid', pprint=True)
print('{0:.2f}\t{1:.2f}\t{2:.2f}'.format(p, r, f))

alm = Alignments(lex, ref='lexstatid')
alm.align(scoredict=lex.cscorer)
alm.output('tsv', filename='wordlist-aligned', ignore='all', prettify=False)
