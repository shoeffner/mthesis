
Table: Accumulated computation times per pipeline configuration.;;Accumulated computation times per pipeline configuration, measured on
the pexels dataset. The `SourceCapture` step is excluded. The other steps are
`FaceLandmarks` (F), `HeadPoseEstimation` (H), `PupilLocalization` (P),
`EyeLike` (E), `GazePointCalculation` (G), and `GazeCapture` (C). All values
are in \si{\micro\second}. \label{tab:pipeline-times}

Pipeline                Median             Max            Mean             Min
-------------- --------------- --------------- --------------- ---------------
Default (FHPG) \num{    63846} \num{  2078141} \num{   185651} \num{    35219}
EyeLike (FHEG) \num{    70142} \num{   121546} \num{    77389} \num{    55375}
iTracker (FC)  \num{    79875} \num{  1820336} \num{   110943} \num{    69975}
