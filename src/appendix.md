\appendix


# Additional information

This chapter contains information to help reproduce the results of Gaze but
are not important enough to appear in the main text.


## Calibrating OpenCV

OpenCV offers a tool to store camera calibration settings which can be used for
certain functions to improve their results. Gaze benefits from such functions,
among others it uses `solvePnP` (@sec:head-pose-estimation). This section
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
couple of pictures of a benchmark image: a checkerboard pattern (see
@fig:calibcheck) is used in the following. Calibration works best if the image
is on a hard surface, like card board. An example call to the calibration tool
is denoted in @cl:cvcalibcall. The parameters `-h=6` and `-w=9` describe the
layout of the (checkerboard) pattern. It means that the checkerboard is seven
squares down and ten squares across, since the parameters expect the numbers of
corners between four squares. `-n=10` is the number of images to be taken,
`-d=1000` is the delay between two images. A higher delay allows that during
calibration the image can be moved to more divers poses without triggering
another image, resulting in a higher variety of points which in turn leads to a
more exact estimation of the camera parameters. The output file to which the
calibration values are written is stored to the file passed with `-o`. The last
parameter, `-s=0.0015` is the size of one checkerboard square in meters. This
value should be measured on the printout of the checkerboard, as slight
variations can occur depending on page orientation, zoom levels, margins,
printer settings, and other factors. In the example the printed version's
squares' side lengths were \SI{0.0015}{meters}. After a successful calibration,
`camera_calib.yml` will be written into the directory. It can be used to
configure Gaze, as explained in @sec:camera-and-screen-parameters.

```{ .bash caption="Using the OpenCV calibration tool to calibrate the camera." label=cl:cvcalibcall }
./cpp-example-calibration -h=6 -w=9 -n=10 -d=1000 -s=0.0015 -o=camera_calib.yml
```


# Figures

![Some example faces used to visualize or compare different pipeline steps. The numbers refer to the image names inside `tests/assets/pexel_faces`](pupil_detection_faces.png){ #fig:examplefaces }

![Comparison of eyeLike (top) and Gaze's pupil detections. The original images can be seen in \Cref{fig:examplefaces}. Note that bigger cross markers mean smaller eye image crops.](pupil_detection_comparison.png){ #fig:pupildetectioncomparison }

![Comparison of the solutions to the +PnP problem using +EPnP (left) and the iterative Levenberg--Marquardt optimization (right) in OpenCV's solvePnP function.](solvePnPcomparison.png){ #fig:solvepnpcomparison }

![OpenCV checkerboard pattern to calibrate a camera.](pattern.png){ #fig:calibcheck }


# Code Listings

```{ .yaml file="examples/camera_calib.yml" caption="Example camera calibration output." label=cl:cameracalibyml }
```

```{ .cpp file=assets/examples/pipeline_steps/new_step.h label=cl:newsteph caption="The template header for a new pipeline step. The names are modified to match the file name (`MY_STEP` becomes `NEW_STEP` in this example)." pathdepth=2 }
```


# References
\begingroup\endgroup
