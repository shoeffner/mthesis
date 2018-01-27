# State of the art

This chapter will outline the current state of the art in eye and gaze tracking
approaches which focus on optical methods, as those are most relevant for this
thesis project.

TODO(shoeffner): better intro section

## Models for eye and gaze tracking


## Commercial gaze tracking solutions

Commercial solutions for gaze tracking come in a great variety. There are
hardware systems with one or multiple cameras, coming with specialized computer
hardware or without, and some having their own software solutions to visualize
and analyze the data recorded with them, while others rely on other software.
Few manufacturers focus on webcam solutions, most built highly
specialized hardware instead. The price ranges vary from
about \eur{100} to prices
beyond \eur{20000} [@Mahler2017; @Biggs2016]. Most commercial gaze trackers
state their accuracy in degrees of visual angle. With an accuracy of
\SI{1}{\deg}, a gaze tracker has an error of about \SI{1}{\centi\meter} at a
viewing distance of \SI{57.3}{\centi\meter}. In this section, only a segment of
available solutions is listed.

In the low end price range of remote gaze trackers there are the cheaper
[Tobii EyeX and Tobii Eye Tracker 4X](https://tobiigaming.com) models, which
are not for research but gaming. With prices of \eur{159} they
currently are the cheapest gaze tracking hardware available. Tobii hardware comes
with a developer kit for Windows computers, and can be purchased either as
standalone gaze trackers or built-in modern gaming laptops. Their only
competitor within the low price class, [The Eye Tribe](http://theeyetribe.com)
which sold trackers for \eur{99} to \usd{199}, was acquired by Oculus
in late 2016 [@Constine2016] and is no longer selling its products on their
website. Still below \eur{1000} are the [GP3](https://gazept.com) if bought
without any software, which raises the price up to \eur{2800}. It has an
accuracy of \SI{0.5}{\deg} to \SI{1}{\deg} and a frame rate of
\SI{60}{Hz}. In the higher price segment for remote gaze tracking, Tobii
offers a frame rate of up to \SI{600}{Hz} with an accuracy of \SI{0.4}{\deg}.
Another remote gaze tracker with up to \SI{1000}{Hz} and a similar
accuracy is the EyeLink 1000 by [SR Research](http://sr-research.com).
[Smart eye](http://smarteye.se) offer multi camera setups for setups with
multiple monitors using up to eight cameras. They have an accuracy of
\SI{0.5}{\deg} and between \SI{60}{Hz} and \SI{120}{Hz}. Another multi camera
setup comes from [LC Technologies](http://eyegaze.com).

For mobile eye tracking [pupil labs](https://pupil-labs.com) offers a unique
solution: All their hardware as well as their software is open source and can
potentially be built manually. They offer their \SI{200}{Hz} gaze tracking
glasses from \eur{1000} and also have add-ons for the Microsoft HoloLens,
an +AR kit, and the HTC Vive, a +VR kit. Another choice for +VR is the
[Fove](https://getfove.com) at \usd{599}, a gaze tracking solution
developed specifically for +VR: They specialize in foveated rendering
[@Patney2016] to improve the performance of graphics renderings in +VR.
But Fove and pupil labs are not the only contenders in the gaze tracking for
+VR and +AR market. [Ergoneers](http://ergoneers.com) sell a hardware kit
which can be adapted to +VR but is also designed to be integrated into helmets.
[SensoMotoric Instruments](https://smivision.com)
offered a wide range of remote, mobile, +AR, and +VR solutions in the higher
price ranges, until they were bought by Apple in 2017 [@Rossignol2017].

Although many hardware manufacturers also ship their own analysis software,
there are independent software companies offering analysis software for gaze
tracking. One such company, [interactive minds](https://interactive-minds.com),
works closely together with the hardware manufacturer LC
Technologies. Other software companies include
[iMotions](https://imotions.com), which offers software for gaze tracking but
also for +EEG, +ECG, and other biometrics. Companies like the [Institut für
Wahrnehmungsforschung](http://institut-fw.de) offer to conduct gaze tracking
studies, they specialized on marketing and advertisment.

A modern +saas approach is done by [Eyezag](https://eyezag.com),
which offers a service to perform gaze tracking for websites using only user
webcams. Similarly the platforms [EyesDecide](https://eyesdecide.com) and the
related [xLabs](https://xlabsgaze.com) offer browser integrations to record,
replay and analyze user gazing behavior on websites by employing webcams.


## Free and open-source webcam gaze tracking software

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

[Opengazer](http://inference.org.uk/opengazer) is a software originally
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
