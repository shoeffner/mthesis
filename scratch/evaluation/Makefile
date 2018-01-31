TARGET_DIR ?= $(abspath ../../assets/gen_files)

PUPIL_ACCURACIES = table-comptimes-pexels.md table-comptimes-BioID.md \
				   table-relative-errors-pexels.md table-relative-errors-BioID.md \
				   pexels_accuracy_vs_error.csv BioID_accuracy_vs_error.csv

PIPELINE_TIMES = table-pipeline-step-times.md table-pipeline-times.md

PREDICTIONS = predictions_iTracker.png

UNDETECTED = undetected_faces.png

FILES = $(PUPIL_ACCURACIES) $(PIPELINE_TIMES) $(PREDICTIONS) $(UNDETECTED)

all: $(foreach f,$(FILES),$(TARGET_DIR)/$(f))

$(foreach f,$(PUPIL_ACCURACIES),$(TARGET_DIR)%$(f)): pupil_accuracies.py BioID.csv pexels.csv Makefile | $(TARGET_DIR)/comptimes
	python ./pupil_accuracies.py

$(foreach f,$(PIPELINE_TIMES),$(TARGET_DIR)%$(f)): pipeline_times.py pexels.csv Makefile
	python ./pipeline_times.py

$(foreach f,$(PREDICTIONS),$(TARGET_DIR)%$(f)): prediction_iTracker_BioID.png prediction_iTracker_Pexels.png
	montage $^ -tile 2x -mode Concatenate -geometry "+5+5" $@

$(foreach f,$(UNDETECTED),$(TARGET_DIR)%$(f)): undetected_faces.py pexels.csv Makefile
	montage $(shell python undetected_faces.py) -tile 5x -mode Concatenate -geometry "120x120+2+2" $@


prediction_iTracker_Pexels.png prediction_iTracker_BioID.png: predictions_images.py pexels.csv bioid.csv Makefile
	python ./predictions_images.py

BioID.csv: dataacquisition/build/bioid | ../BioIDImages/bio
	cd dataacquisition/build && ./bioid > ../../BioID.csv || true

pexels.csv: dataacquisition/build/pexels | ../pexels_face_images/resized
	cd dataacquisition/build && ./pexels > ../../pexels.csv || true

MODEL_FILES=itracker_deploy.prototxt snapshots/itracker25x_iter_92000.caffemodel \
			mean_images/mean_face_224.binaryproto mean_images/mean_left_224_new.binaryproto mean_images/mean_right_224.binaryproto

dataacquisition/build/bioid: dataacquisition/bioid.cpp dataacquisition/build/shape_predictor_68_face_landmarks.dat $(foreach m,$(MODEL_FILES),dataacquisition/build/models/$(m)) dataacquisition/CMakeLists.txt | dataacquisition/build
	cd dataacquisition/build && make bioid

dataacquisition/build/pexels: dataacquisition/pexels.cpp dataacquisition/build/shape_predictor_68_face_landmarks.dat $(foreach m,$(MODEL_FILES),dataacquisition/build/models/$(m)) dataacquisition/CMakeLists.txt | dataacquisition/build
	cd dataacquisition/build && make pexels

dataacquisition/build/shape_predictor_68_face_landmarks.dat: | dataacquisition/build
	curl -L -o $@.bz2 https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
	cd dataacquisition/build && bunzip2 -ck shape_predictor_68_face_landmarks.dat.bz2 > shape_predictor_68_face_landmarks.dat

dataacquisition/build/models/%: | dataacquisition/build/models
	curl -L -o $@ https://github.com/CSAILVision/GazeCapture/raw/master/models/$*

dataacquisition/build/models:
	@mkdir -p dataacquisition/build/models/mean_images
	@mkdir -p dataacquisition/build/models/snapshots

dataacquisition/build:
	@mkdir -p dataacquisition/build
	@cd dataacquisition/build && cmake ..

../BioIDImages/bio:
	@$(MAKE) -C ../BioIDImages

$(TARGET_DIR)/comptimes:
	@mkdir -p $(TARGET_DIR)/comptimes
