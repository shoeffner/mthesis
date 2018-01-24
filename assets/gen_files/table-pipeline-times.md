
Table: Accumulated computation times per pipeline configuration, measured on
the pexels dataset. The `SourceCapture` step is excluded. The other steps are
`FaceLandmarks` (F), `HeadPoseEstimation` (H), `PupilLocalization` (P),
`EyeLike` (E), `GazePointCalculation` (G), and `GazeCapture` (C). All values
are in \si{\micro\second}. \label{tab:pipeline-times}

Pipeline                Median             Max            Mean             Min
-------------- --------------- --------------- --------------- ---------------
Default (FHPG) \num{    69334} \num{  2064645} \num{   190782} \num{    35706}
EyeLike (FHEG) \num{    70452} \num{   121738} \num{    78097} \num{    56285}
iTracker (FC)  \num{    82407} \num{  1999776} \num{   115440} \num{    70763}
