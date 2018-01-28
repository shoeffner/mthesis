# Introduction

## A brief history of eye tracking research

In the late 19th century, Helmholtz published his "Handbuch der physiologischen
Optik" [@Helmholtz1866], which is an exhaustive summary and critical review of
about 150 years of research about the eye, especially its inner workings and
functions, and, more importantly, about visual sensation and perception. While
a great part of the handbook focuses on eyeball movements and lens
accommodation, attention is frequently brought up.

\widefn

> Erst indem wir unsere Sinnesorgane nach eigenem Willen in verschiedene
> Beziehungen zu den Objecten bringen, lernen wir sicher urtheilen über die
> Ursachen unserer Sinnesempfindungen\[.\][^translationhelmholtz]
>
> \raggedleft --- <cite>@Helmholtz1866. Handbuch der physiologischen Optik,
> p. 452.</cite>


[^translationhelmholtz]: Translated quotation [@Helmholtz1866]: We learn to
  reason about our sensory impressions only because we can establish different
  relations between our sensory organs and objects at our own discretion.

\stopwidefn

With these words Helmholtz makes a very important observation: Humans are
only able to reason about what they perceive with their eyes because they
can willfully direct them towards objects. In other words,
humans can only reason about their visual perception because they can control
their visual attention.

Helmholtz distinguishes between "facial sensations" (German:
"Gesichtsempfindungen") and "facial perception" (German:
"Gesichtswahrnehmungen"). Facial sensations are sensations of the retina and
the optic nerve, while facial perception denotes the semantics humans attribute
to the combination of those sensations. To form semantics of an object, to
perceive it, humans have to move their eyes to the right position to get the
needed sensory information. Thus they need to attend an object with their eyes.
Turning this conclusion and thinking ahead, we can make the assumption that
what humans attend, that is what they look at, is what they are interested in, because
they have to actively direct their eyes towards that object.

But where are humans looking at? @Huey1908 tried to answer this question for
reading tasks. He built a device as depicted in @fig:huey_eyetracker which is attached to
the locally sedated cornea using a little cup made of plaster cast. The other
side of the device points at smoked paper, onto which it draws the movements of
the attached eye. Using the device, Huey was able to to report accurate
measurements of fixations and saccades, stops and rapid movements of the
eyes, which he used to analyze reading behavior.

