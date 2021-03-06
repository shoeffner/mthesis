# Methods and models

Estimating the gaze points is done in \Gaze{} using a geometric model realized in a flexible
pipelined architecture. Most pipeline steps consist of smaller models which
solve parts of the gaze estimation problem, others serve for input and
output of the data. This chapter details the models and gives an
overview of \Gaze{}'s architecture. Finally, there will be a short introduction of iTracker, the +cnn trained by @Krafka2016,
an alternative deep learning model for gaze tracking.

\setnowidow\setnoclub

## Geometric model

The goal of the geometric model is to find the gaze points on the screen using ray casts.
A ray cast is performed from an eyeball center through its pupil. The
intersections of the screen plane and the ray casts are the gaze points. A
line--plane intersection [@Wikipedia:lineplaneintersection] can be expressed using three points of the
screen plane, an eyeball center and a pupil in the same 3D coordinate
system.
Given an eyeball center $c \in \Rthree$ and a pupil center $p \in \Rthree$, the points on the line
from the eyeball center through the pupil can be described as
\begin{align}
c + (p - c)t,\label{eq:c-p-line}
\end{align}
with $t \in \mathbb{R}$ shifting points on the line. The points on the screen plane can be described by three screen
corners $\tl, \tr, \br \in \Rthree$, one functioning as the reference point and two as the
directions into which the screen plane extends:
\begin{align}
\tl + (\tr - \tl)u + (\br - \tl)v,\label{eq:screen-plane}
\end{align}
with $u, v \in \mathbb{R}$ shifting points on the plane. The intersection between @eq:c-p-line and @eq:screen-plane is thus
\begin{align}
c + (p - c)t       &= \tl + (\tr - \tl)u + (\br - \tl)v \\
c + (p - c)t - \tl &= (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= - (p - c)t + (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= (c - p)t + (\tr - \tl)u + (\br - \tl)v. \label{eq:param-intersection}
\end{align}
Or, in a more concise matrix and vector form, @eq:param-intersection can be expressed as
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
the direction vectors. In practice this should never be a problem, as the methods to
detect the face and pupils would fail earlier, resulting in these calculations never to be executed.

The difficulty is to find all variables such that @eq:matrix-intersection
can be solved. The following sections will show how the eyeball centers are
determined using a generic 3D head model, followed by how \Gaze{} detects faces
and eyes in an image. The detected face landmarks are used to find the pupil
centers and project them into the 3D model, as well as to estimate the head
pose in relation to the camera. Once the relation to the camera is established,
the distance is estimated to calculate the screen position in the
model coordinate system. The eyeball centers, pupil locations in model
coordinates, and screen corners in model coordinates can be inserted into
@eq:matrix-intersection to find $t$ and calculate the gaze points.
Eventually, the gaze points are converted into target coordinates, for example
the pixels of the screen.


### 3D head model and eyeball centers

The eyeball centers can be modeled as part of a 3D head model which will be
needed to estimate the head pose in relation to the camera. A simplified 3D
head model using six landmarks is proposed by @Mallick2016. The landmarks involved are
the tip of the nose&nbsp;(pronasal), the point at the bottom front of the chin
(gnathion), the two outer corners of the eyes (exocanthions), and the two mouth
corners (cheilions). The 3D model does not use the
metric system but coordinates within "some arbitrary reference frame"
[@Mallick2016]. The model uses the tip of the nose as the origin and spans the
coordinate system parallel to the standard anatomical planes. The $x$ axis is
parallel to the coronal and transverse planes, with the positive values to the
left from the head's perspective. @Mallick2016 uses left and right from the viewer's
perspective. \Gaze{} uses left and right from the head's perspective which is
more in line with @Swennen2006. Thus when looking at the model, the $x$ axis
stretches to the right.
The $z$ axis is parallel to
the transverse plane and lies inside the mid-sagittal plane, pointing away from
the face. The $y$ axis is orthogonal to the $x$ and $z$ axes and points upwards
in relation to the head. \Cref{tab:3dheadmodel} summarizes the model points
and @fig:3dheadlandmarks visualizes the locations and the coordinate system. The
model is converted to the metric system to be useful for \Gaze{} using data from
@Facebase, in particular the mean outer canthal width. This is the width of
the left and right eyes' outer corners, from $\ex_r$ to $\ex_l$. @Facebase
report a mean outer canthal width of \SI{86.71}{\milli\meter}, measured
using 3D stereophotogrammetry and within \num{1845} European Caucasian
individuals above the age of 18. In the 3D model, the outer canthal width is
\num{450}. Since the idealized head model assumes symmetry along the
mid-saggital plane it follows that $\num{225} = \SI{43.355}{\milli\meter}$, or
$\num{1} \approx \SI{0.19269}{\milli\meter}$. This relation can be used to
calculate the metric model, as done in \Cref{tab:3dheadmodel}.

Table: 3D head model by @Mallick2016.;;3D head model by @Mallick2016. The first columns describe the landmark
and name its abbreviation [@Swennen2006], followed by the "300 Faces
In-The-Wild Challenge" index [@Sagonas2016]. Then, the 3D model coordinates are
described as used by \Gaze{} and in the original model.
The eyeball centers are an exception as they are only important for the
ray cast and do not have conventional soft tissue landmark abbreviations nor
model points in the original model. \label{tab:3dheadmodel}

Landmark                Abbr.   Index  \Gaze{} [\si{\milli\meter}]   @Mallick2016
---------------------- ------- ------ ----------------------------- --------------------
Pronasal               $\prn$      31 $(0, 0, 0)$                   $(0, 0, 0)$
Gnathion               $\gn$        9 $(0, -63.6, -12.5)$           $(0, -330, -65)$
Exocanthion right      $\ex_r$     37 $(-43.3, 32.7, -26)$          $(-225, 170, -135)$
Exocanthion left       $\ex_l$     46 $(43.3, 32.7, -26)$           $(225, 170, -135)$
Cheilion right         $\ch_r$     49 $(-28.9, -28.9, -24.1)$       $(-150, -150, -125)$
Cheilion left          $\ch_l$     55 $(28.9, -28.9, -24.1)$        $(150, -150, -125)$
Eye ball center right  ($c_r$)        $(-29.05, 32.7, -39.5)$
Eye ball center left   ($c_l$)        $(29.05, 32.7, -39.5)$

An initial idea to model the eyeball center was to place it at the center
of the palpebral fissure -- the line segment between the inner and outer eye corners, the endocanthion and exocanthion -- and move it
inside the head until the $\ex$ and $\en$
are on the eyeball surface. The problem with this idea is that the mean
palpebral fissure length is \SI{28.19}{\milli\meter} [@Facebase] but the mean
eyeball diameter is much less than that: It is reported to be about \SI{24}{\milli\meter} [@Davson2017], or
\SI{22.0}{\milli\meter} to \SI{24.8}{\milli\meter} [@Bekerman2014]. Instead of
solving the equations with a greater diameter or by accounting for the distance
between the eyeball surface and the $\ex$ and $\en$, the midpoint between
$\ex$ and $\en$ is just moved back along the $z$ axis by
\SI{13.5}{\milli\meter}, which is the furthest distance between the cornea and
the eyeball center [@Gross2008]. The endocanthions are assumed to be on the
same line parallel to the $x$ axis and with a distance of the palpebral fissure
length, \SI{28.19}{\milli\meter} apart from their respective exocanthions. The
eyeball centers are then at $(-29.05, 32.7, -39.5)$&nbsp;\si{\milli\meter} and
$(29.05, 32.7, -39.5)$&nbsp;\si{\milli\meter}.

![Annotation visualization of the 3D head model.;;Annotated visualization of the 3D head model. See \Cref{tab:3dheadmodel} for the values of the marked landmarks. The head model is adapted from pixabay.com and under the CC0 license.](3dheadmodel.png){ #fig:3dheadlandmarks width=35% }


### Detecting faces and eyes

Before finding the pupil centers to project them into the 3D model the face of
the subject needs to be found. There are various methods available,
@Frischholz2018 lists 15 +FOSS libraries providing some sort of face detection
and additionally lists several websites and commercial software able to do the same. One method is to use
OpenCV's pre-trained classifiers, which perform a variant
of Haar feature detection using AdaBoost [@Viola2001]. But this
method, albeit popular, only finds face and eye boundaries, while Dlib also finds useful face landmarks. @King2014 released
a face detector in Dlib which uses five \glslink{hog}{histograms of oriented gradients~(HoGs)} and
+MMOD [@King2015]. \Gaze{} uses Dlib's
classifier because it offers an advantage over OpenCV's classifier: It detects
the 68 landmarks used for the "300 Faces In-The-Wild Challenge" shown in @fig:68landmarks.
These landmarks include the landmarks listed in \Cref{tab:3dheadmodel}, so no
additional processing and detection steps are needed after the face is detected.
@sec:license-issues explains one downside of using Dlib's model, which is licensing.
A possible solution is to use the five landmark model which Dlib offers as an alternative,
but it does not detect all landmarks included in the 3D head model. Also using a
3D head model containing the five instead of the six out of 68 landmarks is not stable
enough for the head pose estimation, which is discussed in more detail in @sec:head-pose-estimation.

Dlib describes detected faces with a bounding box around the detected landmarks
as well as a list of landmark coordinates, ordered as labeled in the "300 Faces
In-The-Wild Challenge" [@Sagonas2016]. The landmarks 37 and 46
in @fig:68landmarks correspond to the $\ex_r$ and $\ex_l$, respectively,
similarly landmarks 40 and 43 denote $\en_r$ and $\en_l$. The eyes are
extracted by placing a rectangle with $\ex$ and $\en$ being opposite corners
and detecting its center. The eye is cropped to a square with a side-length of
1.5 times the distance between the eye corners and centered around the
rectangle's center. To visualize this, examples of processed eyes can be found in the
appendix in @fig:pupildetectioncomparison.

![Facial landmarks described and detected by Dlib.;;The 68 landmarks as detected by Dlib on the left, on the right their original description by
@Sagonas2013. In Dlib, the indexes start with 0. Landmarks schema used
with kind permission by Stefanos Zafeiriou.](68landmarks.png){ #fig:68landmarks }


### Pupil localization

Finding the pupil centers in the eyes is done following @Timm2011, inspired by
the success of @Hume2012. The algorithm they propose assumes that the iris, the
colored part of the eye, is a dark circle on a bright background, the sclera,
which implies that there is a strong gradient at its boundary. The gradient direction at the boundary points from darker to brighter areas, that is towards the sclera. To find the center, all points
within the image of the cropped eye are assigned a value by a target function
and the point with the maximum value is chosen as the pupil center.

The pupil location $p \in \mathbb{N}^2$ in \si{{pixels}} is found by solving [@Timm2011;
adapted from @Hume2012]:
\begin{align}
p = \argmax_{\hat{p}} \left\{
    \frac{1}{N} \sum_{i=1}^{N} w_i \left(
       \max \left\{ \left(
            \frac{x_i - \hat{p}}{\left\lVert x_i - \hat{p} \right\rVert_2}
       \right)^\top \varphi\left(g_i, \vartheta\right), 0 \right\}
    \right)^2
\right\}, \label{eq:targetpupilloc}
\end{align}
where $\hat{p} \in \mathbb{N}^2$ are the potential pupil locations, $x_i \in
\mathbb{N}^2$ are all $N$ pixel locations of the image crop, $w_i \in
\mathbb{R}$ are weights for those pixel locations, $g_i \in \Rtwo$ are
the gradients at each pixel location, respectively, and $\left\lVert
\cdot \right\rVert_2$ is the Euclidean norm. A very important function is
$\varphi$, which is defined as:
\begin{align}
\varphi(x, \vartheta) = \begin{cases}
\frac{x}{\left\lVert x \right\rVert_2} &\quad \text{if } \left\lVert x \right\rVert_2 \ge \vartheta \\
                                     0 &\quad \text{else}
\end{cases} \label{eq:threshphi}
\end{align}
with $\vartheta \in \mathbb{R}$ as the dynamic threshold depending on all gradient magnitudes
\begin{align}
\vartheta = \mu_\text{mag} + \theta \sigma_\text{mag},
\end{align}
employing the mean and standard deviation $\mu_\text{mag}, \sigma_\text{mag}$
over the gradient magnitudes $\text{mag}_i = \left\lVert g_i \right\rVert_2$,
and the model parameter $\theta$, which describes the number of standard
deviations. As explained in @sec:pipeline-steps, in \Gaze{} $\theta$ can be configured and is set
to \num{0.3} by default, following @Hume2012.

So to detect a pupil center first the gradient image of the eye has to be
calculated, for which \Gaze{} uses the standard Sobel filter. Using the gradient
magnitudes and the model parameter $\theta$, a dynamic threshold $\vartheta$
can be calculated to discard all low gradients and normalize those which are
not discarded, as defined in @eq:threshphi. Then, for each possible pupil center location $\hat{p}$,
each other pixel location $x_i$ is used to evaluate the target function: If the
direction from $x_i$ to $\hat{p}$ is similar to the gradient direction $g_i$,
the value will be squared and added to $\hat{p}$'s target value. The similarity
measurement is the scalar product: If the two normalized vectors point in
the same direction, it evaluates to $1$, if they point in the opposite
directions it evaluates to $-1$. @Hume2012 noted that in the paper all these
values were taken into account, but vectors pointing inwards should not be
considered at all. Thus @eq:targetpupilloc discards negative scalar products
instead of squaring them by applying the $\max\left\{\cdot, 0\right\}$ function. The
possible pupil center location which on average has the most directions to
locations which have a gradient pointing into the same or similar directions
will be the winning center point.

Sometimes the gradient method leads to problems where the eye crop has some
wrinkles, shadows, low eyelids, reflections on glasses, or other illumination changes.
@Timm2011 use an inverted Gaussian filtered image to calculate
weights which should give the real pupil higher chances to be selected. The
dark parts of the image -- low gray values -- will thus get higher weights. In
\Gaze{}, where Dlib uses \SI{8}{{bit}} image values, a dark pixel with a
smoothed value of \num{15} would for example get a weight of $255-15=240$.
The extension of discarding vectors facing inwards by @Hume2012 also leads to an
improvement, especially because eyebrows and eyelids no longer hint towards
arbitrary points inside the sclera.

Once the pupil centers are found, they need to be aligned with the 3D model.
To project the pupil centers from image coordinates into model coordinates,
the detected landmarks which correspond to the model points are extended to be
3D coordinates, with their $z$ coordinates being set to 0. The affine
transformation from the landmarks to the model is estimated using OpenCV's
`estimateAffine3D` function. Applying the result transformation to the pupils effectively
moves them into the head model. @fig:pupils3dmodel shows the 3D head model with
pupils and eyeball centers after the transformation.

![Estimated head pose visualization.;;Left: Head pose estimation, the red markers are detected by Dlib and the blue
markers are a projection of the model to visualize the differences. Right: The
cyan pupils and magenta eyeball centers
inside the yellow 3D model. The image was visually enhanced by increasing the
dots and brightening the background.](pupils3dmodel.png){ #fig:pupils3dmodel }


### Head pose estimation

To properly estimate the screen–head relation the head pose needs to be known.
A pose consists of a position or location $(x, y, z) \in
\Rthree$ and an orientation $(\alpha, \beta, \gamma),$ with $\alpha,
\gamma \in \{x \in \mathbb{R} | -\pi < x \leq \pi \},$ and $\beta \in \{x \in
\mathbb{R} | 0 \leq x \leq \pi\}$. Of course, in its own coordinate
system defined above, the head pose is always at $(0, 0, 0)$ with an
orientation of $(0, 0, 0)$. But by estimating the head pose in terms of the
camera coordinate system, it is possible to derive the camera location, which
in turn is fix in relation to the screen. So by knowing the camera location,
the screen corners can be found and used to detect gaze points on the screen.

\widefn

In \Gaze{} head pose estimation is performed closely following the approach
outlined by @Mallick2016. The pose only needs to be estimated indirectly by
describing an affine transformation from the model coordinates to camera
coordinates such that a projection into the image coordinates becomes possible.
This affine transformation can be described using a rotation $R \in
\mathbb{R}^{3 \times 3}$ and a translation $T \in \Rthree$. Adapted from
[OpenCV's documentation](https://docs.opencv.org/3.4.0/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d),
the model
\begin{align}
\left(\begin{array}{c}
p'_x \\
p'_y \\
1 \end{array}\right) &=
C \> P \> \left(\begin{array}{c} \! R\ |\ T \! \end{array}\right) \left(\begin{array}{c}
p_x \\
p_y \\
p_z \\
1 \end{array}\right) \\
&= \left(\begin{array}{ccc}
f_x & 0 & c_x \\
0 & f_y & c_y \\
0 & 0 & 1 \end{array}\right)
\left(\begin{array}{cccc}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \end{array}\right) \left(\begin{array}{cccc}
R_{11} & R_{12} & R_{13} & T_x \\
R_{21} & R_{22} & R_{23} & T_y \\
R_{31} & R_{32} & R_{33} & T_z \\
0 & 0 & 0 & 1 \end{array}\right) \left(\begin{array}{c}
p_x \\
p_y \\
p_z \\
1 \end{array}\right) \label{eq:projmodel}
\end{align}
describes the projection from the 3D model point $p \in \Rthree$ to the 2D
image point $p' \in \Rtwo$, using homogenous coordinates. It uses the camera
matrix $C \in \mathbb{R}^{3 \times 3}$, which can be found via calibration or
approximated by the image size, as presented in @sec:camera-and-screen-parameters. It also uses a
projection matrix $P \in \mathbb{R}^{3 \times 4}$ which reduces the dimensions
from three to two, and the affine transformation from the model coordinate
system into the camera coordinate system. Finding the values for $R$ and $T$ is
called the +PnP problem. There are multiple algorithms to solve +PnP problems. Suitable for six points, as it is the case in \Gaze{}, are +EPnP
[@Lepetit2009] and an iterative approach which uses a
Levenberg--Marquardt optimization [@Levenberg1944; @Marquardt1963; @Wikipedia:lm]. The latter
estimates a hidden parameter set $\beta$ as an approximation $\hat\beta$ such
that
\begin{align}
\hat\beta = \argmin_\beta \left\{ \sum_{i=1}^N \left\lVert p_i' - f(p_i, \beta) \right\rVert_2^2 \right\},
\end{align}
where $\beta$ are the values of $R$ and $T$ in @eq:projmodel, and $f(p_i, \beta)$ is the
estimated projection of a model point $p_i$. Once found, the
parameters can be used together with the distance estimation
from @sec:distance-estimation to estimate the screen corners
as described in @sec:calculation-of-screen-corners. In \Gaze{} the Levenberg--Marquardt
optimization is used because it subjectively performs slightly better when
subjects face the camera more directly, while the +EPnP becomes better when
subjects turn their heads. A comparison is shown in @fig:solvepnpcomparison.
Since for gaze tracking subjects look roughly towards the camera, it is more important to
estimate frontal images more accurately.

\stopwidefn

### Distance estimation

In general, to estimate the distance between an object and a
camera from an image, it is important to know the real size of the
object, the sensor size, the resolution, and the focal length. By using the
intercept theorem and the pinhole camera model, the distance to an object can
be determined. Let $o \in \mathbb{R}$ be the width of the object, $d \in
\mathbb{R}$ be the distance between the image plane and the object, $f \in
\mathbb{R}$ the focal length, $i \in \mathbb{R}$ the object's size on the
image, and $p \in \mathbb{R}$ the pixel width. Then, the distance can be expressed as
\begin{align}
d = \frac{fo}{i}. \label{eq:distanceest}
\end{align}
Assume the sensor size to be \SI{0.00635}{\meter} and its aspect ratio as 16:9
[@Luepke2005, for an Apple iSight]. In that case, the sensor width $s \in \mathbb{R}$ is
\SI{0.0055}{\meter}. The pixel width $p$ can be found through division of the
sensor width by the horizontal resolution, $w \in \mathbb{N}$, so $p =
\frac{s}{w}$.
In \Gaze{}, the outer canthal width is used to determine the distance. It's model
size $o$ is
\begin{align}
\left\lVert \ex_r - \ex_l \right\rVert_2 =
\left\lVert \left( \begin{array}{S}
-0.0433 \\
 0.0327 \\
-0.026 \end{array} \right) - \left( \begin{array}{S}
 0.0433 \\
 0.0327 \\
-0.026 \end{array} \right) \right\rVert_2 = \SI{0.0866}{\meter}.
\end{align}
The outer canthal width in the image $i$ is the distance between the landmarks 37
and 46, which is detected by Dlib. It has to be multiplied by $p$ to get its
width in \si{\meter}. Thus, to determine $d$, the only missing
value is $f$. An approximation for $f$ can be measured, for a MacBook Pro with
the assumption of the above mentioned sensor size it is about
\SI{0.01}{\meter}, which is found using the procedure in @sec:determining-the-focal-length.
Substituting all variables into @eq:distanceest leads to
\begin{align}
d = \frac{fo}{i} = \frac{\SI{0.01}{\meter} \cdot \SI{0.0866}{\meter}}{i \si{pixels} \cdot \SI{0.0055}{\meter/{pixels}}} = \frac{\num{0.1575}}{i}\si{\meter}.
\end{align}
This can be used as an approximate distance measure, it is however only accurate
if the head is parallel to the camera. For the purpose of this thesis, this
should be sufficient.


### Calculation of screen corners

The camera marks the origin of the camera coordinate system. A transformation
between the model coordinate system and the camera coordinate system is found
by solving the +PnP problem in @sec:head-pose-estimation. To express the camera in model
coordinates it is moved back into the translation direction, facing the model
origin. Since the transformation gained from solving the +PnP problem is not taking the distance
into account, the translation needs to be adjusted by normalizing it and then
multiplying it by the estimated distance. Thus, the camera position $\mathit{cam} \in
\Rthree$ in model coordinates is
\begin{align}
\mathit{cam} = \frac{-R^\top T}{\left\lVert -R^\top T \right\rVert_2} d.
\end{align}
The screen corners can be calculated by first defining them inside the
model coordinate system and then performing almost the same transformation as
was done for the camera. To get the first screen corner, the offset between the
camera and the top left corner of the screen needs to be measured manually. For example, for
a MacBook Pro with a 15-inch screen the top left corner is
\SI{17.25}{\centi\meter} left of and \SI{0.7}{\centi\meter} below the camera,
so it can be defined as $\tl_\text{model} = (-0.1725, 0.007, 0)$. From there each other screen
corner can be found by adding screen width and height where appropriate,
for example, the bottom right corner would be
$\br_\text{model} = (-0.1725, 0.007, 0) + (0.335, 0.207, 0) = (0.175, 0.214, 0).$ The screen
corners need to be rotated about the model origin, again using the transposed
rotation. After that, they have to be translated by the camera
coordinates, since they were defined relative to the camera. So for screen
corner $\tl$ the transformation is:
$\tl = R^\top \tl_\text{model} + \mathit{cam}.$


## Implementation as a software library

To implement the model and make it usable, it is realized in the
software library \Gaze{}, which sets the goals to be

- easy to integrate into other projects,
- easy to extend,
- free and open source,
- well documented,
- and available on multiple platforms.

\Gaze{} is written in C++ and compiles into a static library to be easily
integrable into other projects. It uses CMake which is used in many C++
projects and thus it should be widely known.
C++ was specifically chosen because it can often be integrated into other
programming languages since many languages already provide mechanisms to call
for example system libraries, which are often written in C or C++. Another
reason is that OpenCV and Dlib are natively written in C++, and while both have
Python bindings, in general their C++ documentation is much more
comprehensible. One important aspect of making \Gaze{} integrable is the +API
design. By first recreating an eye tracking experiment [@Judd2009] and finding
out what the needs for such an experiment are, \Gaze{} is developed around a very
simple API. Extendability is given by a modular design. \Gaze{} builds around a
multi-purpose data processing pipeline in which each step performs a small
task. It is taken great care to allow for simple extensions using custom steps, for which instructions are provided in
@sec:writing-a-custom-pipeline-step. One step towards easy extension is
also making the source code available for free and as open source software.
This way everyone can inspect it, reproduce the results of this thesis and
extend \Gaze{}, criticize it, modify it, or build upon it. These are the reasons
why publishing the source code and software alongside scientific contributions
is very crucial in science [@Barnes2010]. To make it easy to do anything of the above
with \Gaze{}, it tries to follow many good practices and provides a thorough
documentation.


### Library architecture

\Gaze{} has three threads which loosely interact with each other if needed through
an event system. The first thread is the calling program's main thread. If a
program integrates \Gaze{}, it needs to create a `GazeTracker` object and
interacts with it. The `GazeTracker` object starts two additional
threads. This is done so that the calls from the main program to \Gaze{} are fast
and do not interfere with the main program's execution.
The second thread is the GUI event thread. This thread is only
used if \Gaze{}'s debug window is started and uses Dlib's GUI capabilities. The
third thread is the most important part of \Gaze{}: The pipeline. The pipeline
thread is always started and processes the data in the background by creating a
new data object and passing it from one pipeline step to the next.
Whenever an object passed the pipeline, an event is emitted to notify the GUI
and the main thread. The main thread can then store the latest tracking results
to provide seamless access inside feedback loops and the GUI can retrieve the latest
data to update its visualizations.

Each pipeline step follows the same interface
and has to implement two methods: `void process(util::Data&)` and
`void visualize(util::Data&)`. The process method mutates the data
object by performing some calculations and storing the result back. By
convention, each step should not overwrite the results of other steps, but if
two steps perform the same task, this becomes almost inevitable. Each pipeline
step's execution time is measured and stored inside the data object. To
visualize the data, each pipeline step initializes a GUI widget into which data
can be written. The GUI calls the visualize methods only for one step at a
time, as it only visualizes one step at a time.


## An alternative approach: iTracker

As an alternative approach to the geometric model presented above, a pre-trained
+CNN [@Krafka2016] is used for a comparison. It is called iTracker and trained on their
dataset GazeCapture, which contains data of \num{1450} subjects, or about 2.5
million frames. @Krafka2016 make their models publicly
[available](https://github.com/CSAILVision/GazeCapture) on GitHub.
Their network consists of four parts, one per detected eye, one for the face,
and a face grid, which is a binary representation of where the face of a
subject is located in respect to the original image. All the information except
for the face grid is already used inside the geometric model, so it only needs
to be adjusted to fit the input layers of the network. ITracker is implemented
in [Caffe](http://caffe.berkeleyvision.org) [@Jia2014], which can be
integrated into C++ programs. One disadvantage of iTracker is, that it is only
trained on iPhones and iPads.


## Datasets

Some datasets were needed during the development and tests for \Gaze{}. While
for most ad hoc tests the webcam live stream is enough, it is not enough to
allow for reproducibility of the results.

\begingroup \DFNtrysingle \DFNinhibitcbreak

The first dataset, Pexels, is a custom dataset with 120 images from
[Pexels](https://pexels.com). The
images are rescaled so that all are \SI{640}{{pixels}} wide. After resizing,
the smallest image measures \linebreak \SI{640x332}{{pixels}}, the biggest
\SI{640x1137}{{pixels}}. Most images are portrait photographs using different
backgrounds, poses, facial expressions, lighting conditions, and more. The
majority of images are color images and contain a single person's face, with
few exceptions to this rule, like are partial faces, full body
photographs, multiple people, or cats. The people in the images are of
different sexes, ages, and colors, but with about 71 the vast majority are young white
females. Another 20 people are young white males. Only a handful of
people appear to be older than 50, and only about 10 people are of other
ethnicities. Less than five people appear in more than one
picture. Note that all numbers are only approximate counts to get an idea
of the dataset, as the age is always difficult to guess and even sex and skin
color can become difficult depending on pose, lighting, or accessories.
A few example faces can be seen in @fig:examplefaces. Because the dataset was
downloaded for this thesis and is
used to evaluate the results of the eye center detection, they are annotated by hand.
The annotations and scaled images can be found as supplementary material at the
[thesis' GitHub repository][GITHUBARCHIVELINK]. A script is provided inside the
thesis' code repository to download the original images and perform the
annotations.

[GITHUBARCHIVELINK]: https://github.com/shoeffner/mthesis/releases/download/thesis.shoeffner/PexelsDataset.zip

\endgroup

To compare the pupil detection with the original implementations referenced in
@sec:pupil-localization-evaluation, the [BioID
dataset](https://www.bioid.com/facedb) [@Jesorsky2001] is used.
It contains 1521 gray images with a fixed resolution of \SI{384x286}{{pixels}}.
The BioID dataset features only 23 different people with multiple images of
each. Thirty arbitrary example photos can be found in @fig:bioid_examples.
The dataset is often used to compare face and pupil detection algorithms [@Timm2011]
and \Gaze{}'s implementation is compared to the original implementation by
@Timm2011.

As described in @sec:an-alternative-approach-itracker, the iTracker is trained
using the GazeCapture dataset [@Krafka2016]. It includes photos of \num{1450} subjects
and almost 2.5 million frames. Unfortunately, the download of the raw data is
hidden behind a registration, but @Krafka2016 describe the dataset thoroughly
and give some example images. The data was recorded using iPhones and iPads and
contains images featuring various backgrounds, head poses, accessories, and
lighting conditions.

The remaining datasets are those Dlib's shape detectors are based on. One is
the "300 Faces In-The-Wild Challenge" dataset, which consists of
600 images with 68 landmark annotations, which were produced
semi-automatically. The other dataset is the *dlib 5-point face landmark
dataset*, containing 7198 faces. It was labeled using only five landmarks by King.
Both datasets are only used indirectly in \Gaze{}, as only the models are used
to track facial landmarks and determine the head pose.
