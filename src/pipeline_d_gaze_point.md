## Modeling the eye ball centers

To model an eye ball center, the following simplifying assumptions will be used.

TODO(shoeffner): Motivation?

\newcommand{\ex}{\ensuremath{\mathit{ex}}}
\newcommand{\en}{\ensuremath{\mathit{en}}}

TODO(shoeffner): Move `newcommands` to some common file.

1. The eye ball is an idealized sphere with a radius $r$ of \SI{0.012}{\meter} [@Davson2017] around center $c$.
2. The exocanthion ($\ex$) and endocanthion ($\en$) are located on the surface of the eye ball.
2. The exocanthion and endocanthion differ only in the horizontal dimension.
3. The eye ball center has the same vertical position as the exocanthion and endocathion.
4. The eye ball center has the same horizontal position as the exocanthion and endocanthion.
5. The eye ball center is *behind* the exocanthion and endocanthion, i.e.\ $c_z < \ex_z$.

TODO(shoeffner): Explain *behind*, link to head pose chapter to explain why $ < $ and not $ > $.

\missingfigure{eye ball center schema}

Using $\ex = \left(\ex_x, \ex_y, \ex_z\right)^\top$, $\en = \left(\en_x, \en_y, \en_z\right)^\top$, and $c = \left(c_x, c_y, c_z\right)^\top$ the following equations follow:

\begin{align}
r^2 &= \left(\ex_x - c_x\right)^2 + \left(\ex_y - c_y\right)^2 + \left(\ex_z - c_z\right)^2 = r^2 \label{eq:sphereex} \\
r^2 &= \left(\en_x - c_x\right)^2 + \left(\en_y - c_y\right)^2 + \left(\en_z - c_z\right)^2 = r^2 \label{eq:sphereen} \\
c_x &= \frac{\ex_x + \en_x}{2} \label{eq:cx} \\
c_y &= \ex_y = \en_y \label{eq:cy}
\end{align}

Substituting \eqref{eq:cx} and \eqref{eq:cy} into \eqref{eq:sphereex} (analogue for \eqref{eq:sphereen}) leads to

\begin{equation}
\left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2 + \left(\ex_y - \ex_y\right)^2 + \left(\ex_z - c_z\right)^2 = r^2, \nonumber
\end{equation}

which can be simplified further to

\begin{equation}
\left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2 + \left(\ex_z - c_z\right)^2 = r^2. \label{eq:simplesphereex}
\end{equation}

Solving \eqref{eq:simplesphereex} for $c_z$ yields

\begin{align*}
  \left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2 + \left(\ex_z - c_z\right)^2 &= r^2 \\
  \left(\ex_z - c_z\right)^2 &= r^2 - \left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2 \\
  \ex_z - c_z &= \sqrt{r^2 - \left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2} \\
  c_z &= \ex_z - \sqrt{r^2 - \left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2}
\end{align*}

Thus the eye ball center is:

\begin{equation}
c = \left(\begin{array}{c}
\frac{\ex_x + \en_x}{2} \\
\ex_y \\
\ex_z - \sqrt{r^2 - \left(\ex_x - \frac{\ex_x + \en_x}{2}\right)^2}
\end{array}\right) \label{eq:ebc}
\end{equation}

The face model used to determine the head pose orientation from section ADD\_SECTION is not sufficient to calculate these values as it is missing coordinates for the endocanthions. Employing the above assumptions that the exocanthion and endocanthion differ only in their horizontal components and inserting the mean palpebral fissure length of \SI{0.02819}{\meter} [@Facebase], the face model can be extended by the two points $\en_l$ and $\en_r$:

TODO(shoeffner): Link to head pose section/chapter

\begin{align*}
\en_l &= \ex_l - \left(\begin{array}{c}
    0.02819 \\
    0 \\
    0 \end{array}\right) = \left(\begin{array}{c}
    \phantom{-}0.0433 - 0.02819 \\
    \phantom{-}0.0327 \\
    -0.026 \end{array}\right) = \left(\begin{array}{S}
    0.01511 \\
    0.0327 \\
    -0.026 \end{array}\right) \\
\en_r &= \ex_r + \left(\begin{array}{c}
    0.02819 \\
    0 \\
    0 \end{array}\right) = \left(\begin{array}{S}
    -0.01511 \\
    0.0327 \\
    -0.026 \end{array}\right)
\end{align*}

It remains to substitute all variables into \eqref{eq:ebc} for both eye ball centers $c_l$ and $c_r$ [^simplifyeyecenters] and discarding the solutions with ${c_l}_z > {\ex_l}_z$ and ${c_r}_z > {\ex_r}_z$, respectively.

\begin{align}
c_l &= \left(\begin{array}{S}
0.029205 \\
0.0327 \\
-0.032396
\end{array}\right) \label{eq:ebc_l} \\
c_r &= \left(\begin{array}{S}
-0.029205 \\
0.0327 \\
-0.032396
\end{array}\right) \label{eq:ebc_r}
\end{align}

[^simplifyeyecenters]: Of course it is not important to model the endocanthions explicitly, $\frac{\ex_x + \en_x}{2}$ can easily be found by just adding (or subtracting respectively) half of the mean palpebral fissure length ($p$) to (from) the exocanthion, as that is exactly the middle between the exo- and endocanthion.
