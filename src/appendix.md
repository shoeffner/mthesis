\appendix


# Figures

![Some example faces used to visualize or compare different pipeline steps. The numbers refer to the image names inside `tests/assets/pexel_faces`](pupil_detection_faces.png){ #fig:examplefaces }

![Comparison of eyeLike (top) and Gaze's pupil detections. The original images can be seen in \Cref{fig:examplefaces}. Note that bigger cross markers mean smaller eye image crops.](pupil_detection_comparison.png){ #fig:pupildetectioncomparison }

![Comparison of the solutions to the +PnP problem using +EPnP (left) and the iterative Levenberg--Marquardt optimization (right) in OpenCV's solvePnP function.](solvePnPcomparison.png){ #fig:solvepnpcomparison }


# Code Listings

```{ .cpp file=assets/examples/pipeline_steps/new_step.h label=cl:newsteph caption="The template header for a new pipeline step. The names are modified to match the file name (`MY_STEP` becomes `NEW_STEP` in this example)." pathdepth=2 }
```


# References
\begingroup\endgroup
