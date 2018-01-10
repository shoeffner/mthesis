# Introduction

## A brief history of eye tracking research

In the late 19th century, Helmholtz published his "Handbook of physiological
optics" (German: "Handbuch der physiologischen Optik", @Helmholtz1866), which is an
exhaustive summary and critical review of about 150 years of research about the
eye, especially its inner workings and functions, and, more importantly, about
visual sensation and perception. While a great part of the handbook focuses
on eyeball movements and lens accomodation, attention is frequently brought
up.

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
can willfully direct them towards objects[^othersensors]. In other words,
humans can only reason about their visual perception because they can control
their visual attention.

[^othersensors]: Of course his statement is not limited to eyes, but for
  simplicity only the visual system is taken into account here.

Helmholtz distinguishes between "facial sensations" (German:
"Gesichtsempfindungen") and "facial perception" (German:
"Gesichtswahrnehmungen"). Facial sensations are sensations of the retina and
the optic nerve, while facial perception denotes the semantics humans attribute
to the combination of those sensations. To form semantics of an object, to
perceive it, humans have to move their eyes to the right position to get the
needed sensory information. Thus they need to attend an object with their eyes.
Turning this conclusion and thinking ahead, we can make the assumption that
what humans attend (what they look at) is what they are interested in, because
they have to actively direct their eyes towards that object.

But where are humans looking at? @Huey1908 tried to answer this question for
reading tasks. He built a device (see @fig:huey_eyetracker) which is attached to
the locally sedated cornea using a little cup made of plaster cast. The other
side of the device points at smoked paper, onto which it draws the movements of
the attached eye. Using the device, Huey was able to to report accurate
measurements of fixations and saccades (stops and rapid movements of the
eyes, respectively), which he used to analyze reading behavior.

![Schema of Huey's eye tracking device. It work similar to a seismograph.
Image from Google's scan of the New York Public Library's 1968 reprint of
@Huey1908, p. 26.](huey_eyetracker.png){#fig:huey_eyetracker}

Following Huey's example, a surge of new eye tracking devices hit the research
world. @Yarbus1967 became famous for his research on how a given task
influences eye movements in comparison to a free exploration. The device he
used was similar to Huey's, but it is attached without plaster cast, but with
small rubber caps.

TODO(shoeffner): Add Yarbus paper, confirm it were indeed rubber caps

These early methods by Huey and Yarbus are quite intrusive and others searched for non-intrusive methods.

TODO(shoeffner): Something about Buswell, Rayner?

Today, many different eye tracking tools exist. They can be categorized as

- eye-attached, optical, electric potential measurement (EOG/EEG, ...)

While the above mentioned early techniques fall into the eye-attached tracking
category, today optical tracking would be the method of choice for those
studies.

- overview over optical tracking devices
- distinction between eye and gaze tracking

## About this thesis

- Comparison gaze tracking approaches using webcams
- eyeLike (top web search hit) only tracks eyes, not gaze
- Cheap alternative to other softwares
- Providing a best-practices FOSS solution

### Note about online references


