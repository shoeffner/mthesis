#ifndef INCLUDE_GAZE_PIPELINE_STEPS_NEW_STEP_H_
#define INCLUDE_GAZE_PIPELINE_STEPS_NEW_STEP_H_

#include "gaze/gui/visualizeable.h"
#include "gaze/pipeline_step.h"
#include "gaze/util/data.h"


namespace gaze {

namespace pipeline {

class NewStep final
    : public PipelineStep,
      public gui::LabelVisualizeable {

 public:
  NewStep();

  void process(util::Data& data) override;

  void visualize(util::Data& data) override;
};

}  // namespace pipeline

}  // namespace gaze

#endif  // INCLUDE_GAZE_PIPELINE_STEPS_NEW_STEP_H_
