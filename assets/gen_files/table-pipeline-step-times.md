
Table: The different computation times per pipeline step, measured on the pexels
dataset. All values are in \si{\micro\second}.
Note that all pipeline steps are included although the default pipeline only
uses the first four. \label{tab:pipeline-step-times}

Pipeline step                   Median             Max            Mean             Min
---------------------- --------------- --------------- --------------- ---------------
`FaceLandmarks`        \num{    40556} \num{    90661} \num{    49969} \num{    31985}
`HeadPoseEstimation`   \num{      360} \num{     1606} \num{      385} \num{      211}
`PupilLocalization`    \num{    19427} \num{  1974850} \num{   140395} \num{      145}
`GazePointCalculation` \num{       30} \num{      108} \num{       33} \num{       29}
`EyeLike`              \num{    28473} \num{    35339} \num{    27709} \num{    19840}
`GazeCapture`          \num{    40829} \num{  1949250} \num{    65470} \num{    38142}
