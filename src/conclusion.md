# Results, evaluations and comparisons


## Library implementation

TOOD(shoeffner): Add more overall results and show that the implamentation is good.

Gaze's goals to be easily integrable, extendable, to be +FOSS, well documented,
and cross-platform are partly fulfilled. While it is sufficiently easy to
integrate Gaze into software as shown in @sec:building-installing-and-using-gaze, it is not possible to extend
Gaze with a custom pipeline step without building it from source. It would have
been a bigger success if Gaze truly followed a multi-purpose plugin architecture
to quickly prototype custom pipeline steps and test new models. But because Gaze
achieves its goal to be +FOSS, it is possible to change that in the future --
and even gather feedback if that is really a useful addition. The documentation
is available and automatically built using Semaphore and thus always readily
available. The cross-platform usage is not thoroughly tested, but Gaze builds
successfully on macOS and Ubuntu 14.04 and its tests pass on both those
platforms as well. Still the software fulfills many of its goals and could be
used for Gaze tracking in research settings. *Could* be used because not all
aspects of gaze tracking do work, as is outlined below.


## Evaluation of the geometric model

The geometrical model proposed to track gaze is not working. While parts of it
work well, other parts are not as successful. In the following sections the
individual parts will evaluated.


### Face detection

- dlib over OpenCV, advantages/shortcomings


### Pupil localization evaluation

One successful part of Gaze is the pupil center localization [@Timm2011]. Using
the BioID dataset [@Jesorsky2001] and the *relative error* introduced by @Jesorsky2001
the accuracy of Gaze's `PupilLocalization` can be benchmarked. The relative error
is defined as
\begin{align}
e_{\op} = \frac{\op \left( d_l, d_r \right) }{ d_p },
\end{align}
with $d_l, d_r$ the euclidean distance between the left eye center and its
estimation, and the right eye center and its estimation, respectively.
$d_p$ denotes the euclidean distance between the real eye centers. The operator $\op$
is either $\min$, $\max$, or $\mean(x, y) = \frac{x + y}{2}$. Depending on the
operation, different results are measured. If $\min$ is used, the accuracies
only take the better result of both eyes into account, likewise the
worse eye is used for $\max$. The average error of both eyes is calculated
using the $\mean$ inside the error measurement.
In \Cref{fig:bioid_accuracies} `EyeLike`, @Timm2011, and `PupilLocalization` are
compared using the $\max$ relative error, which makes a lot of sense for
accurate eye tracking. To measure the accuracy, the error $e_{\max}$ is
calculated and the percentage of faces for which the error is below or equal
the thresholds is reported. A comparison of all three different errors, $\min,
\max,$ and $\mean$, can be found in \Cref{tab:BioID-pupil-detection-accuracies}.

