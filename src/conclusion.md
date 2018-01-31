# Results, evaluations and comparisons

As shown in @chap:a-gaze-tracking-library the \Gaze{} library achieves its
goals. It is able to process data in a timely manner and solves eye center tracking
extremely well. One of its shortcomings is the model to transform the detected
pupils from the 2D image into the 3D model. In the following sections, the
shortcomings and successes of \Gaze{} are quantified and qualified. Near the end of the chapter
a comparison with iTracker was planned, but since the gaze points cannot be
calculated properly using the geometric model, the comparison is limited. Instead, a brief qualitative
review of iTracker will be done.


## Library implementation

\Gaze{}'s goals to be easily integrable, extendable, to be +FOSS, well documented,
and cross-platform are mostly fulfilled. While it is sufficiently easy to
integrate \Gaze{} into software as shown in @sec:building-installing-and-using, it is not possible to extend
\Gaze{} with a custom pipeline step without recompiling it. It would have
been a bigger success if \Gaze{} truly followed a multi-purpose plugin architecture
to quickly prototype custom pipeline steps and test new models. But because \Gaze{}
achieves its goal to be +FOSS, it is possible to change that in the future --
and even gather feedback if that is really a useful addition. The documentation
is available and automatically built using Semaphore and thus always readily
available. The cross-platform usage is not thoroughly tested, but \Gaze{} builds
successfully on macOS and Ubuntu 14.04 and its tests pass on both those
platforms as well. The software fulfills many of its goals and is ready to use for eye tracking in feedback loops.
For gaze tracking in research settings, however, some shortcomings detailed below
need to be resolved first.


## Evaluation of the geometric model

The geometrical model proposed to track gaze is not working as expected.
Each individual part will be evaluated in the next sections to explain which ones are working and which ones are not.


### Face detection

The face detection works reliable on webcam images: Dlib's face detector
finds the faces in all images of the BioID dataset. The Pexels dataset is more
difficult: Dlib only detects faces in 80 out of 120 images.
@fig:undetected_faces shows the discarded 40 images. More than half of those 40
images contain faces which are either visible from the side or which have an
occluded half. Four faces feature uncommon sunglasses, two photos feature only eyes, and two others
only cats. Only a handful of faces are properly visible and many of those are
not upright. So the limitations of Dlib's face detector are mostly occluded
faces and faces in uncommon orientations, which is okay for the purpose of eye
and gaze tracking.

While missing some faces, Dlib has a much lower false positive rate than OpenCV
[@King2014], which is another option for face detection. Processing a
\SI{640x360}{{pixels}} image took about
\SI{130}{\milli\second} to \SI{140}{\milli\second} using OpenCV and about
\SI{160}{\milli\second} to \SI{170}{\milli\second} using Dlib. But factoring in
the advantage of also getting the 68 landmarks needed for the head pose
estimation during Dlib's processing time strengthens the choice of Dlib over
OpenCV.


### Pupil localization evaluation

One very successful part of \Gaze{} is the pupil center localization [@Timm2011]. Using
the BioID dataset [@Jesorsky2001] and the *relative error* introduced by @Jesorsky2001
the accuracy of \Gaze{}'s `PupilLocalization` can be benchmarked. The relative error
is defined as
\begin{align}
e_{\op} = \frac{\op \left( d_l, d_r \right) }{ d_p },
\end{align}
with $d_l, d_r$ the Euclidean distance between the left eye center and its
estimation, and the right eye center and its estimation, respectively.
$d_p$ denotes the Euclidean distance between the real eye centers. The operator $\op$
is either $\min$, $\max$, or $\mean(x, y) = \frac{x + y}{2}$. Depending on the
operation, different results are measured. If $\min$ is used, the accuracies
only take the result of the better eye into account, likewise the
worse eye is used for $\max$. The average error of both eyes is calculated
using the $\mean$ for the error measurement.
In \Cref{fig:bioid_accuracies} `EyeLike`, @Timm2011, and `PupilLocalization` are
compared using the $\max$ relative error, which makes a lot of sense for
accurate eye tracking. To measure the accuracy, the error $e_{\max}$ is
calculated and the percentage of faces for which the error is below or equal
the thresholds is reported. A comparison of all three different errors, $\min,
\max,$ and $\mean$, can be found in \Cref{tab:BioID-pupil-detection-accuracies}.

