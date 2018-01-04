# Gaze -- A gaze tracking library

Gaze is a software library to perform gaze tracking in relaxed laboratory
conditions[^relaxedlabconditions]. It was programmed with many best practices
for +FOSS in mind and tries to provide a transparent +API to track user gaze
using a common webcam.

[^relaxedlabconditions]: \emph{Relaxed} laboratory conditions means that unlike
  for other eye tracking solutions no special setup is needed. Gaze works with
  normal lighting conditions and just a laptop with an attached webcam in front
  of the participant.


## Features of Gaze

Gaze provides a flexible data pipeline consisting of multiple pre-defined
steps. It is possible to add custom steps by altering Gaze's source code in
very few places (see SECTION). Once implemented, the gaze tracker, the pipeline
and the pipeline steps can be configured using a +YAML file.

TODO(shoeffner): Add ref for SECTION

The software is still very limited and works best with the camera sensor being
in the same plane as the screen surface, thus built-in webcams are
recommended[^3Doffsetcamera]. It can process live webcam streams, video files,
and images[^supportedformats].

[^3Doffsetcamera]: Currently the configuration for the camera position assumes
  only offsets along and across the screen, the orientation and depth can not
  be changed.

[^supportedformats]: Gaze employs OpenCV's `VideoCapture` and is thus limited
  by its capabilities.

The gaze tracker reliably tracks a subject's face and eyes, detects pupils,
estimates the head orientation, and also estimates the distance between camera
and subject. From these measured and estimated information, Gaze calculates an
approximate gaze point.

Gaze has been developed using macOS Sierra and macOS High Sierra, but works on
Ubuntu 14.04 LTS as well[^nowindows].

[^nowindows]: macOS Sierra has been used in the early development process, but
  after the macOS High Sieera update in September 2017, development was done
  under MacOS High Sierra. Ubuntu 14.04 LTS v1711 was not tested live, but
  built and unit-tested on the Semaphore CI service. Unfortunately Gaze was not
  tested on a Microsoft Windows system. For more details, ...

TODO(shoeffner): Add ref for "more details"


## Free and open-source software

Gaze is free and open-source, its soure code can be found on
GitHub[^gazegithuburl]. That means it is publicly available and the source code
and software can be modified and redistributed without any limitations. It is
released under the *MIT License*, which is open and permissive: It allows
commercial and private use, redistribution, and modificatiion of the source
code without any conditions other than keeping the license with the
files [@MITLicense].

TODO(shoeffner): Consider mirroring to Bitbucket and GitLab.

