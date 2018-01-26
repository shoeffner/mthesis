# \Gaze{} -- A gaze tracking library

\Gaze{} is the software library developed during this thesis. It is supposed to
perform gaze tracking in relaxed laboratory conditions. *Relaxed* laboratory
conditions means that, unlike for other eye tracking solutions, no special
setup or calibration is needed. \Gaze{} works with normal lighting conditions and
just a laptop with an attached webcam in front of the participant. It was
programmed with many best practices for +FOSS in mind and tries to provide a
transparent +API to track user gaze using a common webcam.

This chapter gives an overview over the library and its features and provides
detailed instructions on how to build and use it. The level of detail for the
instructions is very high to also give people without a strong
background in software development enough information to compile and run it.
Because \Gaze{} is +FOSS, this should enable many interested researchers to
reproduce the results presented in @chap:results-evaluations-and-comparisons.
Or they can try out other methods by using their own configurations and
implementations, leveraging \Gaze{}'s modular architecture and extendability.


## Features of \Gaze{}

\Gaze{} provides a flexible data pipeline consisting of multiple pre-defined
steps. It is possible to add custom steps by altering \Gaze{}'s source code in
very few places, as is explained in @sec:writing-a-custom-pipeline-step. Additionally \Gaze{}
features a debug +GUI, which visualizes each pipeline step individually. Once
implemented, the gaze tracker, the pipeline
and the pipeline steps can be configured using a +YAML file, `gaze.yaml`.
The library works best with the camera sensor being in the same plane as the
screen surface, thus built-in webcams are recommended. This is because
currently the configuration for the camera position assumes only offsets along
and across the screen, the orientation and depth can not be changed. \Gaze{} can
process live webcam streams, video files, and images.
The gaze tracker reliably tracks a subject's face and eyes, detects pupils,
estimates the head orientation, and also estimates the distance between camera
and subject. From these measured and estimated information, \Gaze{} calculates an
approximate gaze point.
\Gaze{} has been developed using macOS High Sierra, but also builds on Ubuntu 14.04 LTS.


## Free and open-source software

