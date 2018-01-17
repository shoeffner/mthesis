# Results, evaluations and comparisons

## Library implementation

- eye tracking working
- gaze tracking not
- configuration possible
- flexible pipeline implementation (slight overhead)
- processing times

## Geometrical model

- gaze tracking not working

### Face detection

- dlib over OpenCV, advantages/shortocmings

### Head pose estimation

- model precision
- Problems will still arise when subjects point their noses directly into the
  camera: In such a case there are two possible solutions for the $z$ axis,
  either pointing outwards or pointing inwards of the head, leading to some false
  estimations.


### Pupil detection

- comparison eyeLike / PupilLocalization

### Gaze point estimation

- distance, projection problems

## iTracker

- mobile display limitations
- caffe troublesome
- segfault
- alright under the right circumstances
- "for everyone" vs. research only


## Conclusion

- easy to use software which can be extended and configured
- geometric model is not working
- eye (and pupil) tracking works mostly very well
- other solutions have their own shortcomings, so this is still an open exciting research question
