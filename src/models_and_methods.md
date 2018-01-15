# Methods and models

TODO(shoeffner): make globally available by moving them to the header-includes?

Estimating gaze is done in Gaze using a geometric model realized in a flexible
pipelined architecture. Most pipeline steps consist of smaller models which
solve parts of the gaze estimation problem, others serve for input and
output[^iopipeline] of the data. This chapter details the models and gives an
overview of Gaze's architecture. Finally there will be a short introduction of
an alternative deep learning model for gaze tracking.


## Geometric model

The goal of the geometric model is to detect the pupil centers of both eyes and
perform a raycast from the eye ball centers through the pupils. The
intersections of the screen plane and the raycast are the gaze points. The
line--plane intersection (formulae adapted from
@Wikipedia:lineplaneintersection) can be expressed using three points of the
screen plane, the eye ball center and the pupil in the same 3D coordinate
system.
Given an eye ball center $c$ and a pupil center $p$, $c, p \in \Rthree$, the points on the line
from the eye ball center through the pupil can be described as

\begin{align}
c + (p - c)t,\label{eq:c-p-line}
\end{align}

with $t \in \mathbb{R}$. The points on the screen plane can be described by three screen
corners $\tl, \tr, \br \in \Rthree$, one functioning as the reference point and two as the
directions into which the screen plane extends:

\begin{align}
\tl + (\tr - \tl)u + (\br - \tl)v,\label{eq:screen-plane}
\end{align}

with $u, v \in \mathbb{R}$. The intersection between @eq:c-p-line and @eq:screen-plane is thus

