# Methods and models

\begingroup
\newcommand{\tl}{\mathit{tl}}
\newcommand{\tr}{\mathit{tr}}
\newcommand{\br}{\mathit{br}}

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
line-plane intersection can be expressed using three points of the screen
plane, the eye ball center and the pupil in the same 3D coordinate system. \todo{add note about model=world coordinate system $= R^3$}
Given an eye ball center $c$ and a pupil center $p$, the points on the line
from the eye ball center through the pupil can be described as

\begin{align}
c + (p - c)t,\label{eq:c-p-line}
\end{align}

with $t \in \mathbb{R}$. The points on the screen plane can be described by three screen
corners $\tl, \tr,$ and $\br$, one functioning as the reference point and two as the
directions into which the screen plane extends:

\begin{align}
\tl + (\tr - \tl)u + (\br - \tl)v,\label{eq:screen-plane}
\end{align}

with $u, v \in \mathbb{R}$. The intersection between \Cref{eq:c-p-line} and \Cref{eq:screen-plane} is thus

\begin{align}
c + (p - c)t       &= \tl + (\tr - \tl)u + (\br - \tl)v \\
c + (p - c)t - \tl &= (\tr - \tl)u + (\br - \tl)v \\
c + (p - c)t - \tl &= (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= - (p - c)t + (\tr - \tl)u + (\br - \tl)v \\
c - \tl            &= (c - p)t + (\tr - \tl)u + (\br - \tl)v \label{eq:param-intersection}
\end{align}

Or, in a more concise matrix and vector form with a slightly changed notation, \Cref{eq:param-intersection} can be expressed as

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
\Cref{eq:c-p-line}. This can be done by inverting the $3 \times 3$ matrix, which works as
long as the line is not parallel to the plane, in other words as long as the
line vector stays linear independent to the direction vectors. In practice this should
not happen, as the methods to detect the face and pupils would fail before
these calculations are done.

The difficulty is to find all variables such that \Cref{eq:matrix-intersection}
can be solved.

- gaze has 3d head model
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

\endgroup
