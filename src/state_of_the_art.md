# State of the art

This chapter will outline the current state of the art in eye and gaze tracking
approaches which focus on optical methods, as those are most relevant for this
thesis project.


## Free and open-source software projects for webcam gaze tracking

Several +FOSS projects attempt to perform gaze tracking. They all have
different requirements and use cases: They require webcams, modified webcams,
or depth cameras, and they need either images of the full face or just
of individual eyes. Most projects only track eyes. A comparing overview over
the software presented in this section can be found in \Cref{tab:compgazesoft}.


\begingroup\let\ts\small

Table: Comparison of open source gaze tracking software. Unfortunately not all
could be tested, thus the results rely on the respective author's reports. \label{tab:compgazesoft}

\ts Software and Author                \ts Input            \ts Tracks \ts License
-------------------------------------- -------------------- ---------- ------------------
\ts deepgaze [@Patacchiola2017]        \ts not available    \ts head   \ts MIT
\ts eyeLike [@Hume2012]                \ts Face             \ts eyes   \ts MIT
\ts gazr [@Lemaignan2016]              \ts Face             \ts head   \ts Apache 2.0
\ts iTracker [@Krafka2016]             \ts Face, eyes, mask \ts gaze   \ts Research-only
\ts OpenGazer [@Ferhat2012]            \ts Face             \ts gaze   \ts GPL 2.0
\ts webcam-eyetracker [@Dalmaijer2015] \ts Infrared eye     \ts eyes   \ts GPL 3.0
\ts Webgazer.js [@Papoutsaki2016]      \ts Face             \ts gaze   \ts GPL 3.0
\ts \Gaze{}                            \ts Face             \ts eyes   \ts MIT

\endgroup


The eye tracking implementation [eyeLike](https://github.com/trishume/eyeLike)
by Tristan Hume is the most important work for this thesis. The implementation
uses gradients to detect eye centers [@Timm2011]. It is not suited to be
integrated into other software and can be seen as a reference implementation o
f the eye center detection algorithm. \Gaze{} implements
the same algorithms but tries to provide a more flexible interface.

[Opengazer](http://www.inference.org.uk/opengazer/) is a software originally
developed by Piotr Zieliński which tracks gaze after a few calibration steps
using a normal webcam. It was published in 2010 and last updated in 2013, but a
[fork](https://github.com/tiendan/OpenGazer) of the project was created by Onur
Ferhat in 2014 and maintained until 2016. The fork achieved errors of about \SI{1.5}{\deg},
improving the original project by about \SI{17.5}{{\%}}, and being about
\SI{1}{\deg} short of Tobii X1 Light Eye Trackers [@Ferhat2012].

One of the more prominent examples is [PyGaze](http://pygaze.org), a software
primarily used to perform eye tracking and gaze tracking analysis
[@Dalmaijer2014]. It is written and Python and maintained by Edwin Dalmaijer
and Sebastiaan Mathôt. Since 2015 it features a webcam based pupil tracker
named webcam-eyetracker [@Dalmaijer2015]. It tracks the pupil of one eye and
uses infrared light. Because of that, it is not suitable for all webcams,
as most have a built-in infrared filter -- though for some webcams it is
possible to remove it. It also needs to have specific lighting conditions;
Dalmaijer reports he had to turn off all regular lights when using it.

The package [gazr](https://github.com/severin-lemaignan/gazr) by Séverin
Lemaignan integrates with [+ROS](https://ros.org). It is designed for
human-robot interaction and currently work is done to extend it with gaze
tracking capabilities. So far it performs head pose estimation using webcams or
RGB-D cameras [@Lemaignan2016].

In 2016, Kyle Krafka and his colleagues published the dataset GazeCapture
alongside the pre-trained +cnn iTracker [@Krafka2016]. It performs gaze
tracking using iPhone and iPad cameras. \Gaze{} employs the iTracker +cnn
to compare the geometric model against it, the results are in
@sec:comparison-with-and-brief-review-of-itracker.

Alexandra Papoutsaki enabled online gaze tracking in web browsers using
[WebGazer.js](http://webgazer.cs.brown.edu) [@Papoutsaki2016]. They offer a few
example programs and make it easy to integrate their tool into websites.
WebGazer.js uses the webcam and calibrates the camera by having the subject
clicking a number of times at different screen positions they gaze at.

The Python package [deepgaze](https://github.com/mpatacchiola/deepgaze) by
Massimiliano Patacchiola uses ++cnn to perform various human-computer
interaction tasks. It claims as one of its features to be able to do gaze
tracking, but the current version does not yet offer this functionality.
However, it does perform head pose estimation [@Patacchiola2017]. Since its
publication about the head pose estimation is from 2017, it is possible that
gaze estimation will be added in the future.