\begin{align}
c + (p - c)t       &= \tl + (\tr - \tl)u + (\br - \tl)v \\
c + (p - c)t - \tl &= (\tr - \tl)u + (\br - \tl)v \\
c + (p - c)t - \tl &= (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= - (p - c)t + (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= (c - p)t + (\tr - \tl)u + (\br - \tl)v \label{eq:param-intersection}
\end{align}

Or, in a more concise matrix and vector form with a slightly changed notation, @eq:param-intersection can be expressed as

\begin{align}
\left(\begin{array}{c}
c_x - \tl_x \\
c_y - \tl_y \\
c_z - \tl_z \end{array}\right) =
\left(\begin{array}{ccc}
c_x - p_x & \tr_x - \tl_x & \br_x - \tl_x \\
c_y - p_y & \tr_y - \tl_y & \br_y - \tl_y \\
c_z - p_z & \tr_z - \tl_z & \br_z - \tl_z \end{array}\right)
\left(\begin{array}{c}
t \\
u \\
v \end{array}\right). \label{eq:matrix-intersection}
\end{align}

To find the intersection, this matrix equation needs to be solved for $t$ so
that the intersection can be calculated by inserting $t$ into
@eq:c-p-line, for both eyes independently. This can be done by inverting
the $3 \times 3$ matrix, which works as long as the line is not parallel to the
plane, in other words as long as the line vector stays linear independent to
the direction vectors. In practice this should not happen, as the methods to
detect the face and pupils would fail before these calculations are done.

The difficulty is to find all variables such that @eq:matrix-intersection
can be solved. The following sections will show how the eye ball centers are
determined using a generic 3D head model, followed by how Gaze detects faces
and eyes in an image. The detected face landmarks are used to find the pupil
centers and project them into the 3D model, as well as to estimate the head
pose in relation to the camera. Once the relation to the camera is established,
a distance estimate is performed to calculate the screen position in the
model coordinate system. The eye ball centers, pupil locations in model
coordinates, and screen corners in model coordinates can be inserted into
@eq:matrix-intersection to find $t$ and calculate the gaze points.
Eventually the gaze points are converted into target coordinates, for example
the pixels of the screen.


### 3D head model and eye ball centers

The eye ball centers can be modeled as part of a 3D head model which will be
needed to estimate the head pose in relation to the camera. A simplified 3D
head model using six landmarks is proposed by @Mallick2016. It does not use the
metric system but coordinates within "some arbitrary reference frame"
[@Mallick2016]. The model uses the nose tip as the origin and spans the
coordinate system parallel to the standard anatomical planes. The $x$ axis is
parallel to the coronal and transverse planes, with the positive values to the
left from the head's perspective[^xdirectiondiff]. The $z$ axis is parallel to
the transverse plane and lies inside the mid-sagittal plane, pointing away from
the face. The $y$ axis is orthogonal to the $x$ and $z$ axes, it points upwards
(in relation to the head). \Cref{tab:3dheadmodel} summarizes the data points
and @fig:3dheadlandmarks visualizes the locations and coordinate system. The
model is converted to the metric system to be useful for Gaze using data from
@Facebase, in particular the mean outercanthal width (that is the width from
the left and right eyes outer corners, or from $\ex_r$ to $\ex_l$). @Facebase
report data a mean outercanthal width of \SI{86.71}{\milli\meter}, measured
using 3D stereophotogrammetry and within \num{1845} european caucasian
individuals above the age of 18. In the 3D model, the outercantal width is
\num{450}. Since the idealized head model assumes symmetry along the
mid-saggital plane it follows that $\num{225} = \SI{43.355}{\milli\meter}$, or
$\num{1} \approx \SI{0.19269}{\milli\meter}$.  This relation can be used to
calculate the metric model, as it is done in \Cref{tab:3dheadmodel}.

[^xdirectiondiff]: @Mallick2016 uses left and right from the viewers
  perspective. Gaze uses left and right from the head's perspective which is
  more in line with @Swennen2006. Thus when looking at the model, the $x$ axis
  go to the right.

Table: 3D head model by @Mallick2016. The first columns describe the landmark
and names its abbreviation [@Swennen2006], followed by the "300 Faces
In-The-Wild Challenge" index [@Sagonas2016]. Then the 3D model coordinates are
described as used by Gaze and in the original model.
The eye ball centers are an exception as they are only important for the
raycast and do not have conventional soft tissue landmark abbreviations nor
model points in the original model. \label{tab:3dheadmodel}

Landmark                Abbr.   Index  Gaze (\si{\milli\meter})   @Mallick2016
---------------------- ------- ------ -------------------------- --------------------
Pronasal               $\prn$      31 $(0, 0, 0)$                $(0, 0, 0)$
Gnathion               $\gn$        9 $(0, -63.6, -12.5)$        $(0, -330, -65)$
Exocanthion right      $\ex_r$     37 $(-43.3, 32.7, -26)$       $(-225, 170, -135)$
Exocanthion left       $\ex_l$     46 $(43.3, 32.7, -26)$        $(225, 170, -135)$
Cheilion right         $\ch_r$     49 $(-28.9, -28.9, -24.1)$    $(-150, -150, -125)$
Cheilion left          $\ch_l$     55 $(28.9, -28.9, -24.1)$     $(150, -150, -125)$
Eye ball center right  ($c_r$)        $(-29.05, 32.7, -39.5)$
Eye ball center left   ($c_l$)        $(29.05, 32.7, -39.5)$

An initial idea to model the eye ball center was to use place it at the center
of the palpebral fissure (the distance between both eye corners) and move it
inside the head until the $\ex$ and $\en$ (endocanthion, the inner eye corner)
are on the eye ball surface. The problem with this idea is that the mean
palpebral fissure length is \SI{28.19}{\milli\meter} [@Facebase] but the mean
eye ball diameter is much less than that (\SI{24}{\milli\meter} [@Davson2017],
\SI{22.0}{\milli\meter} to \SI{24.8}{\milli\meter} [@Bekerman2014]). Instead of
solving the equations with a greater diameter or by accounting for the distance
between the eye ball surface and the $\ex$ and $\en$, the mid point between
$\ex$ and $\en$ is just moved back along the $z$ axis by
\SI{13.5}{\milli\meter}, which is the furthest distance between the cornea and
the eye ball center [@Gross2008]. The endocanthions are assumed to be on the
same line parallel to the $x$ axis and with a distance of the palpebral fissure
length, \SI{28.19}{\milli\meter} apart from their respective exocanthions. The
eye ball centers are then at $(-29.05, 32.7, -39.5)$&nbsp;\si{\milli\meter} and
$(29.05, 32.7, -39.5)$&nbsp;\si{\milli\meter}.

![Annotated visualization of the 3D head model. See \Cref{tab:3dheadmodel} for the values of the marked landmarks.](missingfigure){ #fig:3dheadlandmarks }


### Detecting faces and eyes

Before finding the pupil centers to project them into the 3D model the face of
the subject needs to be found. There are various methods available,
@Frischholz2018 lists 15 +FOSS libraries providing some sort of face detection,
and additional lists of websites and commercial softwares. One method is to use
[OpenCV's](https://opencv.org) pre-trained classifiers, which perform a variant
of haar feature detection using AdaBoost (Based on @Viola2001). But this
method, albeit popular, only finds face and eye boundaries. @King2014 released
a face detector in [Dlib](https://dlib.net) which uses five +HoG models and
+MMOD [@King2015]. While outperforming OpenCV with a much lower false alarm
rate [@King2014], OpenCV's classifiers were slightly faster when implemented in
Gaze. Processing an image of size \SI{640x360}{{pixels}} took about
\SI{130}{\milli\second} to \SI{140}{\milli\second} using OpenCV and about
\SI{160}{\milli\second} to \SI{170}{\milli\second} using Dlib. Gaze uses Dlib's
classifier because it offers an advantage over OpenCV's classifier: It detects
the 68 landmarks used for the "300 Faces In-The-Wild Challenge" [@Sagonas2013] (@fig:68landmarks).
These landmarks include the landmarks listed in \Cref{tab:3dheadmodel}, so no
additional processing and detection step is needed after the face is detected.
There is one downside to using Dlib, which is licensing
(@sec:licensing-issues). A possible solution is to use the 5 landmark model,
but it does not detect all landmarks included in the 3D head model, and using a
3D head model containing the five instead of the 68 landmarks was not stable
enough for the head pose estimation (@sec:head-pose-estimation).

Dlib describes detected faces with a bounding box around the detected landmarks
as well as a list of landmark coordinates, ordered as labeled in the "300 Faces
In-The-Wild Challenge" [@Sagonas2016, \Cref{tab:3dheadmodel}].



### Head pose estimation


- find distance between screen and head
- find transformation between model and image
    - find relation between head and screen
- find transformation from screen to face




## Library architecture


### Input: source capture

The first pipeline step uses
[`cv::VideoCapture`](https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html)
to capture the input specified inside the `gaze.yaml`.


[^iopipeline]: As of writing, no special output writers are implemented, but
  the infrastructure exists.



- steps:
  - source capture
  - face/eye detection
  - head pose estimation
  - pupil detection
  - gaze estimation
- architecture/design (better move this to models and methods somehow)


## An alternative approach: GazeCapture
