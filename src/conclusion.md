# Results, evaluations and comparisons


## Library implementation

Gaze's goals to be easily integrable, extendable, to be +FOSS, well documented,
and cross-platform are partly fulfilled. While it is sufficiently easy to
integrate Gaze into software (@sec:using-gaze), it is not possible to extend
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

What works well is the pupil center detection [@Timm2011]. Using
the BioID dataset [@Jesorsky2001] and the *relative error* introduced by @Jesorsky2001
the accuracy of Gaze's `PupilLocalization` can be benchmarked. The relative error
is defined as
\begin{align}
e_{\op} = \frac{\op \left( d_l, d_r \right) }{ d_p },
\end{align}
with $d_l, d_r$ the euclidean distance between the left eye center and its
estimation, and the right eye center and its estimation, respectively, and with
$d_p$ the euclidean distance between the real eye centers. The operator $\op$
is either $\min$, $\max$, or $\mean(x, y) = \frac{x + y}{2}$. In
\Cref{fig:bioid_accuracies} `EyeLike`, @Timm2011, and `PupilLocalization` are
compared using the $\max$ relative error. To measure the accuracy,
the error $e_{\max}$ is calculated and the percentage of faces for which the
error is below or equal the thresholds is reported. A comparison of all three
different errors, $\min, \max,$ and $\mean$, can be found in
\Cref{tab:bioid_accuracies}.

\begin{figure}
    \begin{tikzpicture}
        \begin{axis}[xlabel={relative error}, ylabel={accuracy}]
            \addplot[color=blue] table [x=error, y=Timm2011, col sep=comma] {assets/gen_files/bioid_accuracy_vs_error.csv};
            \addplot[color=red] table [x=error, y=gaze_max_normalized_error, col sep=comma] {assets/gen_files/bioid_accuracy_vs_error.csv};
            \addplot[color=green] table [x=error, y=eyelike_max_normalized_error, col sep=comma] {assets/gen_files/bioid_accuracy_vs_error.csv};
        \end{axis}
    \end{tikzpicture}
    \caption{\label{fig:bioid_accuracies}Comparison of pupil detection accuracy between Timm and Barth (2011), Hume (2012) and Gaze's \texttt{PupilLocalization} on the BioID dataset. Only the maximum relative error is shown. Refer to \Cref{tab:bioid_accuracies} for a tabular version of all relative errors.}
\end{figure}

TODO(shoeffner): beautify plot \Cref{fig:bioid_accuracies}

While the accuracy of `PupilLocalization` is very good, `EyeLike` is faster
and, since it always scales images to the same size, has much more predictable
computation times as can be see in \Cref{@tab:comptimes}. Gaze is especially
slow in the beginning and whenever it needs to build up a bigger lookup table,
leading to very high maximum and mean computation times. It can be concluded,
that for real time scenarios `EyeLike` is the better choice as it is faster with
only a small loss in performance. For accurate processing when time is of no
critical importance, for example during offline analysis of recorded video
data, Gaze's `PupilLocalization` is the better option.

TODO: mention times for different image sizes (?)
- gaze tracking not working


### Face detection

- dlib over OpenCV, advantages/shortcomings


### Head pose estimation

- model precision
- Problems will still arise when subjects point their noses directly into the
  camera: In such a case there are two possible solutions for the $z$ axis,
  either pointing outwards or pointing inwards of the head, leading to some false
  estimations.


### Gaze point estimation

- distance, projection problems


## Computation times


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
