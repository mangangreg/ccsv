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

# Example
See [examples](./examples) folder for more.

demo_v3_yaml.ccsv
```yaml
---
name: test
value:
  - something1
  - something2,3,4
style:
  ".body":
    background: blue
    color: lightgrey
---
item,cost,quantity,total
chalk,3.50,2,=cost*quantity
cheese,1.99,1,=cost*quantity
```

gets converted to 
*demo_v3_yaml.csv*

```csv
item,cost,quantity,total
chalk,3.50,2,7.0
cheese,1.99,1,1.99
```



# TODO
- [x]  Create example
- [x]  Proof of concept with simple parser
- [x]  Proof of concept simple computation
- [x]  Put on github
- [x]  Move from notebook to script and run basic test
- [x]  Consider using YAML instead of json? [https://pyyaml.org/wiki/PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [x]  Html output
    - [ ] Basic output
    - [ ] Give a better formatted page, with some core style
- [ ]  Styles
    - [x] Basic yaml-css implementation
    - [ ] Custom styling on cells/rows etc.
- [ ]  Design
    - [ ] Sketch out overall goals a bit better (workflow, CLI, interface)
- [ ]  Set up testing 
- [ ]  Find a ready-to-go computation parser?
- [x]  Add computation
- [ ]  Map out some more agreed upon base facts
- [ ]  Read up on pyparse for more complicated parsing (here)
    - [ ]  [https://dev.to/zchtodd/building-parsers-for-fun-and-profit-with-pyparsing-4l9e](https://dev.to/zchtodd/building-parsers-for-fun-and-profit-with-pyparsing-4l9e)
- [ ] Tidy
    - [ ] clear out initial examples


### Future

- [ ]  Build an interface / integrate with csv viewer
- [ ]  Stylesheets
- [ ]  Custom functions and other metadata