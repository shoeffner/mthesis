# Eye center localization

To accurately estimate gaze points it is important to first estimate the pupils' locations in relation to the respective eye corners. @Timm2011 use a gradient based method to detect eye centers. An example implementation by Tristan Hume can be found online[^thume:eyeLike]. In his blog post[^thume:2012-11-04], Hume explains some adjustments he learned about during correspondence with Timm. These adjustments are also implemented in \gaze.


[^thume:eyeLike]: [eyeLike](https://github.com/trishume/eyeLike)
[^thume:2012-11-04]: [Simple, accurate eye center tracking in OpenCV](http://thume.ca/projects/2012/11/04/simple-accurate-eye-center-tracking-in-opencv/)