\Gaze{} is +FOSS, its source code can be found on
[GitHub](https://github.com/shoeffner/gaze). That means it is publicly available and the source code
and software can be modified and redistributed without any limitations. It is
released under the MIT License, which is open and permissive: It allows
commercial and private use, redistribution, and modification of the source
code without any conditions other than keeping the license with the
files [@MITLicense].


### Why free and open-source software?

The decision to release \Gaze{} as a +FOSS under the MIT License [@MITLicense] was
done because the author strongly believes that Open Source and Open Access are
important for research. By allowing everyone to use and modify the software and
to access the accompanying documentation and thesis, other researchers can
verify and reproduce the results. Other individuals can get all available
information about the project without having to pay for a license.
In case they are interested in the project, they can improve
it and contribute their modifications back, or build their own software out of
it. Especially due to the nature of thesis projects, it is unlikely that the
author will keep working on the project, but potential other authors do not
have to start from scratch and can use the code.

Positive side effects of releasing \Gaze{}'s source code publicly are that the
author tries to follow stricter coding guide lines, and provides a detailed source code
[documentation](https://shoeffner.github.io/gaze).


### Development process

A good practice is to manage code and other projects with a +vcs. Version
control allows to roll back changes if needed, retains a change history and,
since it can usually be synchronized between multiple devices, provides a
simple way to create backups. The +vcs used for \Gaze{} is
[Git](https://git-scm.com), which is very popular among software developers:
@stosurvey2017 finds in the [stackoverflow Developer Survey
2017](https://insights.stackoverflow.com/survey/2017), that about \SI{70}{{\%}} of
30,730 responses claim to be using at least Git for version control, followed
by [Subversion](https://subversion.apache.org/) with about \SI{10}{{\%}}. Of course
this data has to be taken into account
carefully, as most respondents are in some way users of
[Stack Overflow](https://stackoverflow.com), a programming related questions
and answers website. But the results mean that many people are already
familiar with Git and can easily join the project and collaborate without
having to overcome high entrance barriers like learning a new +vcs.

An exemplary workflow with Git starts with cloning the code
repository, that means downloading the latest source code. Then, for each
feature to be added to the project, these steps are performed:

1. Create a branch. This can be understood as a local temporary copy of the
   source code.
2. Modify the code in the branch to build the feature.
3. Create a commit, which is comparable to a checkpoint to which you can always
   return. It also gives the code a unique version number, since a commit
   creates a unique hash for the current code.
4. Publish the commit to the original host, which is called pushing.
5. After verifying that the commit does not break the functionality and follows
   the project's coding standards, the changes can be merged into the
   original code.

There are many different ways to structure a Git workflow. One is the GitFlow
branching model [@Driessen2010], which largely influenced \Gaze{}'s workflow in the
beginning. \Gaze{} does not use a specific develop and release branch, instead
finished features get pushed to the master branch directly, which makes the
process look more like a traditional trunk-based workflow, where all features
are developed and pushed onto a common branch, the so called trunk or master.

\Gaze{} is published on the source code hosting service
[GitHub](https://github.com). When a new commit is
pushed, that means uploaded, to the GitHub servers, a web request is sent to the
continuous integration service [Semaphore CI](https://semaphoreci.com).
Semaphore will compile the published version and run the unit tests, which test a
few methods for integrity. On success, the commit is considered valid and the
changes can be merged into the master branch. To prevent common mistakes and
ensure certain code quality guidelines, [cpplint](https://github.com/cpplint/cpplint)
can be used before pushing a commit to GitHub. It checks if the code
conforms to the
[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).

If a commit updates the master branch, Semaphore performs an additional step.
It builds the documentation for \Gaze{} and pushes it to a specially named branch,
the `gh-pages` branch. This branch is orphaned, which means it has no direct
relation to the other source code. GitHub uses this special branch for one of
its features: static page hosting. All contents on the `gh-pages` branch are published
at a specific +URL. This way, the [source code
documentation](https://shoeffner.github.io/gaze) is always available online and
contains the latest changes. "Always" is a slight simplification, as failures
can always happen: GitHub has a +sla uptime of \SI{99.95}{{\%}} for its
business customers. Since \Gaze{} is only hosted as a free repository, this +sla
does not apply directly, but it is reasonable to assume that the services are
available most of the time for free users as well.


### License issues

While \Gaze{} is licensed under the MIT License, it can not be used for commercial
applications at the time of writing this thesis, although the license gives
this impression. This is because the license of the training data
[@Sagonas2016] for the 68 face landmarks' model
`shape_predictor_68_face_landmarks.dat` [@King2009], which is used for the face
and landmark detection, does not allow commercial uses. On the website accompanying
the dataset it is explicitly stated that "the annotations are provided for
research purposes ONLY (NO commercial products)"[^quoteibug], and King
emphasizes in the
[`README.md`](https://github.com/davisking/dlib-models/blob/ae50fe33583de33c60276611d37915e93d11566b/README.md)
accompanying the model that the derived model falls under the same license.

[^quoteibug]: [https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/](https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/), Accessed: 2018-01-10.

A similar notice accompanies \Gaze{}. To avoid problems and allow commercial
applications, initially the five landmarks model was tried to be incorporated into \Gaze{}.
But the five landmarks selected by King do not perform well to estimate the
head pose in 3D as is explained in @sec:head-pose-estimation-1. Thus the 68 landmarks model was chosen, resulting in this
license disagreement.

The same licensing problem arises when using the iTracker extension.
The pre-trained model is released under a custom license which also does not
permit non-research usage, as Khosla states in the repositories
["License agreement for use of GazeCapture database and iTracker models"](https://github.com/CSAILVision/GazeCapture/blob/03e687b039a822e7d5bc70673f101def0cba7255/LICENSE.md#section-2--scope).
This usage restriction is surprising: The paper presenting the dataset and
the models is called "Eye Tracking for Everyone" [@Krafka2016], a bold claim
which does not seem to hold.


## Setting up \Gaze{}

Reproducing the results achieved with \Gaze{} is possible by following a couple of
setup steps. The source code should be downloaded, built, and tested using one
of the provided example programs, or a custom test program.

\Gaze{} builds on other free software and thus has some pre-requisites which need
to be fulfilled before compiling it. A C++17 compiler is inevitable, as \Gaze{} uses
`std::shared_mutex` from the C++ standard library, which was introduced in the
[C++17 standard](http://en.cppreference.com/w/cpp/thread/shared_mutex). For
example on macOS High Sierra this can be Clang 9, which compiles \Gaze{} properly,
for Ubuntu 14.04 g++7 works well, as was tested on Semaphore CI's build system.
Additional requirements are OpenCV 3.3.1, CMake 3.10.0, boost 1.55.0, and Dlib
version 19.8. Usually different versions of the software dependencies should
work fine, but for Dlib version 19.8 is a hard minimal requirement, as it
contains a [bug fix](https://github.com/davisking/dlib/pull/957) for a bug
discovered during the \Gaze{}'s development.


## Building, installing, and using \Gaze{}

Building \Gaze{} just requires two steps from the
`gaze` directory as is shown in @cl:buildgaze.
The `configure.sh` script in line 1 executes CMake to create the
required build files. Afterwards `make` compiles the project. To install \Gaze{}, `make
install` can be issued as a followup command; it installs all header files and
the library to the proper system locations.

```{ .bash caption="Building \Gaze{}." label=cl:buildgaze }
./configure.sh
cd build
make
```

\Gaze{} is a library, so it can not be used alone but only by incorporating it
into other programs. A minimal program to integrate \Gaze{} is demonstrated in
@cl:gaze_simple.cpp. The program `gaze_simple` will start the gaze tracker in
line 8 and track twenty webcam frames during the `for` loop in lines 9--12. The
only additional prerequisite is to have the
`shape_predictor_68_face_landmarks.dat` in the same directory as the executable
`gaze_simple`.
To compile the program, only a short CMake configuration file as shown in
@cl:cmakegazesimple is needed. It configures the compiler to link the
executable to Dlib, OpenCV and \Gaze{} by searching the library locations in lines
5--7 and linking against them in lines 10--11. By calling `cmake .. && make`
from a `build` directory next to the source file, the program will be built.

```{ .cpp file=assets/examples/gaze_simple/gaze_simple.cpp pathdepth=2 .caption label=cl:gaze_simple.cpp }
```

```{ .cmake file=assets/examples/gaze_simple/CMakeLists.txt pathdepth=2 .caption label=cl:cmakegazesimple }
```


### Demo programs

The \Gaze{} repository contains two example programs:
`simple_tracking` and `where_people_look`. To compile and use them, it is
necessary to run the configure step in @cl:buildgaze again, this time appending the `--examples`
option. After building the examples using `make`, two executables can be found in the
`build` directory.

The `simple_tracking` program demos the debug +GUI shown in @fig:gazedebuggui.
The debug view can be used to visualize \Gaze{}'s various pipeline steps and
inspect the computation times each step needs. The tab bar at the top of the
window can be used to switch between the different pipeline step
visualizations. The debug +GUI uses a tabbed bar to only visualize one step at
a time, as drawing many +GUI widgets at once is a computationally expensive
process. Additionally to the debug +GUI, a small window showing the current
measured gaze point using a green cross on a black background is shown when
using `simple_tracking`. It also implements the main loop of the program: As
soon as it is closed, \Gaze{} will close its debug +GUI as well and stop tracking.

![\Gaze{}'s debug GUI. On the left the pipeline steps are listed along with their
computation times in \si{\micro\second}. The tabs can be used to switch between
pipeline step visualizations.](gazedebuggui.png){#fig:gazedebuggui}

TODO(shoeffner): Replace photograph with less distracting one (maybe convert image to grayscale)

In their paper, @Judd2009 investigate salient regions of images. The program
`where_people_look` is a re-implementation of @Judd2009's experiment using
\Gaze{}. In then experiment, subjects are presented with 1000 randomly
chosen images. Their task is just to freely view each image for three seconds.
Each of the images is followed by gray screen for one second, in which
subjects are asked to fixate the center of the screen. In the original task,
the experiment was split into two blocks of 500 images each. The
re-implementation does not perform this split, as it is mostly used as an
example on how \Gaze{} can be integrated into typical experiments. To run the
experiment, first the subject identifier must be entered and the directory
containing the stimuli needs to be selected. The stimuli are downloaded during
the build process. After selecting the stimuli, a gray screen opens up and
once the subject is ready, the experiment can be started by pressing the space key.


### \Gaze{}'s application programming interface

The example program `where_people_look` from last section was developed before
the +API for \Gaze{} was settled. This helped to find out which functionality is
needed for an eye or gaze tracking experiment and allowed to design the +API in
a behavior driven way. The tasks in \Cref{tab:gazeapi} were observed during the
implementation of `where_people_look` and implemented in \Gaze{}.


Table: Functions of the \Gaze{} gaze tracker and their corresponding API methods. \label{tab:gazeapi}

Function                          API methods
--------------------------------- -----------------------------------------------
\multirow{2}{*}{Initialization}   `void init(std::string, bool)`
                                  `GazeTracker(std::string, bool)`
\begingroup\endgroup              \begingroup\endgroup
Calibration                       `void calibrate()`
\begingroup\endgroup              \begingroup\endgroup
\multirow{2}{*}{Trial annotation} `void start_trial(std::string)`
                                  `void stop_trial()`
\begingroup\endgroup              \begingroup\endgroup
Result storage                    None
\begingroup\endgroup              \begingroup\endgroup
Latest gaze location              `std::pair<int, int> get_current_gaze_point()`


The initialization of the `GazeTracker` is done by either calling the default
constructor followed by its `init()` function, or by using the two argument
constructor directly. In @cl:gaze_simple.cpp, the two
argument constructor is called with the subject identifier `"1"` and the
default value `false` for the debug flag. The subject identifier will be used
to store results on the hard drive. The debug flag decides whether the debug
+GUI which is shown in @fig:gazedebuggui should be opened by supplying `true`, or not. This is mostly of
interest during the development process and not during actual experiments,
which is why the default is `false`. If the debug +GUI should be shown when
starting the program, but not during the experiment, it can be simply be opened
by setting the flag to `true`. When the window is no longer needed, it can
be closed, without interfering any other windows needed for the experiment and
without interfering with \Gaze{}'s functionality.

The calibration method is introduced in case \Gaze{} would use some calibration
later on, but it is not used at the time of writing this thesis. Because the
eye tracking functionality was prioritized during development, the
trial annotations have also no effect other than printing a notice to the
terminal. They are supposed to write the identifier passed via
`start_trial(std::string)` to the result set, to identify which trial was
active during the stored measurements. As soon as a writer is implemented, this
functionality will work. The result storage is not used as it is supposed
handled by a pipeline step. If a pipeline step stores data, it will write the
output as soon as it receives the data, thus removing the need of a specific
function to trigger a save action.

This leaves \Gaze{} with just one other function than the initialization ones,
`get_current_gaze_point()`. This function is especially useful for
feedback loops and debugging, as it provides a direct access to the latest
result calculated by the \Gaze{} pipeline.


## Configuring and extending \Gaze{}

There are two ways to customize \Gaze{}. The first is to configure it using the
`gaze.yaml`, the second is to write a custom pipeline step. In the following
section, both options will be briefly explored to make it easy to integrate
with \Gaze{} and to extend it. This should make it easier to adjust \Gaze{}
to one's own needs and to contribute pipeline steps to the project.


### Configuring \Gaze{}

The `gaze.yaml` can be used to configure \Gaze{}. By creating a `gaze.yaml` file
inside the directory from which the program integrating \Gaze{} is executed, the
default configuration values can be overwritten. This works because \Gaze{} first
loads the default values and then replaces them by any changes made in a
potential `gaze.yaml`. This is done to allow customization of parameters
without recompiling the source code, thus making it easy to install \Gaze{} once
and use it in several different projects with different needs and settings.

The `gaze.yaml` consists of two major parts: The meta
configuration block to configure the camera and screen parameters and the
pipeline configuration. To get an idea of the default values and to get started
writing a custom `gaze.yaml`, the project contains a `gaze.default.yaml`, which
exhibits the default values used by \Gaze{} and contains a lot of information
about how each parameter affects the program and how it should be chosen. To
complement the documentation inside the file, the following two sections give
some hints about how to decide the values for which parameters.


#### Camera and screen parameters

Inside the meta configuration block which is seen in @cl:gazedefmeta reside the
setup related parameters, that
is the camera and screen settings. The screen settings consist of a resolution
in pixels and measurements in meters. For example, the laptop used for the
development process had a resolution of \SI{2880 x 1800}{{pixels}}, and
its screen width and height were \SIlist{33.5;20.7}{\centi\meter}. Since screen
sizes are usually provided in inches across the diagonal, the screen width and
height have to be measured manually.
Additionally to the screen width and height, the camera position has to be
measured. At the time of writing, \Gaze{} only supports cameras which are built
into the laptop screen or in the same plane as the screen, and only cameras
directed orthogonally away from the screen towards the subject. Thus, the camera
position has to be provided using two values, the horizontal offset $x$ from
the upper left screen corner, and the vertical offset $y$ from the same corner
, here $x = \SI{17.25}{\centi\meter},$ and $y = \SI{0.7}{\centi\meter}$.
@fig:measuringmetadata visualizes which measurements have to be taken.
The target parameters allow to specify an area of interest: Instead of mapping
the measured gaze coordinates to the screen coordinates, they will be mapped
into a regular grid with the dimensions mentioned inside the target parameters.

```{ .yaml file=assets/gaze/gaze.default.yaml label=cl:gazedefmeta caption="The default meta configuration block for \Gaze{}." .stripcomments lines=1-59 }
```

TODO(shoeffner): Add figure fig:measuringmetadata showing measurements

The camera's resolution can also be configured alongside the target +fps. Many
webcams are limited in their +fps capabilities, so even by providing high
values it is possible that the camera does not reach more than about 30 +fps.
For online fixation tracking this does not matter much, as \Gaze{} is slower than
30 +fps on a common MacBook Pro which is detailed in @sec:computation-times.
Still it means that \Gaze{} will not be able to properly track saccades in online
settings because its sampling rate is simply too slow. In offline settings,
when analyzing pre-recorded video data, \Gaze{} does not have these problems, as
the frame rate is defined by the video material.
The computation speed is additionally highly dependent on the image
sizes, so smaller resolutions lead to faster computation times.
Better hardware, for example a dedicated GPU to improve Dlib's or Caffe's
speeds, might also result in better computation times, possibly allowing for
faster performance of \Gaze{}.

Crucial settings for the camera to estimate distances properly are the sensor's
size, its aspect ratio, and the focal length. These values are difficult to
measure and many device vendors do not report them, as producing smaller
sensors and cameras using higher resolutions is cheaper @citationneeded. Apple
uses the iSight for their MacBook Pro. Its older versions uses a
\SI{6.35}{\milli\meter} sensor [@Luepke2005] with an aspect
ratio of 4:3. The 15 inches MacBook Pro from mid 2015 used for \Gaze{}'s
development has a default webcam resolution of \SI{1280 x 720}{{pixels}}, which
leads to an aspect ratio of 16:9. Since the sensor size is unknown, the best
available approximation is to use the old known value, \SI{6.35}{\milli\meter}. It
follows that the sensor size is \SI{5.5 x 3.1}{\milli\meter}, although it is
likely that they use a different size in reality, since the aspect ratio
changed. The focal length can be measured manually if it is not provided by the
manufacturer; this is shown in @sec:determining-the-focal-length.

Additionally to setting the sensor parameters, the webcam can be calibrated for
the use with OpenCV. Calibration in this case means to estimate the camera
matrix and distortion coefficients of a camera, which can be used to undistort
the images. \Gaze{} does not directly undistort the images to process them
further, but algorithms like `cv::solvePnP`,
which is used by \Gaze{}, benefit from exact values.
OpenCV provides a calibration tool which
outputs the needed matrices. Detailed instructions on how to use it
are inside the appendix in @sec:calibrating-opencv. Parts of the resulting output
file in @cl:cameracalibyml need to be merged into the `gaze.yaml`, namely the
sections `camera_matrix` and `distortion_coefficients`. They need to be placed
into the section `camera` inside the `meta` part. An example is already given
inside the `gaze.default.yml` file in @cl:gazedefmeta.

Note that the calibration is not necessary for testing and development
purposes, as it is possible to use an estimated camera matrix $C$ without any
distortions. According to @Mallick2016, a good approximation can be made using
the image width $w$ and its height $h$. For the example configuration of a 16:9
image with dimensions \SI{640 x 360}{{pixels}}, a possible estimated camera
matrix using the approximation would be
\begin{align}\def\arraystretch{2.2}
C = \left(\begin{array}{ccc}
w & 0 & \dfrac{w}{2} \\
0 & w & \dfrac{h}{2} \\
0 & 0 & 1
\end{array}\right)
= \left(\begin{array}{ccc}
640 & 0 & 320 \\
0 & 640 & 180 \\
0 & 0 & 1
\end{array}\right).
\end{align}


#### Pipeline steps

The pipeline step order as well as each individual pipeline step can be
configured using various options. This is useful as for example the different
implementations of @Timm2011 can be exchanged without recompiling \Gaze{} by just
changing the configuration file. The default pipeline configuration can
be found inside the `gaze.default.yaml` as well, it is shown in @cl:gazedefpipeline.

```{ .yaml file=assets/gaze/gaze.default.yaml label=cl:gazedefpipeline caption="The default pipeline configuration block for \Gaze{}." .stripcomments lines=61-200 }
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

The `FaceLandmarks` step employs Dlib's +HoG classifier with a pre-trained
model as explained in @sec:detecting-faces-and-eyes. The model path can be
adjusted using the `model` attribute. By default it is
`shape_predictor_68_face_landmarks.dat`, which is the model file downloaded
during \Gaze{}'s build process. The path has to be specified relative to the model
directory.

To estimate the head pose the `HeadPoseEstimation` step is configured with
an abstract 3D model of the head. The model is defined using the three
parameters `landmark_indices`, `model`, and `model_scale`. The landmark indices
are a list of integers corresponding to the landmarks of @Sagonas2016, but with
an offset of $-1$ since @Sagonas2016 use 1-based indexing, while Dlib uses 0-based
indexing. The default model uses six landmarks as outlined in
@sec:detecting-faces-and-eyes, but in @sec:head-pose-estimation-1 some other
models have been tried.

The steps `EyeLike` and `PupilLocalization` are fully exchangeable since both
are implementations of @Timm2011. `EyeLike` is a copy of Hume's code eyeLike
[@Hume2012], hence the name; It was adjusted to fit into \Gaze{}. The two steps
have some slight implementation differences. `EyeLike` scales the image patches
containing the eyes to a specific size of \SI{50x50}{{pixels}}, while
`PupilLocalization` avoids this.
Usually this means that if a subject sits closer to the camera and thus the
eyes are larger, `EyeLike` will perform faster, while `PupilLocalization` is
much faster for subjects which are further away from the camera. The precision
for both implementations is similar, but depending on whether the scale affects
precision or not, either one can outperform the other in certain circumstances.
Another implementation difference is that `PupilLocalization` uses a
pre-calculated lookup table for some constant values because it was hoped that
a lookup table might speed up the process at the cost of some memory.
Eventually the speed did not change much, the image size is a much more
important factor as it dominates the algorithm's complexity. A third
implementation detail is that `EyeLike` is implemented using OpenCV, while
`PupilLocalization` uses Dlib. A very interesting difference is the choice of
gradient functions. `EyeLike` uses a gradient function inspired by Matlab
[@Hume2012], `PupilLocalization` uses the standard Sobel edge detector as Dlib
implements it. For both implementations the `relative_threshold` can be set. In both steps it
is used to discard possible eye center locations if the gradient magnitude at
the tested location is below $\mu_\text{mag} + \theta \sigma_\text{mag}$ with
the `relative_threshold` $\theta$, which is detailed in @sec:pupil-localization.
By default the `PupilLocalization` with a relative threshold of $0.3$ is
used.

The final step of the default pipeline, `GazePointCalculation`, uses a simple
model to map the detected pupils onto the 3D head model and performs a ray cast
towards the screen as explained in @sec:geometric-model. For this to work, the
position of the screen in relation to the head is determined first. As
explained in @sec:distance-estimation, this is done by estimating the direction
and distance between head and screen.


### Writing a custom pipeline step

To add a new pipeline step to \Gaze{}, a few changes have to be made. The best
start is to add some configuration to the `gaze.default.yaml`, it only needs
to contain the type: `- type: NewStep`. When \Gaze{} is used with such a
"faulty" configuration, the `FallbackStep` will be used. It explains
which changes have to be made to implement a custom pipeline step. The
documentation for `PipelineStep` covers the procedure additionally. First, a
new header file needs to be
created. A template like @cl:newsteph is provided inside the documentation.
For the new pipeline step, the names have to be adjusted in lines 1, 2, 13, 18,
and 29 to represent the new type chosen above.
In line 15 the visualization type can be changed, allowed choices
are `Label`, `Image`, and `Perspective` visualizations. The choice determines
which widget is used for the pipeline step inside the debug +GUI. The last
change inside the header file is to add  documentation for the `process` and
`visualize` methods.
After that, a new implementation file, here `new_step.cpp`, has to be added
and referenced inside the `src/gaze/CMakeLists.txt` as an additional source
file. Similarly, the header file must be included in
`include/gaze/pipeline_steps.h`. The last step is to add a case to the
`init_pipeline()` function inside `src/gaze/gaze_tracker.cpp` which is seen in
@cl:initpipeline. Now the new step is readily available.

```{ .cpp file=assets/examples/pipeline_steps/new_step.h label=cl:newsteph caption="The template header for a new pipeline step. The names are modified to match the file name, so `MY_STEP` becomes `NEW_STEP` in the example." pathdepth=2 }
```

### GazeCapture

`GazeCapture` is one custom pipeline step which is more complicated. Instead of
the few changes in @sec:writing-a-custom-pipeline-step, it requires additional
compilation steps and depends on Caffe 1.0. Since it is also not completely
straight forward to compile it and still crashes from time to time due to some
memory access errors, it is disabled by default. It can be enabled by
configuring \Gaze{} using CMake by setting the flag `-DWITH_CAFFE=ON`.
The build process will then fetch Caffe and compile it, so that \Gaze{} can link
against it and it can be employed inside the pipeline.
When `GazeCapture` is used inside the pipeline, it requires only the `SourceCapture`
and `FaceLandmarks` pipeline steps to come before it. It performs predictions
using the iTracker +CNN outlined in @sec:an-alternative-approach-itracker.
