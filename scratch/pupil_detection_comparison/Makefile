IMLIST=$(shell ls eye*b.png | sed 's/eyeLike//' | sed 's/b.png//')

all: faces comparison

.INTERMEDIATE: $(foreach i,$(IMLIST),mon$(i).png)
mon%.png: eyeLike%r.png eyeLike%l.png pupil%r.png pupil%l.png
	@montage $^ -geometry 50x50+3+3 $@

faces: ../../assets/images/pupil_detection_faces.png
../../assets/images/pupil_detection_faces.png: $(foreach i,$(IMLIST),../pexels_face_images/photos/$(i).jpeg)
	montage $(foreach i,$(IMLIST),-label $(i) ../pexels_face_images/photos/$(i).jpeg) \
		-tile x6 -geometry "120x120>+6+6" $@

comparison: ../../assets/images/pupil_detection_comparison.png
../../assets/images/pupil_detection_comparison.png: $(patsubst %,mon%.png,$(IMLIST))
	montage $(foreach i,$(IMLIST),-label $(i) mon$(i).png) \
		-tile x6 -geometry +2+2 $@
