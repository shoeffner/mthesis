# Gaze -- A gaze tracking library

Gaze is a software library to perform gaze tracking in relaxed laboratory
conditions. *Relaxed* laboratory conditions means that, unlike for other eye
tracking solutions, no special setup is needed. Gaze works with normal lighting
conditions and just a laptop with an attached webcam in front of the
participant. It was programmed with many best practices for +FOSS in mind and
tries to provide a transparent +API to track user gaze using a common webcam.


## Features of Gaze

Gaze provides a flexible data pipeline consisting of multiple pre-defined
steps. It is possible to add custom steps by altering Gaze's source code in
very few places (see @sec:writing-a-custom-pipeline-step). Once
implemented, the gaze tracker, the pipeline
and the pipeline steps can be configured using a +YAML file, `gaze.yaml`.
The software works best with the camera sensor being in the same plane as the
screen surface, thus built-in webcams are recommended[^3Doffsetcamera]. It can
process live webcam streams, video files, and images (see @sec:input-source-capture).
The gaze tracker reliably tracks a subject's face and eyes, detects pupils,
estimates the head orientation, and also estimates the distance between camera
and subject. From these measured and estimated information, Gaze calculates an
approximate gaze point.
Gaze has been developed using macOS Sierra and macOS High Sierra, but works on
Ubuntu 14.04 LTS as well[^nowindows].

[^3Doffsetcamera]: Currently the configuration for the camera position assumes
  only offsets along and across the screen, the orientation and depth can not
  be changed.

[^nowindows]: macOS Sierra has been used in the early development process, but
  after the macOS High Sierra update in September 2017, development was done
  under MacOS High Sierra. Ubuntu 14.04 LTS v1711 was not tested live, but
  built and unit-tested on the Semaphore CI service. Unfortunately Gaze was not
  tested on a Microsoft Windows system.


## Free and open-source software

