# Future work

After concluding that \Gaze{} is a useful software for eye tracking but not so
much for gaze tracking in the last chapter, this chapter presents a
non-exhaustive list of possible work to explore in the future. It will also
very briefly discuss the pre-trained models used in the thesis and how to
improve those in the future, and provide an outlook of what to expect next.


## Possible fixes and extensions for \Gaze{}

\Gaze{} has some issues which need attention. Mostly this is related to the
geometric model used to calculate the gaze points. The affine transformation
used to reverse the 2D projection to the 3D model and to transform the pupils
should be re-evaluated and possibly replaced. One way could be to model the
eyeballs as spheres or ellipsoids and perform more sophisticated projections
onto their surfaces. It might even be needed to account for refraction of light
in the eye, something not taken into account at all in \Gaze{}'s models. Some
of the models mentioned in @Hansen2010 could be of use.
Another possibility is to introduce a calibration method and see if the model
works using system calibrated to the subject. This might be difficult because
of the pipeline architecture, but custom steps or a general extension to the
pipeline are possibilities to solve this.

One additional possible shortcoming of \Gaze{} is that it relies on both,
Dlib and OpenCV heavily. Because of that, oftentimes conversions between the
data formats are needed, potentially slowing down the computations. While first
the algorithms themselves should be improved before thinking about such
details, it is something to keep in mind if working on \Gaze{}.

The way the configuration works is also worth improving. In the current
implementation, the 3D model has to be supplied multiple times inside the
configuration because the pipeline steps do not share their
information. It might be a good idea to aggregate shared information in one
block or define a different configuration format in general, to avoid
redundancies, as those can easily lead to errors.

Apart from these problems, there are also many possible extensions to make for
\Gaze{}. One is to implement result writes and readers. Writers give the
ability to store data and analyze it, readers allow to continue processing a
video file or to reevaluate data using a different method. When implementing
writers, it might also prove useful to determine what other information needs
to be stored inside the data object; for example, the frame number is currently
not stored but might be very useful for video analysis. Although there are
numerous different data formats for eye tracking data [@Schöning2016],
\Gaze{}'s modular approach allows for easy implementation of various formats.

Because the current implementation only allows for cameras located in the
screen plane, a second interesting extension to \Gaze{} would be to make this
more flexible. This is no easy task as the conversions then need to account for
four additional dimensions -- not only offsets in two directions but offsets
in three directions and a three-dimensional orientation. But this would allow
having setups with external webcams much easier than with the current
approach.

In terms of implementation, \Gaze{} has a couple of things to improve on. One
example are to provide bindings to other languages -- to use \Gaze{} in for
example Python, but also the other direction to write pipeline steps in Python
and use them within \Gaze{}. The former could be realized using frameworks like
[Boost.Python](http://www.boost.org/doc/libs/1_66_0/libs/python/doc/html/index.html)
or [pybind11](https://github.com/pybind/pybind11), the latter could be realized
by building the pipeline around a plugin system. Additionally many parts of the
code do not have proper tests yet. While there are some tests for the
`PupilLocalization` pipeline step, most other parts of the code are just tested
manually by visual inspection using the +GUI. This should be improved, as that
also improves the effectiveness of the continuous integration, as it is more
likely to warn of broken builds.


## Thoughts on the data and pre-trained models

To avoid the license disagreements between the different models used in \Gaze{},
a good idea is to search for other models with more permissive licenses or train
custom models which do not have those limitations. One of such alternative
models could be the five landmarks model provided by Dlib, and since it is
still unclear if those points are enough to determine the head pose, it is an
option to explore. To train custom models the biggest challenge is to come by
properly annotated data, but also to keep models small and efficient.

As was seen in @sec:face-detection, face detection is clearly not a completely
solved task yet. Even models trained on the "300 Faces In-The-Wild challenge"
do not recognize occluded faces, especially if occluded by shades or if only
have of the face is visible. Of course, it is a little bit of a definition
issue and depends on the question if one wants to detect occluded faces or not,
but in general, this is still not resolved. And even if only non-occluded faces
should be detected, tilted faces also still pose challenges. Thus improving on
face detections is still an interesting task. Of course, for eye tracking in
lab conditions the current detectors work well enough, even exceeding their
needs.


## Closing remarks

Eye and gaze tracking are an exciting field of research. Over the last century,
significant progress has been made, providing many sophisticated solutions to track
eyes and gaze in various ways. Many of those solutions require difficult setups,
are expensive, require specific hardware, or their implementations are not
available as open source solutions. \Gaze{} tries to fit into this landscape by
providing an +FOSS solution which does not require any difficult setup and no
specialized hardware. While it does not reach the same gaze tracking
performance like other solutions, its eye tracking capabilities are very promising.
It will be interesting to see if geometric models like the one in \Gaze{}, or
machine learning model like iTracker will provide tools to bring gaze tracking
to a broad community in the future -- and if webcams will be a useful tool to
do gaze tracking in general; inside academia, and outside. For studies which do
not need saccade information it might prove useful, as well as for
computer control and user experience research, and many other areas, some of
which are unthinkable of today.
