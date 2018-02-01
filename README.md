# Master's thesis

This repository contains materials for my master's thesis evolving around the
gaze tracking library [gaze](https://github.com/shoeffner/gaze).

You can find the compiled version on the [GitHub releases page](https://github.com/shoeffner/mthesis/releases/tag/thesis.shoeffner).


## Setup compilation process

Requirements (tested, other versions might work as well):


**General**

- `pandoc` 2.0.6 - 2.1.1
- `pandoc-citeproc` 0.12.2.4 -- 0.13
- `pdfTeX` 3.14159265-2.6-1.40.18
- `Makeglossaries` 2.20
- `GNU Make` 3.81
- `ImageMagick` 7.0.7-21
- `ack` 2.22
- `Ghostscript` (`gs`) 9.21
- `Poppler` (`pdfinfo`) 0.62.0
- `OpenCV` 3.3.1 -- 3.4.0
- `caffe` 1.0
- `Python` 3.6.4, see [requirements.txt](requirements.txt).



## Compile

### First time

Download the [raw pexels dataset](https://github.com/shoeffner/mthesis/releases/download/thesis.shoeffner/PexelsDataset_raw.zip) and extract it into
[scratch/pexels_face_images](scratch/pexels_face_images).

### Every time

To compile the thesis, run:

```bash
make
```


## Additional materials

The folder [scratch](scratch) contains all kinds of things I came up with to gather
data, make calculations, etc.
In the folder [scratch/related_materials](scratch/related_materials) there are some materials I produced during
the process of my thesis but which are not really related to the written master's thesis.
