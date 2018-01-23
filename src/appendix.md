\appendix


# Additional information

This chapter contains information to help reproduce the results of Gaze but
are not important enough to appear in the main text.


## Calibrating OpenCV

OpenCV offers a tool to store camera calibration settings which can be used for
certain functions to improve their results. Gaze benefits from such functions,
among others it uses `solvePnP` which is used to estimate the head pose in @sec:head-pose-estimation. This section
explains briefly how to use the calibration tool. Please note that there is
also a
[tutorial](https://docs.opencv.org/3.0-beta/doc/tutorials/calib3d/camera_calibration/camera_calibration.html)
available which provides some videos and a more thorough explanation of the
mathematics.

The calibration tool can be found in OpenCV's samples,
[samples/cpp/calibration.cpp](https://github.com/opencv/opencv/blob/fc9e031454fd456d09e15944c99a419e73d80661/samples/cpp/calibration.cpp).
To be able to use it, OpenCV needs to be compiled manually by providing the
CMake flag `-DBUILD_EXAMPLES=ON` to build the `cpp-example-calibration`
executable. To calibrate the camera, the calibration tool needs to take a
couple of pictures of a benchmark image: a checkerboard pattern as in
@fig:calibcheck is used in the following. Calibration works best if the image
is on a hard surface, like card board. An example call to the calibration tool
is denoted in @cl:cvcalibcall. The parameters `-h=6` and `-w=9` describe the
layout of the checkerboard pattern. It means that the checkerboard is seven
squares down and ten squares across, since the parameters expect the numbers of
corners between four squares. `-n=10` is the number of images to be taken,
`-d=1000` is the delay between two images. A higher delay allows that during
calibration the image can be moved to more divers poses without triggering
another image, resulting in a higher variety of points which in turn leads to a
more exact estimation of the camera parameters. At least three pictures should
be taken, but more images provide better results. The output file to which the
calibration values are written is stored to the file passed with `-o`. The last
parameter, `-s=0.0015` is the size of one checkerboard square in meters. This
value should be measured on the printout of the checkerboard, as slight
variations can occur depending on page orientation, zoom levels, margins,
printer settings, and other factors. In the example the printed version's
squares' side lengths were \SI{1.5}{\milli\meter}. After a successful calibration,
`camera_calib.yml` will be written into the directory. It can be used to
configure Gaze, as explained in @sec:camera-and-screen-parameters.

```{ .bash caption="Using the OpenCV calibration tool to calibrate the camera." label=cl:cvcalibcall }
./cpp-example-calibration -h=6 -w=9 -n=10 -d=1000 -s=0.0015 -o=camera_calib.yml
```


## Determining the focal length

To find the effective focal length of a camera the angle of view needs to be
measured, and the sensor size has to be known. For Gaze's examples the sensor width is
assumed to be \SI{0.0055}{\meter}. After measuring the angle of view, it can be used to solve [@Wikipedia:aov]
\begin{align}
\alpha &= 2 \arctan \frac{d}{2f} \\
f &= \frac{d}{2 \tan \frac{\alpha}{2}},
\end{align}
with $d$ being the sensor size, either \SI{0.0055}{\meter} for horizontal calculations,
or \SI{0.0031}{\meter} for vertical one. These values are taken from @sec:camera-and-screen-parameters. $\alpha$
is the angle of view and $f$ is the focal length.
To find $\alpha$ the camera is placed parallel to a wall, facing it. Then the
distance $w$ between the left most and the right most points
which are still visible on the camera image, and the
distance between the camera and the wall $v$ are measured for the horizontal calculations. For applying this to the vertical case, the top and bottom most points need to be used. Using trigonometry
the angle of view can be calculated by substituting the values into
\begin{align}
\alpha = \arctan \frac{w}{2v}.
\end{align}
For the examples in Gaze the focal length used is \SI{0.01}{\meter}, which is
the approximate mean of the measured values for the horizontal and vertical
focal lengths ($f_h, f_v$), measured using a folding rule at a distance of
\SI{1.04}{\meter} for a MacBook Pro:
\begin{align}
f_h &= \frac{\SI{0.0055}{\meter}}{ 2 \tan \left( \frac{1}{2} \arctan \left( \frac{ w_h }{ 2v } \right) \right) }
= \frac{\SI{0.0055}{\meter}}{ 2 \tan \left( \frac{1}{2} \arctan \left( \frac{ \SI{1.13}{\meter} }{ 2 \cdot \SI{1.04}{\meter} } \right) \right) } \approx \SI{0.011}{\meter} \\
f_v &= \frac{\SI{0.0031}{\meter}}{ 2 \tan \left( \frac{1}{2} \arctan \left( \frac{ w_v }{ 2v } \right) \right) }
= \frac{\SI{0.0031}{\meter}}{ 2 \tan \left( \frac{1}{2} \arctan \left( \frac{ \SI{0.66}{\meter} } { 2 \cdot \SI{1.04}{\meter} } \right) \right) } \approx \SI{0.01}{\meter} \\
f &= \frac{f_h + f_v}{2} = \frac{\SI{0.011}{\meter} + \SI{0.01}{\meter}}{2} = \SI{0.0105}{\meter} \approx \SI{0.01}{\meter}.
\end{align}


# Tables

@file:assets/gen_files/table-comptimes-pexels.md

@file:assets/gen_files/table-comptimes-BioID.md

@file:assets/gen_files/table-relative-errors-pexels.md

@file:assets/gen_files/table-relative-errors-BioID.md


# Figures

![Some example faces from the pexels dataset used to visualize or compare different pipeline steps. The numbers refer to the image names.](pupil_detection_faces.png){ #fig:examplefaces }

![Comparison of eyeLike and Gaze's pupil detections, showing eyeLike's images above Gaze's. The original images can be seen in \Cref{fig:examplefaces}. Note that bigger cross markers mean smaller eye image crops.](pupil_detection_comparison.png){ #fig:pupildetectioncomparison }

![Comparison of solutions to the PnP problem using EPnP on the left and the iterative Levenberg--Marquardt optimization in OpenCV's solvePnP function. Pexels images 0000, 0025, 0031, 0044; cropped.](solvePnPcomparison.png){ #fig:solvepnpcomparison }

![Comparison of solutions to the PnP problem using five landmarks and six out of 68 landmarks. The left column is Model A described in @sec:head-pose-estimation-1, the middle column Model B. Pexels images 0000, 0025, 0031, 0044; cropped.](landmarkscomparison.png){ #fig:landmarkscomparison }

![Some example faces from the BioID dataset. The numbers refer to the image names.](BioID_exampleimages.png){ #fig:bioid_examples }

![OpenCV checkerboard pattern to calibrate a camera.](pattern.png){ #fig:calibcheck }


# Code Listings

```{ .yaml file="examples/camera_calib.yml" caption="Example camera calibration output." label=cl:cameracalibyml }
```

```{ .cpp file=assets/gaze/src/gaze/gaze_tracker.cpp label=cl:initpipeline caption="The `init_pipeline()` method. To extend it properly, a new `else if` case has to be added." lines=71-100 pathdepth=3 }
```


# References
\renewcommand{\footnote}[1]{} <!-- Avoid DOI links to go to footnotes: disable footnotes in general. -->
\begingroup\endgroup
