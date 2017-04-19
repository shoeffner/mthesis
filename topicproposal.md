% Master's thesis proposal: Gaze tracking using common webcams
% Sebastian Höffner
% February 13th, 2017

---
nocite: "@*"
...

# Goal

In my thesis I will write a software which allows to track gaze points on a
screen by only using a webcam. To measure the quality and accuracy I will
compare different setups of software or hardware. The features which I will
compare are accuracy (metric to be decided, e.g. pixels or angular error), and
performance (should be real time or close to real time). My system should have an
average error of less than or equal to 1 %, while the performance should not
show any significant lag, i.e. it should keep up a frame rate of about 30 FPS.

# Motivation

Eye tracking is a very important technology to study gaze behaviour. Many
solutions exist, but most of them rely on expensive hardware or sell as
expensive software, which is then again often tightly coupled to specific
hardware or operating systems. By writing a software which uses common webcams
to do accurate eye tracking many of these problems can be overcome. Even if the
results will not turn out to be perfect it will still be viable for people who
are starting out on eye tracking and first want to get a quick start before
buying expensive setups.

There are some approaches for tracking eyes already freely available, most
importantly PyGaze's webcam eye tracker and the OpenCV based eyeLike, both of
which only track eyes but not gaze behavior. However, in online discussions
people search for solutions to tracking gaze with their webcams using these
tools, so there is definitely a need for such software.

A third motivation to write a software is that there is no free open source
software to perform gaze tracking without a specific hardware setup available.
This is an opportunity to contribute such software to the open source and
research community.

# Challenges

The main challenge is of course the accurate and performant gaze tracking. To
overcome this challenge multiple smaller challenges have to be tackled. Eye
tracking, that means the tracking of the pupil in a camera image, is already
very accurately solved by the free software eyeLink. However, it needs to be
incorporated in the software in a way that the data is usable for further
calculations. The next step is then to determine the gaze direction and from
that calculate the position on the screen. This should first be done for
relatively stable frontal face images, however if that succeeds a next step is
to also take head movements into account.

Eventually the approach should be compared to existing professional solutions.
For this two possibilities seem plausible: either using a video, trying to
reliably test it by repeated similar movements and gazes, or conducting a little
study which measures eye movements from multiple participants to come up with an
estimate and a "real lab" situation. In both cases, a seemingly random path should
be followed and the accuracy of the webcam eye tracker should be compared to
others. In the best case it is somehow possible to measure a reference system
and the webcam tracker simultaneously for a good comparison.

As a reference system the Tobii Eye X was proposed, however other options might
arise as well.

# Related work and starting points

There is plenty of work available about eye tracking. @timm2011 provide a
basis for eye tracking by using a gradient algorithm, which I want to use for
the base eye tracking. To estimate the parameters for gaze calculations I plan
to look into papers like @filho2010 and @veronese2012, which employ a simple
artificial neural network to estimate the depth of binocular images. However,
there might be easier and more suitable approaches for eye tracking.

The very recent paper by @jung2016, which use ultrasonic sensors to compensate
for head movements, might provide inspiration to compensate head movements in
general.

# References