\begin{figure}
    \begin{tikzpicture}
        \begin{axis}[xlabel={relative error}, ylabel={accuracy}, domain=0:1, xmin=0, xmax=0.25]
            \addplot[color=blue] table [x=error, y=Timm2011, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
            \addplot[color=red] table [x=error, y=gaze_max_normalized_error, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
            \addplot[color=green] table [x=error, y=eyelike_max_normalized_error, col sep=comma] {assets/gen_files/BioID_accuracy_vs_error.csv};
        \end{axis}
    \end{tikzpicture}
    \caption{\label{fig:bioid_accuracies}Comparison of pupil detection accuracy between Timm and Barth (2011), Hume (2012) and Gaze's \texttt{PupilLocalization} on the BioID dataset. Only the maximum relative error is shown. Refer to \Cref{tab:BioID-pupil-detection-accuracies} for a tabular version of all relative errors.}
\end{figure}

TODO(shoeffner): beautify plot \Cref{fig:bioid_accuracies}

The accuracy of `PupilLocalization` is very good and reaches the same accuracy
as @Timm2011. Inspecting the times in \Cref{tab:comptimes-BioID} it becomes clear that `PupilLocalization` performs faster than the implementation of `EyeLike` on the
BioID dataset with a median computation time of \SI{1.838}{\milli\second},
compared to `EyeLike`'s median computation time of \SI{24.780}{\milli\second}
across the whole dataset. Even the maximum
computation time is still on par, but for `PupilLocalization` this probably
stems from resizing the lookup table. Still, since the eye size is a quadratic
factor in the implementation, the computation time of `PupilLocalization`
changes dramatically with bigger images, while `EyeLike`'s computation times
are relatively stable. This can be seen in \Cref{tab:comptimes-pexels} for the Pexels dataset, which contains
bigger images: The median computation time is
still better for the whole dataset, but while inspecting only results where
both eye patches have a side length of more than \SI{50}{{pixels}}, the size to
which `EyeLike` scales the eye patches to, `EyeLike` outperforms
`PupilLocalization` by a factor of about $4$.

It can be concluded that for real time scenarios with modern image
resolutions `EyeLike` is the better choice, as it is faster with only a small
loss in performance. For accurate processing when time is of no critical
importance, for example during offline analysis of recorded video data, Gaze's
`PupilLocalization` is usually the better option. In general it should be
noted, that with `PupilLocalization` and eyeLike [@Hume2012] there are two successful
replications of the eye center detection approach by @Timm2011. Comparing the
different accuracies per dataset which are listed in \Cref{tab:pexels-pupil-detection-accuracies}
and \Cref{tab:BioID-pupil-detection-accuracies}, it becomes clear that the
algorithm works better with the images from the BioID dataset, but still
performs reasonably well on the pexels dataset.


### Head pose estimation

The head pose estimation works well in most cases. If a subject is looking
straight into the camera, in the extreme case, when the nose points
directly towards the camera and the coronal plane is parallel to the screen
plane, there are two equally likely possible solutions: the $z$ axis pointing
outwards or inwards. In most cases this is not a problem, as it is unlikely
that this happens. But sometimes this causes different results from frame to
frame.
Since there was no annotated ground truth for the datasets used about the head
poses, it is not possible to give a quantitative analysis about the success of
the method, but as was lined out in @sec:head-pose-estimation a qualitative
analysis can be performed. In @sec:head-pose-estimation it is already
established that the +EPnP version of the `solvePnP` algorithm does not work as
well as the iterative version, thus here the difference between the five and
the 68 landmarks models will be shown.

The problem with the 68 landmarks model is, as stated in @sec:license-issues, that it is only allowed for
research usage. As an alternative
the five landmarks model by Dlib was tried using a custom 3D head model.
Unfortunately the 3D head model used in Gaze [@Mallick2016] relies on the six
landmarks pronasal, gnathion, exocanthions left and right, and the cheilions
left and right, which are not all present in the five landmarks model. It uses
the two exocanthions, the subnasal -- the point below the nose -- and the
endocanthions. To be able to estimate a head pose, a
different 3D model is used, Model&nbsp;A in @cl:5lm-model. It is difficult to find
accurate relational measurements for these landmarks, so for the endocanthions
the same model assumption is made as is for the eye ball centers, that they are
offset towards the center by the length of the palpebral fissure [@Facebase].
The subnasal is located using an arbitrary guess backed by the data about the
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
vectors can no longer span three linear independent vectors. A few adjustments
are tried to resolve this issue, for example using Model&nbsp;B in @cl:5lm-model
which just moves the endocanthions about a centimeter outwards of the face.
For some faces like 0031 in @fig:landmarkscomparison this works slightly better, for others like 0044 worse.
It remains unclear whether the five landmarks can be
used with a proper model to estimate head poses accurately, or if the points
really do not contain enough information to properly span three dimensions
between them.


### Gaze point estimation

- gaze tracking not working
- distance, projection problems


## Computation times

@file:assets/gen_files/table-pipeline-step-times.md

@file:assets/gen_files/table-pipeline-times.md


## iTracker

- mobile display limitations
- caffe troublesome
- segfault
- alright under the right circumstances
- "for everyone" vs. research only


## Conclusion

* difficult to get camera parameters
- easy to use software which can be extended and configured
- geometric model is not working
- eye (and pupil) tracking works mostly very well
- other solutions have their own shortcomings, so this is still an open exciting research question
