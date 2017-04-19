% Master's thesis: Gaze tracking using common webcams
% Sebastian Höffner
% April 26th, 2017

---
theme: metropolis
colortheme: metropolis
themeoptions:
    - progressbar=foot
...


# Eye tracking today

- Eye tracking allows to study gaze behaviour
- Often measures saccades and fixations and distinguishes them
- Important in many (behavioral) experiments, to investigate e.g.
    * perspective taking / theory of mind
    * attention shift
    * search strategies
    * ...


# Eye tracking solutions

- Tobii
- EyeTribe
- SMI
- SR


# Eye tracking solution problems

Most solutions are

- expensive (hardware or software, or even both)
- tightly coupled to specific operating systems or ecosystems
- difficult to set up
- are inaccurate if dealing with head movements


# Eye tracking vs gaze tracking

---------------------------------------------------------------------
Eye tracking                       Gaze tracking
---------------------------------- ----------------------------------
follows the eyes                   addtionally calculates the
                                   reference point on the stimulus

usually relatively easy            only easy using certain
                                   assumptions: fixed viewport,
                                   distance, no head movements, ...

can be done with very cheap        only available with expensive
hardware                           hard- and software (EUR 150+)

enough to track the iris           usually relies on corneal reflections
                                   or infrared
---------------------------------------------------------------------


# Hardware and software requirements

- Camera needs high FPS for saccades
- Fast processing time (should not have impact on experiments)
- Accurate -- precise pupil position to pixel mapping
- Often stereo vision (binocular)
    * better depth perception
    * individual tracking of both eyes


# Webcams as a cheap alternative

- Often built-in in modern laptops -- if not, very cheap to buy
- Relatively low FPS (~30)
- No infrared (IR filter sometimes removable)
- No stereo vision (monocular)
- Often contain additional features: auto focus, brightness corrections, ...


# Possible applications

- Simple experiments which focus on fixations
- Easy to use and setup: potential to even use it at home
    * For experiments
    * As input device
    * Marketing research


# Related work

- PyGaze [@dalmaijer2014]
- eyeLink [@timm2011, Demo]

But: Both projects seem to stall


# My contribution

- Extension of @timm2011 to allow for gaze tracking

- Evaluate different gaze tracking methods and compare
    * accuracy (measure yet to be defined)
    * reliability
    * classification (saccades, fixations)
    * meta data: price, availability, adaptability


# Challenges

- Accuracy and performance: e.g. ~1 % error for fixations compared to commercial solutions
- Extending eyeLink: It's not designed to be extended
- API design
- Head movements
- Defining evaluation criteria
- I have never really worked with eye tracking before


# Remark about open science

- Everything will be made available on GitHub
- If the project is successful it will be possible to extend it
    - Different language bindings, drivers, etc.
- Publishing as open source allows others to contribute
- Publishing as open source encourages high quality


# SMART Summary

Specific:
  ~ Implement gaze tracking software for webcam video streams

Measurable:
  ~ Compare performance with existing solutions (e.g. accuracy)

Achievable:
  ~ Eye tracking exists, needs to be extended to gaze tracking

Relevant:
  ~ Cheap and open solution for eye tracking reduces paywalls and increases cooperation

Time-bound:
  ~ End of September (Ahhh that's so soon already!)


# References
