from lingpy import *
from segments.tokenizer import Tokenizer
import re

data = csv2list('raw/data_incl_opt.tsv', strip_lines=False)

header1 = data[0]
header2 = data[1]

lang1 = header1[1:]
lang2 = header2[1:]
rest = data[2:]

rest1 = [rest[i] for i in range(0, len(rest), 2)]
rest2 = [rest[i+1] for i in range(0, len(rest), 2)]

# we store all data in the following dictionary, with the header being in data
# point key 0
idx = 1
D = { 0: [
    'doculect',
    'doculect_old',
    'concept',
    'langid',
    'value',
    'form',
    'cog',
    'tokens',
    ]
    }

# converter from languages.tsv to the rest
langs_ = {
        b: c for a, b, c in  csv2list(
            'languages.tsv', strip_lines=False)
        }


# load the tokenizer
tk = Tokenizer('profile.tsv')

for i, line in enumerate(rest1):
    concept = line[0]
    words = dict(zip(header2, line))
    cogs = dict(zip(header2, rest2[i]))
    for l1, l2 in zip(lang1, lang2):
        forms, cogids = words[l2].split(','), cogs[l2].split(',')
        if len(cogids) > len(forms):
            cogids += ['', '', '']
        for form, cog in zip(forms, cogids):
            if form.strip() != "?":
                tks = tk(form.replace(' ', '_').replace('?', ''), 'IPA')
                if form.strip():
                    D[idx] = [
                            langs_.get(l2, '???'),
                            l2,
                            concept,
                            l1,
                            words[l2],
                            form.strip(),
                            concept+'-'+cog.strip() or str(idx)+'-0',
                            tks.split(' ')
                            ]
                    idx += 1
wl = Wordlist(D)
wl.renumber('cog')
wl.add_entries('segments', 'tokens', lambda x: [y.split('/')[1] if '/' in y
    else y for y in x])

wl.output('tsv', filename='wordlist', prettify=False, ignore='all')

wl.output('tsv', filename='wordlist-short', prettify=False, ignore='all',
        subset=True, rows=dict(language='not in '+str([p for p in wl.taxa if
            p.startswith('Proto')])))

try:
    lex = LexStat('wordlist.bin.tsv')
except:
    lex = LexStat('wordlist-short.tsv', segments='segments')
    lex.get_scorer(runs=10000)
    lex.output('tsv', filename='wordlist.bin')
lex.cluster(method='lexstat', cluster_method='infomap', threshold=0.55)

from lingpy.evaluate.acd import bcubes
p, r, f = bcubes(lex, 'cogid', 'lexstatid', pprint=True)
print('{0:.2f}\t{1:.2f}\t{2:.2f}'.format(p, r, f))

alm = Alignments(lex, ref='lexstatid')
alm.align(scoredict=lex.cscorer)
alm.output('tsv', filename='wordlist-aligned', ignore='all', prettify=False)
