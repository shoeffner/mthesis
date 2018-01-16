imlist=`ls eye*b.png | sed 's/eyeLike//' | sed 's/b.png//'`

# montage temp patches
for i in $imlist; do
    montage eyeLike${i}r.png eyeLike${i}l.png pupil${i}r.png pupil${i}l.png \
            -geometry 50x50+3+3 mon${i}.png
done

# combine patches
montage `for i in $imlist; do echo "-label ${i} mon${i}.png"; done` -tile x6 -geometry +2+2 ../../assets/images/pupil_detection_comparison.png
rm mon*.png

# combine original images
montage `for i in $imlist; do echo "-label ${i} ../pexels_face_images/photos/${i}.jpeg"; done` \
        -tile x6 -geometry "120x120>+6+6" ../../assets/images/pupil_detection_faces.png
