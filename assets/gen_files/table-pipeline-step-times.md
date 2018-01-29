
Table: Computation times per pipeline step.;;The different computation times per pipeline step, measured on the pexels
dataset. All values are in \si{\micro\second}.
Note that all pipeline steps except for the source capture are included,
even though the default pipeline only uses the first four.
\label{tab:pipeline-step-times}

Pipeline step                   Median             Max            Mean             Min
---------------------- --------------- --------------- --------------- ---------------
`FaceLandmarks`        \num{    39694} \num{    92488} \num{    49031} \num{    29581}
`HeadPoseEstimation`   \num{      359} \num{     1677} \num{      391} \num{      206}
`PupilLocalization`    \num{    18028} \num{  1992450} \num{   136196} \num{      133}
`GazePointCalculation` \num{       30} \num{       74} \num{       33} \num{       28}
`EyeLike`              \num{    27708} \num{    36537} \num{    27934} \num{    19044}
`GazeCapture`          \num{    39972} \num{  1767480} \num{    61912} \num{    38398}
