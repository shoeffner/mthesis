# Unit test face images

The files inside this directory are to download and prepare unit test images.
The final images are included inside the [gaze repository](https://github.com/shoeffner/gaze).

To download and resize the images, perform these steps:

```bash
mkdir photos
python downloader.py
mkdir resized
python resize.py
```

To annotate the images and create the test set properly run:

```bash
mkdir annotations
python annotate.py
```

Navigate using the arrow left and right keys. Click on the pupils to mark them
(the markers alternate). Click somewhere outside the image to delete the markers.
Press space to save and advance to the next image.

When you are done, copy the contents from `annotations` and `resized` to the
unit test assets directory.

```bash
mkdir -p ${GAZE_ROOT_DIR}/tests/assets/pexels_faces
cp annotations/* ${GAZE_ROOT_DIR}/tests/assets/pexels_faces
cp resized/* ${GAZE_ROOT_DIR}/tests/assets/pexels_faces
```


## License

All images are downloaded from [pexels](https://www.pexels.com) and are
released under a CC0 license.
