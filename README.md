# ccsv

A computed csv file format, not quite a csv, not quite a spreadsheet, concept in progress...


# Requirements
Recommended to use a virtual environment and install from the enviroments file. For example with `virtualenv`:

```shell
pyenv virtualenv 3.9.13 ccsv
pyenv activate ccsv
pip install -r requiremets.txt
```

# Usage
To output a `.csv` from a `.ccsv`
```shell
python ccsv.py examples/demo_v1.ccsv 
```


# TODO
- [x]  Create example
- [x]  Proof of concept with simple parser
- [x]  Proof of concept simple computation
- [x]  Put on github
- [x]  Move from notebook to script and run basic test
- [ ]  Consider using YAML instead of json? [https://pyyaml.org/wiki/PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [ ]  Set up testing 
- [ ]  Find a ready-to-go computation parser?
- [ ]  Put the csv part at the top?
    - [ ]  Use a delimiter of three hyphens, and just split the file based on that? sort of markdwon-esque
- [ ]  Add computation
- [ ]  Map out some more agreed upon base facts
- [ ]  Read up on pyparse for more complicated parsing (here)
    - [ ]  [https://dev.to/zchtodd/building-parsers-for-fun-and-profit-with-pyparsing-4l9e](https://dev.to/zchtodd/building-parsers-for-fun-and-profit-with-pyparsing-4l9e)
- [ ]  Stylesheets

### Future

- [ ]  Build an interface / integrate with csv viewer
- [ ]  Stylesheets
- [ ]  Custom functions and other metadata