[^gazegithuburl]:
  [https://github.com/shoeffner/gaze](https://github.com/shoeffner/gaze). There
  are no specific reasons to host Gaze on GitHub other than that the author is
  already familiar with the ecosystem, and that the libraries dlib and OpenCV are
  also available there.


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
@stosurvey2017 finds that about 70 % of 30,730 responses claim to be using (at
least) Git for version control (followed by
[Subversion](https://subversion.apache.org/) with about 10 %)[^stosurveylink].
This means that many people are already familiar with the tool and can easily
join the project for collaboration without high entrance barriers.

[^stosurveylink]:
  [stackoverflow Developer Survey 2017](https://insights.stackoverflow.com/survey/2017)

A typical workflow[^gitworkflows] with Git starts with *cloning the code
repository*, that is downloading the latest source code. Then, for each feature
to be added to the project, these steps are performed:

1. Create a branch. This can be understand as a local temporary copy of the
   source code.
2. Modify the code in the branch to build the feature.
3. Create a *commit*, which is comparable to a checkpoint where you can always
   return to. It also helps to give the code a version number, since a commit
   creates a unique hash for the current code[^hashadvantages].
4. Publish the commit to the original host[^onlydiffpushed] (this is called
   *pushing*).
5. After verifying that the commit does not break the functionality and follows
   the project's coding standards, the changes can be merged into the
   original code.

[^gitworkflows]: There are many different ways to structure a Git workflow. One
  is the *GitFlow* branching model [@Driessen2010], which hugely influenced
  Gaze's workflow in the beginning. However, Gaze does not use a specific develop
  and release branch, instead finished features get pushed to the master branch
  directly, which makes the process look more like a traditional trunk-based
  workflow, where all features are developed and pushed on a common branch, the
  so called trunk.
[^hashadvantages]: Having a unique hash for a code has other advantages as
  well, for example it can be used to verify the integrity of source code.
[^onlydiffpushed]: Technically, only the differences between the original and
  the changed version need to be submitted, alongside some meta information.

Gaze is published on the source code hosting service
[GitHub](https://github.com). Whenever a new commit is
pushed (i.e. uploaded) to the GitHub servers, a web request is sent to the
continuous integration service [Semaphore CI](https://semaphoreci.com).
Semaphore will compile the published version and run the unit tests, which test a
few methods for integrity. On success, the commit is considered valid and the
changes can be merged into the master branch.

Whenever the master branch is updated, Semaphore performs an additional step.
It builds the documentation for Gaze and pushes it to a specially named branch,
the `gh-pages` branch. This branch is *orphaned*, which means it has no direct
relation to the other source code. GitHub uses this special branch for one of
its features: static page hosting. All content on the `gh-pages` branch is
published at the URL
[https://shoeffner.github.io/gaze](https://shoeffner.github.io/gaze).
This way the documentation is always[^uptimegithub] available online and
contains the latest changes.

[^uptimegithub]: GitHub has an +SLA uptime of 99.95 % for its business
  customers. Since Gaze is only hosted as free repository, this +SLA does not
  apply directly, but it is reasonable to assume that the services are available
  most of the time for free users as well.

TODO(shoeffner): add index page to gh-pages branch


### Licensing issues

While Gaze is licensed under the MIT License, it can not be used for commercial
applications at the time of writing this thesis. This is because the license of
the training data [@Sagonas2016] for the 68 face landmarks' model [@King2009]
(`shape_predictor_68_face_landmarks.dat`), which is used for the face and
landmark detection, does not allow commercial uses. On the website accompanying
the dataset it is explicitly stated that "the annotations are provided for
research purposes ONLY (NO commercial products)"[^quoteibug], and King
clarifies this in the
[README.md](https://github.com/davisking/dlib-models/blob/ae50fe33583de33c60276611d37915e93d11566b/README.md)
accompanying the model:

> The license for this dataset excludes commercial use and Stefanos Zafeiriou,
> one of the creators of the dataset, asked me to include a note here saying
> that the trained model therefore can't be used in a commerical product.

TODO(shoeffner): Add similar notice to Gaze.

A similar notice accompanies Gaze. To avoid problems and allow commercial
applications, the author of Gaze initially tried to work with the five
landmarks model available with dlib. But the five landmarks selected by
King[^dlibmodelsREADME] for that model do not perform well to estimate the head
pose in 3D, so the 68 landmarks model was chosen, resulting in this license
crash.

[^quoteibug]: [https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/](https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/)
[^dlibmodelsREADME]: dlib-models' [README.md](https://github.com/davisking/dlib-models/blob/ae50fe33583de33c60276611d37915e93d11566b/README.md)


## Setting up Gaze

Reproducing the results achieved with Gaze is possible by following a couple of
setup steps. The source code should be downloaded, built, and tested using one
of the provided example programs, or a custom test program. Gaze's source can
be found at
[https://github.com/shoeffner/gaze](https://github.com/shoeffner/gaze).

Gaze has some dependencies which need to be installed before building Gaze. A
modern (2017 "modern") C++ compiler is inevitable (C++17 is needed as Gaze uses
[`shared_mutex`](http://en.cppreference.com/w/cpp/thread/shared_mutex)). For
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

Gaze is a library, so it can not be used alone but only by other programs.
A minimal program to integrate gaze might look like this[^simplificationsimplegaze]:

```{ .cpp file=assets/examples/gaze_simple/gaze_simple.cpp pathdepth=2 .caption }
```

[^simplificationsimplegaze]: Of course, it is possible to use e.g.\
  `std::unique_ptr` for the gaze tracker to avoid manual cleanup.

The above program will start the gaze tracker and track twenty webcam frames,
given the `shape_predictor_68_face_landmarks.dat` is next to the executable.
Gaze's API also allows to start and stop trials to distinguish them in the
output, but the functionality is not yet properly implemented.

To compile the program above, a CMake configuration like the following is enough:

```{ .cmake file=assets/examples/gaze_simple/CMakeLists.txt pathdepth=2 .caption  }
```

### Demo programs

Within the Gaze repository, two example programs are provided:
`simple_tracking` and `where_people_look`. To compile and use them, it is
necessary to run the configure step again:

```{ .bash caption="Building Gaze usage examples." }
./configure.sh --examples
cd build
make -j8
```

After building the examples using `make`, two executables can be found in the
`build` directory.

The simple tracker just opens up a black screen containing a green cross which
denotes the current gaze point, alongside the gaze tracker's debug view. The
debug view can be used to visualize the various pipeline steps and inspect the
computation times each step needs.

TODO(shoeffner): show example image

Where people look is a reimplementation of @Judd2009's experiment using Gaze.

TODO(shoeffner): explain where people look more detailed


## Configuring and extending Gaze

- gaze.default.yaml
- Contents of FallbackStep
- Explain how the Pipeline works

### Configuring Gaze

### Writing a custom pipeline step