Gaze is free and open-source, its soure code can be found on
[GitHub](https://github.com/shoeffner/gaze). That means it is publicly available and the source code
and software can be modified and redistributed without any limitations. It is
released under the MIT License, which is open and permissive: It allows
commercial and private use, redistribution, and modificatiion of the source
code without any conditions other than keeping the license with the
files [@MITLicense].


### Why free and open-source software?

The decision to release Gaze as a +FOSS under the MIT License [@MITLicense] was
done because the author strongly believes that Open Source and Open Access are
important for research. By allowing everyone to use and modify the software and
to access the accompanying documentation and thesis, other researches can
verify and reproduce the results. Other individuals can get all available
information about the project without having to pay for a journal or buying a
software license. In case they are interested in the project, they can improve
it and contribute their modifications back, or build their own software out of
it. Especially due to the nature of thesis projects, it is unlikely that the
author will keep working on the project, but potential other authors do not
have to start from scratch and can use the code.

Positive side effects of releasing Gaze's source code publicly are that the
author tries to follow stricter coding guide lines (by employing
[cpplint](https://github.com/cpplint/cpplint) for
static code checking), and provides a detailed source code
documentation[^docslink].

[^docslink]: [https://shoeffner.github.io/gaze](https://shoeffner.github.io/gaze)


### Development process

A good practice is to manage code (and other projects) with a +VCS. Version
control allows to roll back changes if needed, retains a change history and,
since it can usually be synchronized between multiple devices, provides a
simple way to create backups. The author's +VCS of choice for Gaze is
[Git](https://git-scm.com), which is very popular among software developers:
@stosurvey2017 finds in the [stackoverflow Developer Survey
2017](https://insights.stackoverflow.com/survey/2017), that about 70&nbsp;% of
30,730 responses claim to be using (at least) Git for version control (followed
by [Subversion](https://subversion.apache.org/) with about 10&nbsp;%). Of course
this data has to be taken into account
carefully, as most respondents are in some way users of the website
[stackoverflow.com](https://stackoverflow.com), a programming related questions
and answers website. But the results mean that many people are already
familiar with Git and can easily join the project and collaborate without
having to overcome high entrance barriers like learning a new +VCS.

A typical workflow with Git starts with cloning the code
repository, that means downloading the latest source code. Then, for each
feature to be added to the project, these steps are performed:

1. Create a branch. This can be understand as a local temporary copy of the
   source code.
2. Modify the code in the branch to build the feature.
3. Create a commit, which is comparable to a checkpoint to which you can always
   return. It also gives the code a unique version number, since a commit
   creates a unique hash for the current code[^hashadvantages].
4. Publish the commit to the original host[^onlydiffpushed] (this is called
   pushing).
5. After verifying that the commit does not break the functionality and follows
   the project's coding standards, the changes can be merged into the
   original code.

There are many different ways to structure a Git workflow. One is the GitFlow
branching model [@Driessen2010], which largely influenced Gaze's workflow in the
beginning. Gaze does not use a specific develop and release branch, instead
finished features get pushed to the master branch directly, which makes the
process look more like a traditional trunk-based workflow, where all features
are developed and pushed onto a common branch, the so called trunk or master.

[^hashadvantages]: Having a unique hash for a code has other advantages as
  well, for example it can be used to verify the integrity of source code.
  While for SHA1, the algorithm behind git's hash creation, a hash collision
  has been found [@Stevens2017], Git takes steps against it.
[^onlydiffpushed]: Technically, only the differences between the original and
  the changed version are submitted, plus some meta information.

Gaze is published on the source code hosting service
[GitHub](https://github.com). Whenever a new commit is
pushed (i.e. uploaded) to the GitHub servers, a web request is sent to the
continuous integration service [Semaphore CI](https://semaphoreci.com).
Semaphore will compile the published version and run the unit tests, which test a
few methods for integrity. On success, the commit is considered valid and the
changes can be merged into the master branch.

Whenever the master branch is updated, Semaphore performs an additional step.
It builds the documentation for Gaze and pushes it to a specially named branch,
the `gh-pages` branch. This branch is orphaned, which means it has no direct
relation to the other source code. GitHub uses this special branch for one of
its features: static page hosting. All content on the `gh-pages` branch is
published at the +URL
[https://shoeffner.github.io/gaze](https://shoeffner.github.io/gaze).
This way the documentation is always available online and
contains the latest changes. "Always" is a slight simplification, as failures
can always happen: GitHub has an +SLA uptime of 99.95&nbsp;% for its
business customers. Since Gaze is only hosted as free repository, this +SLA
does not apply directly, but it is reasonable to assume that the services are
available most of the time for free users as well.


### Licensing issues

While Gaze is licensed under the +MIT License, it can not be used for commercial
applications at the time of writing this thesis. This is because the license of
the training data [@Sagonas2016] for the 68 face landmarks' model [@King2009]
(`shape_predictor_68_face_landmarks.dat`), which is used for the face and
landmark detection, does not allow commercial uses. On the website accompanying
the dataset it is explicitly stated that "the annotations are provided for
research purposes ONLY (NO commercial products)"[^quoteibug], and King
emphasizes this in the `README.md` accompanying the model:

[^quoteibug]: [https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/](https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/), Accessed: 2018-01-10.

> The license for this dataset excludes commercial use and Stefanos Zafeiriou,
> one of the creators of the dataset, asked me to include a note here saying
> that the trained model therefore can't be used in a commerical product.
>
> \raggedleft --- <cite>Davis King, [README.md](https://github.com/davisking/dlib-models/blob/ae50fe33583de33c60276611d37915e93d11566b/README.md), Accessed: 2018-01-10.</cite>

A similar notice accompanies Gaze. To avoid problems and allow commercial
applications, initially the five landmarks model was tried to be incorporated into Gaze.
But the five landmarks selected by King do not perform well to estimate the
head pose in 3D, so the 68 landmarks model was chosen, resulting in this
license crash.

TODO(shoeffner): add cross ref to head pose estimation


## Setting up Gaze

Reproducing the results achieved with Gaze is possible by following a couple of
setup steps. The source code should be downloaded, built, and tested using one
of the provided example programs, or a custom test program. Gaze's source can
be found at
[https://github.com/shoeffner/gaze](https://github.com/shoeffner/gaze).

Gaze has some dependencies which need to be installed before building Gaze. A
C++17 compiler is inevitable, as Gaze uses
[`shared_mutex`](http://en.cppreference.com/w/cpp/thread/shared_mutex). For
example on macOS High Sierra Clang 9 compiles Gaze properly,
for Ubuntu 14.04 g++ 7 works well[^testedonsemaphore].
Additional requirements are OpenCV (3.3.1), CMake (3.10.0-rc3), and dlib
(v19.8)[^hardrequirements].

[^testedonsemaphore]: Tested only on Semaphore.
[^hardrequirements]: The required versions for CMake and dlib are minimal
  requirements, for OpenCV some lower versions might work as well (but are
  untested). CMake requires a version 3.10 to find the correct boost libraries
  needed for one example program, dlib contains a bug fix in version 19.8 which
  was made for the development of this thesis
  ([dlib pull request 957](https://github.com/davisking/dlib/pull/957)).


### Building and installing Gaze

Under normal circumstances, building Gaze just requires two steps (from the
`gaze` directory):

```{ .bash caption="Building Gaze." }
./configure.sh
cd build
make -j8
```

The `configure.sh` script executes [CMake](https://cmake.org/) to create the
needed build files. Afterwards `make` compiles the project. Adding `make
install` as a followup command installs all header files and the library to the
proper system locations.


## Using Gaze

Gaze is a library, so it can not be used alone but only by incorporating it
into other programs. A minimal program to integrate gaze might look like
this:

```{ .cpp file=assets/examples/gaze_simple/gaze_simple.cpp pathdepth=2 .caption label=cl:gaze_simple.cpp }
```

The program `gaze_simple` (see @cl:gaze_simple.cpp) will start the gaze tracker and track twenty webcam frames,
given the `shape_predictor_68_face_landmarks.dat` is next to the executable.
To compile the program, only a short CMake configuration file like @cl:cmakegazesimple is needed.

```{ .cmake file=assets/examples/gaze_simple/CMakeLists.txt pathdepth=2 .caption label=cl:cmakegazesimple }
```


### Demo programs

The Gaze repository contains two example programs:
`simple_tracking` and `where_people_look`. To compile and use them, it is
necessary to run the configure step again, this time using the `--examples`
option (@cl:configureshexamples).

```{ .bash caption="Building Gaze usage examples." label=cl:configureshexamples }
./configure.sh --examples
cd build
make -j8
```

After building the examples using `make`, two executables can be found in the
`build` directory.

The simple tracker just opens up a black screen containing a green cross which
denotes the current gaze point, alongside the gaze tracker's debug +GUI (@fig:gazedebuggui). The
debug view can be used to visualize the various pipeline steps and inspect the
computation times each step needs.

![Gaze's debug +GUI. On the left the pipeline steps are listed along with their
computation times in \si{\micro\second}.](gazedebuggui.png){#fig:gazedebuggui}

TODO(shoeffner): Remove photograph with less distracting one (maybe convert image to grayscale)

Where people look is a reimplementation of @Judd2009's experiment using Gaze.

TODO(shoeffner): explain where people look more detailed


### Application programming interface

TODO(shoeffner): gaze API


## Configuring and extending Gaze

There are two ways to customize Gaze. The first is to configure it using the
`gaze.yaml`, the second is to write a custom pipeline step. In the following
section, both options will be briefly explored.


### Configuring Gaze

To configure Gaze, the `gaze.yaml` can be used. By just copying (and renaming) the
`gaze.default.yaml` to the directory from which Gaze is executed, the default
values can be overwritten. This works because Gaze first loads the default
values and then replaces them by any changes made in a potential `gaze.yaml`.
The `gaze.yaml` consists of two major parts: The meta configuration block to
configure the camera and screen parameters and the pipeline configuration.


#### Camera and screen parameters

Inside the meta configuration block (@cl:gazedefmeta) reside the setup related parameters, that
is the camera and screen settings. The screen settings consist of a resolution
in pixels and measurements in meters. For example, the Laptop used for the
development process had a resolution of \SI{2880 x 1800}{{pixels}}, and
its screen width and height were \SIlist{0.335;0.207}{\meter}. Since screen
sizes are usually provided in inches across the diagonal, the screen width and
height have to be measured manually.
Additionally to the screen width and height, the camera position has to be
measured. At the time of writing, Gaze only supports cameras which are built
into the laptop screen or in the same plane as the screen, and only cameras
directed orthogonally away from the screen towards the subject. Thus, the camera
position has to be provided using two values, the horizontal offset $x$ from
the upper left screen corner, and the vertical offset $y$ from the same corner.
@fig:measuringmetadata visualizes which measurements have to be taken.

```{ .yaml file=assets/gaze/gaze.default.yaml label=cl:gazedefmeta caption="The default meta configuration block for Gaze." .stripcomments lines=1-56 }
```

TODO(shoeffner): Correctly measure dimensions, just in case. Also, change the default values to something more common.

TODO(shoeffner): Add figure fig:measuringmetadata showing measurements

The camera's resolution can also be configured alongside the target +FPS. Many
webcams are limited in their +FPS capabilities, so even by providing high
values it is possible that the camera does not reach more than about 30 +FPS.
For online gaze tracking this does not matter much, as Gaze is slower than
30 +FPS on a common MacBook Pro. But better hardware might result in better
computation times, possibly allowing Gaze to be faster.

TODO(shoeffner): Add ref for Gaze's performance.

Crucial settings for the camera to estimate distances properly are the sensor's
size and its aspect ratio. These values are difficult to measure and many
device vendors do not report them, as producing smaller sensors and cameras
using higher resolutions is cheaper @citationneeded. Apple uses the iSight for
their MacBook Pro. Its older versions uses a \SI{0.00635}{\meter}
(\SI{1/4}{{inches}}) sensor[^cnetisight] with an aspect ratio of 4:3.
The 15 inches MacBook Pro from mid 2015 used for Gaze's development has a
default webcam resolution of \SI{1280 x 720}{{pixels}}, which leads to an
aspect ratio of 16:9. The sensor size is \todo{add sensor size}.

[^cnetisight]: https://www.cnet.com/products/apple-isight/specs/, Accessed: 2018-01-09.

TODO(shoeffner): Remeasure sensor size using reference image and explain procedure

Additionally to the sensor parameters, the webcam can be calibrated for the use
with OpenCV. Calibration in this case means to estimate the camera matrix and
distortion coefficients of a camera, which can be used to undistort the images.
Gaze does not directly undistort the images to process them further, but
algorithms like
[`cv::solvePnP`](https://docs.opencv.org/3.3.1/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d),
which is used by Gaze, benefit from exact values.
OpenCV provides a calibration tool[^calibrationtool] which
outputs the needed settings. To be able to use it, OpenCV needs to be compiled
manually by providing the CMake flag `-DBUILD_EXAMPLES=ON` to build the
`cpp-example-calibration` executable. To calibrate the camera, the calibration
tool needs to take a couple of pictures of a benchmark image: a checkerboard
pattern (see @fig:calibcheck) is used in the following. Calibration works best
if the image is on a hard surface, like card board. An example call to the
calibration tool is denoted in @cl:cvcalibcall. The parameters `-h=6` and
`-w=9` describe the layout of the (checkerboard) pattern. It means that the
checkerboard is seven squares down and ten squares across, since the parameters
expect the numbers of corners between four squares. `-n=10` is the number of
images to be taken, `-d=1000` is the delay between two images. A higher delay
allows that during calibration the image can be moved to more divers poses
without triggering another image, resulting in a higher variety of points which
in turn leads to a more exact estimation of the camera parameters. The output
file to which the calibration values are written is stored to the file passed
with `-o`. The last parameter, `-s=0.0015` is the size of one checkerboard
square in meters. This value should be measured on the final printout of the
checkerboard, as slight variations can occur depending on page orientation,
zoom levels, margins, printer settings, and other factors. In the example the
printed version's squares' side lengths were \SI{0.0015}{meters}.

TODO(shoeffner): Add two or three different calibrating images.

[^calibrationtool]: The calibration tool can be found in OpenCV's samples,
  [samples/cpp/calibration.cpp](https://github.com/opencv/opencv/blob/fc9e031454fd456d09e15944c99a419e73d80661/samples/cpp/calibration.cpp).
  There is also a
  [tutorial](https://docs.opencv.org/3.0-beta/doc/tutorials/calib3d/camera_calibration/camera_calibration.html)
  available.

```{ .bash caption="Using the OpenCV calibration tool to calibrate the camera." label=cl:cvcalibcall }
./cpp-example-calibration -h=6 -w=9 -n=10 -d=1000 -s=0.0015 -o=camera_calib.yml
```

Parts of the resulting output file (@cl:cameracalibyml) need to be merged
into the `gaze.yaml`, namely the sections `camera_matrix` and
`distortion_coefficients`. They need to be placed into the section `camera`
inside the `meta` part. An example is already given inside the
`gaze.default.yml` file (@cl:gazedefmeta).

```{ .yaml file="examples/camera_calib.yml" caption="Example camera calibration output." label=cl:cameracalibyml }
```

Note that the calibration is not necessary for testing and development
purposes, as it is possible to use an estimated camera matrix $K$ without any
distortions. According to @Mallick2016, a good approximation is

\begin{align}\def\arraystretch{2.2}
K = \left(\begin{array}{ccc}
w & 0 & \dfrac{w}{2} \\
0 & w & \dfrac{h}{2} \\
0 & 0 & 1
\end{array}\right),
\end{align}

with $w$ being the image width and $h$ the image height in pixels. Thus for the
example configuration of a 16:9 image with dimensions \SI{640 x 360}{{pixels}},
a possible estimated camera matrix would be

\begin{align}
K = \left(\begin{array}{ccc}
640 & 0 & 320 \\
0 & 640 & 180 \\
0 & 0 & 1
\end{array}\right).
\end{align}

TODO(shoeffner): Should I call out the unused `target` parameters?


#### Pipeline steps

The pipeline step order as well as each individual pipeline step can be
configured using various options. This is useful as for example the different
implementations of @Timm2011 can be exchanged without recompiling Gaze by just
changing the configuration file. The default pipeline configuration can again
be found inside the `gaze.default.yaml` (@cl:gazedefpipeline).

```{ .yaml file=assets/gaze/gaze.default.yaml label=cl:gazedefpipeline caption="The default pipeline configuration block for Gaze." .stripcomments lines=58-200 }
```

All pipeline steps are identified by a type, which by convention maps to their
C++ class implementation name. The available types at the time of writing are
`SourceCapture`, `FaceLandmarks`, `HeadPoseEstimation`, `PupilLocalization`,
`EyeLike`, and  `GazePointCalculation`.

`SourceCapture` is a step to record input data. The data can be specified using
the `source` attribute. If an integer is provided, the corresponding webcam
device is used as a live stream. Usually the first camera with device ID `0` is
needed, thus this is the default. The setting can also be set to an image or
video path, allowing to analyze static images and video files as needed.

The `FaceLandmarks` step employs dlib's +HoG classifier with a pretrained
model. The model path can be adjusted using the `model` attribute, by default
it is `shape_predictor_68_face_landmarks.dat`, which is the model file
downloaded during Gaze's build process. The path has to be specified relative
to the model directory.

The steps `EyeLike` and `PupilLocalization` are fully exchangeable since both
are implementations of @Timm2011 (`EyeLike` is a copy of Hume's code
[@Hume2012], hence the name. It was adjusted to fit into Gaze). They have some
slight implementation differences. `EyeLike` scales the image patches
containing the eyes to a specific size, while `PupilLocalization` avoids this.
Usually this means that if a subject sits closer to the camera (and thus the
eyes are larger), `EyeLike` will perform faster, while `PupilLocalization` is
much faster for subjects which are further away from the camera. The precision
for both implementations is similar, but depending on whether the scale affects
precision or not, either one can outperform the other in certain circumstances.
Another implementation difference is that `PupilLocalization` uses a
pre-calculated lookup table for some constant values because it was hoped that
a lookup table might speed up the process at the cost of some memory.
Eventually the speed did not change much. A third implementation detail is that
`EyeLike` is implemented using OpenCV, while `PupilLocalization` uses dlib. For
both implementations the `relative_threshold` can be set. It is used to discard
possible eye center locations if the gradient magnitude at the tested location
is below $\mu_\text{mag} + \theta\sigma_\text{mag}$ (with $\theta$ being the
`relative_threshold`, see SECTION REFERENCE), in both steps. By default the
`PupilLocalization` with a relative threshold of $0.3$ is used.

To estimate the head pose the `HeadPoseEstimation` step is configured with
an abstract 3D model of the head. The model is defined using the three
parameters `landmark_indices`, `model`, and `model_scale`. The landmark indices
are a list of integers corresponding to the landmarks of iBug, but with an
offset of 1 since iBug uses 1-based indexing and dlib uses 0-based indexing.

TODO(shoeffner): Add section reference

TODO(shoeffner): Clarify the landmark indices (replace iBug)

### Writing a custom pipeline step

- fallback step
- places to change

- architecture/design (better move this to models and methods somehow)