![Schema of Huey's eye tracking device. It work similar to a seismograph.
Image from Google's scan of the New York Public Library's 1968 reprint of
@Huey1908, p. 26.](huey_eyetracker.png){#fig:huey_eyetracker}

Following Huey's example, a surge of new eye tracking devices hit the research
world. @Yarbus1967 became famous for his research on how a given task
influences eye movements in comparison to a free exploration. The device he
used is similar to Huey's, but it is attached to the eyes without plaster cast,
but with small rubber cups. These early methods by Huey and Yarbus are quite
intrusive and others searched for non-intrusive methods.

Today, many different eye and gaze tracking tools exist. @Chennamma2013
categorize them in four kinds: +Eog, scleral search coils, infrared
oculography, and video oculography. +Eog determines the rotation of eyes by
measuring the electrical fields around them. It is used in +eeg research to
remove blink artifacts, although other techniques using more sophisticated eye
tracking have been proposed for artifact rejection [@Noureddin2012]. Another
exemplary use case for +eog and +eeg is sleep research, where they can be used
to determine sleep stages, or as an indicator for lucid dreams [@Appel2017].
Scleral search coils are search coils attached to or embedded into special
contact lenses. By moving the search coils inside a magnetic field, their exact
poses can be measured with great accuracy and resolutions [@Shelhamer2010].
In infrared oculography an eye is illuminated by infrared light and the
intensity of the reflected light is measured. It is very coarse but can be used
during +mri [@Chennamma2013]. The most important kind is video oculography,
where eyes and gaze are tracked by analysing video streams. It comes in many
varieties: employing one or many cameras, using visible or infrared light,
constraining the subjects using chin rests or similar tools, with cameras
attached to special glasses, computer screens or standing in front or around
the participants, and much more. As many types of video oculography there are,
as many different use cases do they have. Eye and gaze tracking is used in
research on attention and perception in neuroscience as well as psychology
[@Duc2008; @Duchowski2002], in marketing [@Wedel2008], process planning and
optimization [@Duchowski2002], but also in usability research and human
computer interaction [@Duchowski2007]. Eye and gaze tracking research have long
been limited to laboratory settings, but with better and smaller hardware
experiments are more often performed in real world scenarios, for example in
front of any computer [@Papoutsaki2016], on mobile phones and tables in various
locations [@Krafka2016] or with head mounted tracking devices in retail shops
[@Vilks2017]. With the advent of +AR and +VR new applications arise even more
applications, for example foveated rendering can be used to improve rendering
performance in ++VR [@Patney2016].

Strictly speaking it is important to distinguish between eye tracking and gaze tracking.
In this thesis eye tracking refers to the process of detecting the
positions of the eyes or eye centers -- the pupil centers. Gaze tracking on the
other hand refers to process of estimating the gaze point on a computer
screen. Often the two terms are used interchangeably, though mostly only the
term eye tracking is used while gaze tracking is not used at all. Especially
the commercial hardware and software solutions presented in
@sec:commercial-gaze-tracking-solutions are often marketed as eye tracking
devices, while in fact they also perform gaze tracking. This thesis will try to
use the two terms distinctively, but since they are closely interwoven it might not
always be possible.


## About this thesis

The goal of this thesis is to implement the gaze tracking library \Gaze{} which employs
a calibration free geometric feature-based model and is easy to use, modify, and extend. The
library focuses only on tracking of screen directed gaze, that is it only
tracks subjects gazing at a computer screen and estimates where on the screen
the subject gazes at. It also should only require a common webcam to keep its
deployment costs at a minimum. One important aspect is that the library
should be +FOSS, so that everyone interested in the project can reuse and
modify parts of it for any purpose.

In the first part, different eye and gaze tracking
solutions will be evaluated and an overview over the current state of the art
in eye and gaze tracking hardware and software established. Then the methods
and models will be presented, starting with geometric model of gaze, the
direction of view, and the architecture of \Gaze{}, the library implementing
the model.  The eye tracking model is chosen because of its success in eyeLike
[@Hume2012], an implementation of @Timm2011. As an alternative to the
geometric model, a pre-trained neural network by @Krafka2016 will be
introduced and employed. After the introduction of the methods and models, the \Gaze{} library
will be described in more detail to explain how the geometric model is
implemented and how the library can be used or extended. One example for such
an extension is the incorporation of the pre-trained model of @Krafka2016.
Following the library description, the results of the different methods and
models will be discussed and the two approaches, geometric model and +cnn, will
be compared. It will be shown that the eye tracking approach works as good as
in its original paper, even though the rest of the geometric model
is not as good as was hoped for. Finally a brief lookout will be given to
discuss future steps beyond this thesis.

Thus the scope of this thesis has four main points: First reimplementing a
model for eye tracking, second use a simplified model to perform gaze tracking
on a screen surface, third compare the model with a pre-trained +cnn, and
fourth realize all these points in a free, open, and reusable software library
which only needs a webcam video.


### Note about online references and other sources


#### Online references

Since this thesis focuses around the development of a computer software
library, many resources are not available as classical journal or conference
papers, or books. Instead, blogs and websites, documentation pages and other
formats used as references are published exclusively on the internet. While
such sources are cited with a +URL and, if they are listed in the [References], a retrieval
date, it is possible that over time contents change. If some content is no
longer available online or changed by the time you read this thesis, please try
to access the content through the Internet Archive's [Wayback
Machine](https://archive.org/web), which hopefully is still around. Often links to software products
will be provided directly as part of the text. To avoid ++URL in the
middle of sentences, they will be placed inside footnotes.


#### Photographs from Pexels

During the development of \Gaze{}, several photographs of faces differing in
backgrounds, poses, lightings, and other conditions, are used. Unless otherwise
noted, all photographs in this thesis are either taken by the author or
downloaded from the website [Pexels](https://pexels.com). Pexels releases all images into the public domain, using the +CC0 license. This allows
the usage of the photographs without the need of any attribution [@CC0License].


#### File names and source code availability

In many situations there will be source code or similar code listings. Some are
annotated with a file path, denoting in which files they can be found. These
file paths are usually relative to the library source code's root directory or
the thesis source code's `assets/examples` directory. It should become clear
from the context, whichever is correct. In case you did not receive this thesis
in a print format with an attached +SDcard, you can find the source code for the
\Gaze{} library and the thesis online, as well as other supplementary materials.
A list of ++URL can be found in \Cref{tab:links}.

Table: Links to the thesis' source files. \label{tab:links}

Description             Link
---------------------- ------------------------------------------
\Gaze{} Source Code    https://github.com/shoeffner/gaze
\Gaze{} Documentation  https://shoeffner.github.io/gaze
Thesis PDF & Materials https://shoeffner.github.io/mthesis
Thesis Source Code     https://github.com/shoeffner/mthesis
Continuous Integration https://semaphoreci.com/hoeffner/gaze

TODO(shoeffner): put pdf and materials up on mthesis page, add note about git tags described in this thesis


#### Exchange rates between USD and EUR

In section @sec:commercial-gaze-tracking-solutions all prices of hardware and
software are given in EUR. Some prices were only available in USD on the
manufacturers websites, so to keep the currency comparable, all USD prices were
converted and rounded to EUR. The exchange rate used was $\SI{1}[{USD\,}]{} =
\usd{1}$, as reported by [XE.com Inc.](https://xe.com) on January 28, 2018 at
19:48 UTC.
