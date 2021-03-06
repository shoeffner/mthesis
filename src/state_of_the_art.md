# State of the art

This chapter will outline the current state of the art in eye and gaze tracking
approaches which focus on video-oculography, as those are most relevant for this
thesis. First, a few of the models for gaze tracking are presented, covering
pupil localization, head pose estimation, and gaze point estimation. Then,
commercial gaze tracking solutions will be presented, covering examples for
remote, mobile and +VR gaze trackers, but also some webcam gaze trackers and
some analysis software. It is important to note that although they are coined *gaze*
tracking solutions here, which they are, most are marketed simply as *eye*
tracking solutions. After
a brief coverage of the commercial solutions, a number of +FOSS projects will
be compared. Almost all of them focus on webcam based gaze tracking, which is
what this thesis aims to achieve as well.


## Models for eye and gaze tracking

Video-oculography tracking essentially requires two kinds of models, one model to
detect pupil centers and one model to estimate the gaze point. Since in this
thesis subjects are supposed to be able to move their head freely, a third
model to estimate the head pose is needed. In this section, a few models for
these purposes will be briefly reviewed. For an in-depth review of some of
these and many other models, please refer to @Hansen2010, who compiled a
detailed review of eye and gaze models.

For pupil detection, it is in general possible to distinguish between shape- and
appearance-based models [@Hansen2010], most of them work on image patches
containing the eyes and a small area around them. Shape-based models assume the iris
as a circular object and optionally add ellipses around it to model the
sclera or eyelids. Some of those methods use a circular Hough transform to find
the pupil centers [@Soltany2011; @George2016]. Other models perform local fits
of circles or ellipses into the image using expectation maximization or random
sample consensus to detect the eyes or pupils [@Li2005; @Hansen2005].
Appearance-based models search for other image features, such as color to
discard the white sclera in different color spaces [@Periketi2011]. Others
discard eye center candidate pixels if they have high entropy, stating that the
sclera's blood vessels and illumination differences lead to it [@Fini2011].
Machine learning models like support vector machines are another method
to detect facial features like eyes [@Park2002]. This thesis will build on a
feature-based approach using the gradients pointing from a dark iris towards a
bright sclera as indicators for eye centers [@Timm2011].

To estimate the gaze point many models use infrared light and track the
first Purkinje image, which is the reflection of the light source on the cornea
[@Ohno2004]. Others use multiple cameras to estimate the 3D head pose and
approximate the eyeball centers to cast rays from the eyeballs through
detected pupils [@Newman2000]. Many methods for gaze estimation require some
kind of calibration [@Hansen2010], but some research is also done to use
calibration-free methods, for example using Gaussian mixture models
[@Xiong2014] or geometric calculations [@Nagamatsu2009]. However, the
calibration free methods apply some constraints. @Xiong2014 only distinguished
between left and right, and @Nagamatsu2009 used a chinrest to avoid head
movements and to keep the head in focus of four cameras.

Face detection is an old problem in computer vision with a popular
solution of applying Haar features to detect faces [@Viola2001]. The "300 Faces
In-The-Wild Challenge" [@Sagonas2013; @Sagonas2016] sparked broad interest in
improving the state of the art. For the challenge, which took place twice,
@Sagonas2013 proposed a unified landmark scheme to compare detection results.
As a side effect, all methods relying on those landmarks provide simple means to
extract image patches containing the eyes, which can then be used for further
processing with one of the many methods for pupil detections mentioned above.
This removes the need to detect the eyes specifically, as is for example done
by @Sirohey2001.
The most successful contributions to the "300 Faces In-The-Wild Challenge" in
both installments rely on ++cnn [@Zhou2013; @Fan2016].


## Commercial gaze tracking solutions

Commercial solutions for gaze tracking come in a great variety. There are
hardware systems with one or multiple cameras, coming with specialized computer
hardware or without, and some having their own software solutions to visualize
and analyze the data recorded with them, while others rely on other software.
Few manufacturers focus on webcam solutions, most built highly
specialized hardware instead. The prices range from
about \eur{100} to prices
beyond \eur{20000} [@Mahler2017; @Biggs2016]. Most commercial gaze trackers
state their accuracy in degrees of visual angle. With an accuracy of
\ang{1}, a gaze tracker has an error of about \SI{1}{\centi\meter} at a
viewing distance of \SI{57.3}{\centi\meter}. In this section, only a segment of
available solutions is listed.

