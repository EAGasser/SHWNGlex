from lingpy import *
import re

data = csv2list('raw/data.tsv', strip_lines=False)
header1 = data[0]
header2 = data[1]
lang1 = header1[1:]
lang2 = header2[1:]
rest = data[2:]
rest1 = [rest[i] for i in range(0, len(rest), 2)]
rest2 = [rest[i+1] for i in range(0, len(rest), 2)]
idx = 1
D = { 0: [
    'doculect',
    'concept',
    'langid',
    'value',
    'form',
    'cog'
    ]
    }
for i, line in enumerate(rest1):
    concept = line[0]
    words = dict(zip(header2, line))
    cogs = dict(zip(header2, rest2[i]))
    for l1, l2 in zip(lang1, lang2):
        forms, cogids = words[l2].split(','), cogs[l2].split(',')
        if len(cogids) > len(forms):
            cogids += ['', '', '']
        for form, cog in zip(forms, cogids):
            if form.strip():
                D[idx] = [
                        l2,
                        concept,
                        l1,
                        words[l2],
                        form.strip(),
                        concept+'-'+cog.strip() or str(idx)+'-0'
                        ]
                idx += 1
wl = Wordlist(D)
wl.renumber('cog')
wl.add_entries('tokens', 'form', ipa2tokens, clean_string=True, merge_vowels=False,
        )


wl.output('tsv', filename='wordlist', prettify=False, ignore='all')

wl.output('taxa', filename='languages')
