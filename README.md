# Master's thesis

This repository contains materials for my master's thesis evolving around the
gaze tracking library [gaze](https://github.com/shoeffner/gaze).


## Setup compilation process

Requirements (tested, other versions might work as well):
- `pandoc` 2.0.6
- `pandoc-citeproc` 0.12.2.4
- `python` 3.6.4


Install dependencies (using Python virtual environment):

```bash
python -m venv .venv gaze-thesis
source .venv/bin/activate
./install.sh
```

This process also install [nbstripout](https://github.com/kynan/nbstripout)
which should be used to clean up ipynb files before committing them.

## Compile

To compile the full thesis, run:

```bash
make
```

To compile individual chapters, run:

```bash
make chapter_name
```

where `chapter_name` is the name of a file in `src`, e.g. to compile
`src/gaze_library.md` one can use:

```bash
make gaze_library
```


## Additional materials

The folder [scratch](scratch) contains all kinds of things I came up with to gather
data, make calculations, etc.
In the folder [scratch/related_materials](scratch/related_materials) there are some materials I produced during
the process of my thesis but which are not really related to the written master's thesis.
