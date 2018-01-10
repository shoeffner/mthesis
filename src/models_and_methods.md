# Methods and models

Estimating gaze is done in Gaze using a pipelined architecture. Many pipeline
steps consist of models which solves part of the gaze estimation problem,
others serve for input and output[^iopipeline] of the data.
This chapter summaries their functions and details the model for each
computation step.

## Input: source capture

The first pipeline step uses
[`cv::VideoCapture`](https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html)
to capture the input specified inside the `gaze.yaml`.


[^iopipeline]: As of writing, no special output writers are implemented, but
  the infrastructure exists.


- Gaze: Pipeline
- Each step performs a task for the big picture and is thus exchangeable

- steps:
  - source capture
  - face/eye detection
  - head pose estimation
  - pupil detection
  - gaze estimation
