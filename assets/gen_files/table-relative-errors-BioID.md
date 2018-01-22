
Table: Different accuracies per relative error thresholds on the BioID
dataset. While @Timm2011 provide a graph of their results, only their $\max$
values are reported. \label{tab:BioID-pupil-detection-accuracies}

Error type                       Method               0.05  0.10  0.15  0.20  0.25
-------------------------------- ------------------- ----- ----- ----- ----- -----
\multirow{3}{*}{$\max$}          `EyeLike`           0.354 0.828 0.882 0.896 0.919
                                 `PupilLocalization` 0.764 0.937 0.962 0.980 0.995
                                 [@Timm2011]         0.825 0.934 0.952 0.964 0.980
\midrule\multirow{2}{*}{$\mean$} `EyeLike`           0.524 0.863 0.914 0.968 0.982
                                 `PupilLocalization` 0.870 0.963 0.992 1.000 1.000
\midrule\multirow{2}{*}{$\min$}  `EyeLike`           0.702 0.960 0.974 0.977 0.987
                                 `PupilLocalization` 0.949 0.991 0.997 1.000 1.000

