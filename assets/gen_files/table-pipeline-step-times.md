
Table: The different computation times per pipeline step, measured on the pexels
dataset. All values are in \si{\micro\second}.
Note that all pipeline steps are included although the default pipeline only
uses the first four. \label{tab:pipeline-step-times}

Pipeline step                   Median             Max            Mean             Min
---------------------- --------------- --------------- --------------- ---------------
`FaceLandmarks`        \num{    38823} \num{    86313} \num{    48247} \num{    32093}
`HeadPoseEstimation`   \num{      332} \num{     1536} \num{      361} \num{      206}
`PupilLocalization`    \num{    18379} \num{  1887190} \num{   129017} \num{      140}
`GazePointCalculation` \num{       29} \num{       72} \num{       30} \num{       28}
`EyeLike`              \num{    25584} \num{    32380} \num{    25774} \num{    18389}
`GazeCapture`          \num{    39316} \num{  1866580} \num{    62319} \num{    38116}