\begin{figure}
    \centering
    \begin{tikzpicture}
        \begin{axis}[xlabel={relative error},
                     ylabel={accuracy},
                     xticklabel style={/pgf/number format/fixed},
                     ymin=0,
                     ymax=1,
                     xmin=0,
                     xmax=0.25,
                     xtick={0, 0.05, 0.10, 0.15, 0.20, 0.25},
                     enlargelimits=false,
                     title={Maximum relative error accuracy comparison},
                     legend style={area legend, at={(0.65,0.2)}, anchor=south},
                    ]
            \addplot[color=blue,thick] table [x=error, y=Timm2011, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
            \addplot[color=black!60!green,thick] table [x=error, y=eyelike_max_normalized_error, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
            \addplot[color=red,thick] table [x=error, y=gaze_max_normalized_error, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
            \legend{Timm \& Barth,Hume,\Gaze{}}
        \end{axis}
    \end{tikzpicture}
    \caption[Comparison of pupil detection accuracies.]{\label{fig:bioid_accuracies}Comparison of pupil detection accuracy between Timm and Barth (2011), Hume (2012) and \Gaze{}'s \texttt{PupilLocalization} on the BioID dataset. Only the maximum relative error is shown, that is the worse eyes are taken into account. Refer to \Cref{tab:BioID-pupil-detection-accuracies} for a tabular version of all relative errors.}
\end{figure}

The accuracy of `PupilLocalization` is very good and reaches the same accuracy
as @Timm2011. Inspecting the times in \Cref{tab:comptimes-BioID} it becomes clear that `PupilLocalization` performs faster than the implementation of `EyeLike` on the
BioID dataset with a median computation time of @file:assets/gen_files/comptimes/BioID-all-PupilLocalization-median.si,
compared to `EyeLike`'s median computation time of @file:assets/gen_files/comptimes/BioID-all-EyeLike-median.si
across the whole dataset. Even the maximum
computation time is still on par. Still, since the eye size is a quadratic
factor in the implementation, the computation time of `PupilLocalization`
changes dramatically with bigger images, while `EyeLike`'s computation times
are relatively stable. This can be seen in \Cref{tab:comptimes-pexels} for the Pexels dataset, which contains
bigger images: The median computation time is
still better for the whole dataset, but while inspecting only results where
both eye patches have a side length of more than \SI{50}{{pixels}}, the size to
which `EyeLike` scales the eye patches to, `EyeLike` outperforms
`PupilLocalization` by a factor of about $4$.

It can be concluded that for real-time scenarios with today's image
resolutions `EyeLike` is the better choice, as it is faster with only a small
loss in performance. For accurate processing when time is of no critical
importance, for example during offline analysis of recorded video data, \Gaze{}'s
`PupilLocalization` is usually the better option. In general, it should be
noted, that with `PupilLocalization` and eyeLike [@Hume2012] there are two successful
replications of the eye center detection approach by @Timm2011. Comparing the
different accuracies per dataset which are listed in \Cref{tab:pexels-pupil-detection-accuracies}
and \Cref{tab:BioID-pupil-detection-accuracies}, it becomes clear that the
algorithm works better with the images from the BioID dataset, but still
performs reasonably well on the Pexels dataset.


### Head pose estimation

The head pose estimation works well in most cases.
In the extreme case when the nose points
directly towards the camera and the coronal plane is parallel to the screen
plane, that is if a subject is looking straight into the camera, there are two
equally likely possible solutions: the $z$ axis pointing
outwards or inwards. In most cases, this is not a problem, as it is unlikely
that this happens. But sometimes this causes different results from frame to
frame as the $z$ axis might change its direction in between.
Since there is no annotated ground truth containing head poses for the datasets used
it is not possible to give a quantitative analysis of the success of
the method, but as was lined out in @sec:head-pose-estimation a qualitative
analysis can be performed. In @sec:head-pose-estimation it is already
established that the +EPnP version of the `solvePnP` algorithm does not work as
well as the iterative version, thus here the difference between the five and
the 68 landmarks models will be shown.

The problem with the 68 landmarks model is, as stated in @sec:license-issues, that it is only allowed for
research usage. As an alternative,
the five landmarks model by Dlib was tried using a custom 3D head model.
Unfortunately, the 3D head model used in \Gaze{} [@Mallick2016] relies on the six
landmarks pronasal, gnathion, exocanthions left and right, and the cheilions
left and right, which are not all present in the five landmarks model. It uses
the two exocanthions, the subnasal -- the point below the nose -- and the
endocanthions. To be able to estimate a head pose, a
different 3D model is used, Model&nbsp;A in @cl:5lm-model. It is difficult to find
accurate relational measurements for these landmarks. The endocanthions are offset towards the center by the length of the palpebral fissure, similar to the eyeball centers.
The subnasal is located using an educated guess backed by the data about the
nasal height and the philtrum length [@Facebase].

```{ .yaml caption="The two 3D head models used for the five landmarks comparison." label=cl:5lm-model }
# Model A
landmark_indices: [4, 3, 0, 2, 1]
model: [
  [0.0, -0.0055, -0.0125],  # subnasal
  [-0.0433, 0.0327, -0.026],  # exocanthion right
  [0.0433, 0.0327, -0.026],  # exocanthion left
  [-0.01511, 0.0327, -0.026],  # endocanthion right
  [0.01511, 0.0327, -0.026],  # endocanthion left
]

# Model B
landmark_indices: [4, 3, 0, 2, 1]
model: [
  [0.0, -0.0055, -0.0125],  # subnasal
  [-0.0433, 0.0327, -0.026],  # exocanthion right
  [0.0433, 0.0327, -0.026],  # exocanthion left
  [-0.01511, 0.0327, -0.016],  # endocanthion right
  [0.01511, 0.0327, -0.016],  # endocanthion left
]
```

As can be seen in @fig:landmarkscomparison, this model is not sufficient. The
reason is that four of its five points are located on the same line. Thus the
vectors can no longer span three linearly independent vectors. A few adjustments
are tried to resolve this issue, for example using Model&nbsp;B in @cl:5lm-model
which just moves the endocanthions about a centimeter outwards of the face.
For some faces like 0031 in @fig:landmarkscomparison this works slightly better, for others like 0044 worse.
It remains unclear whether the five landmarks can be
used with a proper model to estimate head poses accurately, or if the points
really do not contain enough information to properly span three dimensions
between them.


### Gaze point estimation

The gaze point estimation consists of multiple parts. The first part is the
distance estimation, followed by the inverted projection of the detected pupil
centers into the model coordinates. The final step is the ray cast to determine
the gaze point locations.

The distance estimation is only using the outer canthal width, thus this part
is very likely to be highly inaccurate. No precise tests were performed during the evaluation,
a short measurement using a folding rule was conducted instead.
To test the distance, only
very strict face poses rotated towards the camera were considered. Variations
of about \SI{5}{\centi\meter} to \SI{10}{\centi\meter} are expected. Using the focal length of
\SI{10}{\milli\meter} established in @sec:determining-the-focal-length this cannot be achieved.
\Gaze{} estimates the distance about twice further than it is. One possible
explanation is that the focal length in @sec:determining-the-focal-length is
wrong. Given the fact that the MacBook Pro's display is only about half a
centimeter deep, it seems to be a better idea to use
\SI{5}{\milli\meter} instead. This way the overestimation by a factor of two is canceled and the
estimates fall into the right range.
Another possible explanation is the video resolution. In \Gaze{}'s experiments,
a resolution of only \SI{640x360}{{pixels}} is used, which is only half of the
native webcam resolution.
A third explanation might be that the sensor size assumption established in
@sec:camera-and-screen-parameters is invalid, and the newer MacBook's indeed
use a different camera.
Testing which of the problems accounts for the faulty distance estimation
is left open for the future.

The reprojection of the pupil centers turns out to be \Gaze{}'s biggest issue.
While the pupil centers appear to end up in roughly the correct region as can
be guessed from @fig:pupils3dmodel, their location is not accurate enough.
Presumably
the issue is that due to the transformation from a flat 2D projection into a 3D
model the information which is lost during the original 3D-2D projection is not
approximated well enough. This is likely a problem of the model.
A model worth testing instead might be to first perform an orthogonal projection
into the direction of the screen, fit the pupils into the projection and then
perform a ray cast from the pupils onto modeled eyeballs. This would resolve
an error which likely occurs in the current model: By not projecting the pupil
centers properly onto the eyeball, they are likely displaced in relation to
their true position. The effect is visualized in \Cref{fig:failedprojection} using a 2D
simplification: It can easily be seen that even slight variations of a few millimeters from the
correct $p_0$ can lead to huge errors on the screen.
\begin{figure}
\centering
\input{assets/images/failedprojection.tex}
\caption[A small pupil restoration error leads to big prediction errors.]{\label{fig:failedprojection}A small pupil restoration error of using $p_0$ instead of $p_1$ for
the ray cast from $e$ to the screen can lead to big errors on the screen
surface.}
\end{figure}
Because of these reconstruction problems, the ray casting also produces
wrong results -- although for the given inputs the results are correct.
An alternative to using a different model might be to introduce a
calibration method, which \Gaze{} tries to avoid.

To test how well \Gaze{} performs even with a faulty model it can be considered to
see how well it can distinguish between people looking to the left from people
looking to the right.
Unfortunately this turns out to be difficult to test using the datasets already
in use: Neither of the datasets contains
annotations whether the person is looking to the left or right. When
considering annotating the small Pexels dataset it quickly turns out that due
to the nature of portrait photos, most people gaze directly into the camera. In
fact, only 18 images feature obvious gazes to either side. The same holds for the BioID dataset,
in most pictures the people also gaze into the camera. Due to time
constraints, no further selection of images featuring prominent gazes to either side
has been done.


## Comparison with and brief review of iTracker

As outlined in the beginning of this chapter and @sec:an-alternative-approach-itracker,
originally a comparison between the geometric model and the +cnn was planned.
Now that the geometric model is only capable of doing eye tracking,
the comparison is simple: iTracker works well for
gaze tracking, but not for eye tracking, while the geometric model works well
for eye tracking, but not for gaze tracking. Hence, the following is a small
review of iTracker's qualitative performance and its usability.

The custom pipeline step `GazeCapture`, designed to replace most parts of the
default pipeline and employing the +cnn iTracker [@Krafka2016], performs well
up to some limitations.

Integrating iTracker into \Gaze{} is not an easy task as its dependency Caffe
and \Gaze{}'s dependency Dlib both depend on +BLAS, and there are multiple
different implementations of +BLAS available. While most libraries offer bindings to
multiple variants, it is only possible to use one version of +BLAS in
a final program. Thus Caffe and Dlib need to be compiled using the proper
bindings first before they can be used together in iTracker.
To build a custom program using \Gaze{} with the `GazeTracker` pipeline step
requires writing a CMakeLists file which first finds iTracker before searching
for \Gaze{}.
When using iTracker, \Gaze{} occasionally crashes due to some memory errors. It
is not clear whether it is the fault of \Gaze{} or if the problem is a resource
management within Caffe. But because this crash is not resolved, `GazeCapture`
is currently only an optional component.

Taking the technical issues aside, iTracker is able to estimate gaze
inside a limited scope. Because it is trained on data measured exclusively on
iPhones and iPads [@Krafka2016], it has a strong bias towards calculating gaze
points within the boundaries of those screens. This bias is visualized in
@fig:predictionsiTracker, which is a $\log \log$ visualization of the estimated gaze
points on the Pexels and the BioID dataset. Of course, as discussed in
@sec:head-pose-estimation-1, a high proportion of people are looking directly into
the camera, which of course leads to a natural aggregation around the top
middle area of the image, directly below the camera. Still only very few points
can be observed outside the boundaries of an iPhone or iPad screen in relation
to the camera.

![`GazeCapture`'s estimated gaze points on the BioID and Pexels dataset.;;Double-logarithmic visualization of the estimated gaze points on the screen using `GazeCapture`'s iTracker for the BioID dataset on the left and the Pexels dataset on the right. Brighter means more gaze points.](predictions_iTracker.png){ #fig:predictionsiTracker }

Overall iTracker is a convincing implementation of a +cnn for gaze tracking,
but a qualitatively broader training dataset might help improving it even further
to make it feasible in tracking gaze in other settings than on mobile screens.
While its computation times are slightly slower than the default pipeline used
in Gaze as is seen below, this is likely due to the fact that the test laptop
does not have a dedicated +GPU to use Caffe's full potential. This is something
to test in the future.


## Computation times

For real-time gaze point estimations, fast computation times are a very critical
metric. \Gaze{} performs relatively fast for small eyes. The most time-consuming
parts are the face detection and the eye center localization as can
be seen in \Cref{tab:pipeline-step-times}. The other pipeline steps,
especially the head pose estimation and the final ray cast are very fast.
The computation times of the `SourceCapture` step were not measured as it was
not used during the benchmarks because it is not capable of loading a series of
images unless they are frames of a video file.

@file:assets/gen_files/table-pipeline-step-times.md

Without taking the `SourceCapture` into account, the default pipeline is
usually the fastest pipeline. In cases where it needs to resize the lookup
table for the pupil detection step, it slows down a little bit as observed in
@sec:pupil-localization-evaluation. But even the slowest pipeline using
`GazeCapture` is still similarly fast, as can be seen in
\Cref{tab:pipeline-times}. It might be faster if a speedup is gained by using a
+GPU as theorized above. But even with the slightly slower speed iTracker's
+cnn is the best model currently implemented in \Gaze{}.

\clearpage

@file:assets/gen_files/table-pipeline-times.md

The total times for a pipeline in \Cref{tab:pipeline-times} are about
\SI{80}{\milli\second}, which means that the pipeline can process at most
\SI{12}{{frames}} in one second. The real number will be lower, as grabbing the
image from the webcam is not included in the measurements. This makes \Gaze{} a
good choice for non-time critical applications and offline data processing.
During online settings, it will only detect fixations lasting at least
\SI{160}{\milli\second} properly -- saccades or even microsaccades are too short
for \Gaze{} to process. In offline analysis, this can of course still work if
the source material's +FPS were high enough to detect the relevant features of
gaze.


## Conclusion

Gaze tracking using common webcams is definitely no solved problem. While it
earned more attention in the literature over the last few years, few solutions
exist that really work without many constraints. In this thesis, two possible
methods are evaluated: The geometric model, realized in the \Gaze{} library,
and the +cnn iTracker, a pre-trained model which can be used instead of the
geometric model.

\Gaze{} is a good library to perform eye tracking. It can easily be extended
and integrated into projects. Its gaze tracking capabilities are not working
properly, but thanks to its extendability it is possible to use iTracker
to detect gaze points. Many other issues in webcam gaze
tracking cannot be resolved using software alone: most webcams are limited to
small frame rates and it is extremely difficult to find the real specifications
like sensor sizes and focal lengths for many webcams.

While there are some other solutions to webcam eye and gaze tracking, many of the
projects are abandoned, need sophisticated calibration procedures or reach low
precision. The +cnn iTracker and similar approaches seem to be promising models
to make gaze tracking available for everyone and for all devices, but there is still
some work to do, like increasing the area of interest and reducing computation
times. But concerning the possibility of gaze tracking without additional
equipment and considerable cost it warrants further investigation.