In the low-end price range of remote gaze trackers, there are the cheaper
[Tobii EyeX and Tobii Eye Tracker 4X](https://tobiigaming.com) models, which
are not for research but gaming. With prices of \eur{159}, they
currently are the cheapest gaze tracking hardware available. Tobii hardware comes
with a developer kit for Windows computers and can be purchased either as
standalone gaze trackers or built-in modern gaming laptops. Their only
competitor within the low price class, [The Eye Tribe](http://theeyetribe.com)
which sold trackers for \eur{99} to \usd{199}, was acquired by Oculus
in late 2016 [@Constine2016] and is no longer selling its products on their
website. Still below \eur{1000} are the [GP3](https://gazept.com) if bought
without any software, which raises the price up to \eur{2800}. It has an
accuracy of \ang{0.5} to \ang{1} and a frame rate of
\SI{60}{Hz}. In the higher price segment for remote gaze tracking, Tobii
offers a frame rate of up to \SI{600}{Hz} with an accuracy of \ang{0.4}.
Another remote gaze tracker with up to \SI{1000}{Hz} and a similar
accuracy is the EyeLink 1000 by [SR Research](http://sr-research.com).
[Smart eye](http://smarteye.se) offer multi-camera setups for setups with
multiple monitors using up to eight cameras. They have an accuracy of
\ang{0.5} and between \SI{60}{Hz} and \SI{120}{Hz}. Another multi-camera
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
studies, they specialized in marketing and advertisement.

A modern +saas approach is done by [Eyezag](https://eyezag.com),
which offers a service to perform gaze tracking for websites, only using user
webcams. Similarly the platforms [EyesDecide](https://eyesdecide.com) and the
related [xLabs](https://xlabsgaze.com) offer browser integrations to record,
replay and analyze user gazing behavior on websites by employing webcams.


## Free and open-source webcam gaze tracking software

Several +FOSS projects attempt to perform gaze tracking. They all have
different requirements and use cases: They require webcams, modified webcams,
or depth cameras and they need either images of the full face or
of individual eyes. Most projects only track eyes. A comparing overview over
the software presented in this section can be found in \Cref{tab:compgazesoft}.

The eye tracking implementation [eyeLike](https://github.com/trishume/eyeLike)
by Tristan Hume is the most important work for this thesis. The implementation
uses gradients to detect eye centers [@Timm2011]. It is not suited to be
integrated into other software and can be seen as a reference implementation of
the eye center detection algorithm. \Gaze{} implements
the same algorithms but provides a more flexible interface.

\begingroup\let\ts\normalsize

Table: Comparison of open source gaze tracking software.;;Comparison of open source gaze tracking software. Unfortunately, not all
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

[Opengazer](http://inference.org.uk/opengazer) is a software originally
developed by Piotr Zieliński which tracks gaze after a few calibration steps
using a normal webcam. It was published in 2010 and last updated in 2013, but a
[fork](https://github.com/tiendan/OpenGazer) of the project was created by Onur
Ferhat in 2013 and maintained until 2016. The fork achieved errors of about \ang{1.5},
improving the original project by about \SI{17.5}{{\%}}, and being about
\ang{1} short of Tobii X1 Light Eye Trackers [@Ferhat2012].

One of the more prominent examples is [PyGaze](http://pygaze.org), a software
primarily used to perform eye tracking and gaze tracking analysis
[@Dalmaijer2014]. It is written and Python and maintained by Edwin Dalmaijer
and Sebastiaan Mathôt. Since 2015 it features a webcam-based pupil tracker
named webcam-eyetracker [@Dalmaijer2015]. It tracks the pupil of one eye and
uses infrared light. Because of that, it is not suitable for all webcams,
as most have a built-in infrared filter -- though for some webcams it is
possible to remove it. It also needs to have specific lighting conditions;
Dalmaijer reports he had to turn off all regular lights when using it.

The package [gazr](https://github.com/severin-lemaignan/gazr) by Séverin
Lemaignan integrates with the [+ROS](https://ros.org). Gazr is designed for
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
interaction tasks. It claims one of its features is to be able to do gaze
tracking, but the current version does not yet offer this functionality.
However, it does perform head pose estimation [@Patacchiola2017]. Since its
publication about the head pose estimation is from 2017, it is possible that
gaze estimation will be added in the future.\nowidow[3]
