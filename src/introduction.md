# Introduction

## A brief history of eye tracking research

In the late 19th century, Helmholtz published his "Handbuch der physiologischen
Optik" [@Helmholtz1866], which is an exhaustive summary and critical review of
about 150 years of research about the eye, especially its inner workings and
functions, and, more importantly, about visual sensation and perception. While
a great part of the handbook focuses on eyeball movements and lens
accommodation, attention is frequently brought up.

> Erst indem wir unsere Sinnesorgane nach eigenem Willen in verschiedene
> Beziehungen zu den Objecten bringen, lernen wir sicher urtheilen über die
> Ursachen unserer Sinnesempfindungen\[.\][^translationhelmholtz]
>
> \raggedleft --- <cite>@Helmholtz1866. Handbuch der physiologischen Optik,
> p. 452.</cite>

[^translationhelmholtz]: Translated quotation [@Helmholtz1866]: We learn to
  reason about our sensory impressions only because we can establish different
  relations between our sensory organs and objects at our own discretion.

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

Today, many different eye and gaze tracking tools exist. While the above mentioned
early techniques fall into the eye-attached tracking
category, today optical tracking would be the method of choice for those
studies.

- eye-attached, optical, electric potential measurement (EOG/EEG, ...)
- overview over optical tracking devices
- distinction between eye and gaze tracking


## About this thesis

The goal of this thesis is to implement a gaze tracking library which employs
a calibration free geometric model and is easy to use, modify and extend. The
library focuses only on tracking of screen directed gaze, that is it only
tracks subjects gazing at a computer screen and estimates where on the screen
the subject gazes at. In the first part, different eye and gaze tracking
solutions will be evaluated and an overview over the current state of the art
established. Then the methods and models will be presented, starting with
geometric model of gaze, the direction of view, and the architecture of Gaze,
the library implementing the model. As an alternative to the
geometric model, a pre-trained neural network by @Krafka2016 will be
introduced and employed. After the introduction of the methods and models, the Gaze library
will be described in more detail, to explain, how the geometric model is
implemented and how the library can be used or extended. One example for such
an extension is the incorporation of the pre-trained model of @Krafka2016.

TODO(shoeffner): Explain successes as well

The geometric model presented in this thesis is not sufficient to describe gaze,
as such it fails to estimate gaze points on a screen. Why this is the case and
potential ways to improve it will be discussed in the later sections of this
thesis. While it looks promising to use the model provided by @Krafka2016,
it also has some drawbacks which will also be lined out in the discussion.


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

During the development of Gaze, several photographs of faces differing in
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
in a print format with an attached +SDcard, you can find the thesis' source
material online at https://github.com/shoeffner/mthesis and the pdf version at
https://shoeffner.github.io/mthesis. The source code for the Gaze library is
available at https://github.com/shoeffner/gaze and its documentation can
be found at https://shoeffner.github.io/gaze/latest.

TODO(shoeffner): put pdf and materials up on mthesis page, add note about git tags described in this thesis
