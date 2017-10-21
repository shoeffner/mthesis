# Master's thesis

This repository contains materials for my master's thesis evolving around the
gaze tracking library [gaze](https://github.com/shoeffner/gaze).


## Setup compilation process

Requirements:
- `pandoc` 1.19.2.4
- `pandoc-citeproc` 0.11.1.1
- `python` 3.6.3


Install dependencies (using Python virtual environment):

```bash
python -m venv .venv gaze-thesis
source .venv/bin/activate
./install.sh
```


## Compile

```bash
make thesis
```


## Additional materials

```bash
cd related_materials
make presentation  # Build CV group presentation slides
make proposal  # Build original topic proposal
```
