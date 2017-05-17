# SHWNGlex


## Workflow

Make the initial conversion to lingpy-cldf format.

```shell

$ python template.py
```

Make the orthography profile preliminary.

```
$ lingpy profile -i wordlist.tsv -o profile.tsv --column=form
```

Once this is created, you can edit the profile. Then store the content of template in another script (file) and uncomment all ```#!``` instances. This should read your file and the profile and segment data accordingly, if you run the new script.

For cognates, change the name to the actual wordlist name, and run:

```
$ python cognates.py 
```

For nexus output, write:

```
$ python nexus.py INFILE
```



