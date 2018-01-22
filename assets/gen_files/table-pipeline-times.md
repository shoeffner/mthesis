
Table: Accumulated computation times per pipeline configuration, measured on
the pexels dataset. The `SourceCapture` step is excluded. The other steps are
`FaceLandmarks` (F), `HeadPoseEstimation` (H), `PupilLocalization` (P),
`EyeLike` (E), `GazePointCalculation` (G), and `GazeCapture` (C). All values
are in \si{\micro\second}. \label{tab:pipeline-times}

Pipeline                Median             Max            Mean             Min
-------------- --------------- --------------- --------------- ---------------
Default (FHPG) \num{    64780} \num{  1973203} \num{   177655} \num{    34174}
EyeLike (FHEG) \num{    67175} \num{   113970} \num{    74412} \num{    56413}
iTracker (FC)  \num{    79293} \num{  1919807} \num{   110566} \num{    70905}
