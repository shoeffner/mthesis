#include <string>
#include <iostream>
#include <memory>
#include <vector>

#include "caffe/caffe.hpp"

#include "opencv2/opencv.hpp"


cv::Mat load_mean(const std::string& mean_file) {
  caffe::BlobProto blob_proto;
  caffe::ReadProtoFromBinaryFileOrDie(mean_file.c_str(), &blob_proto);

  /* Convert from BlobProto to Blob<float> */
  caffe::Blob<float> mean_blob;
  mean_blob.FromProto(blob_proto);

  std::vector<cv::Mat> channels;
  float* data = mean_blob.mutable_cpu_data();
  for (int i = 0; i < 3; ++i) {
    cv::Mat channel(mean_blob.height(), mean_blob.width(), CV_32FC1, data);
    channels.push_back(channel);
    data += mean_blob.height() * mean_blob.width();
  }

  cv::Mat mean;
  cv::merge(channels, mean);

  cv::Scalar channel_mean = cv::mean(mean);
  return cv::Mat(224, 224, mean.type(), channel_mean);
}

int main(int argc, char** argv) {
  std::string model_file("../GazeCapture/models/itracker_deploy.prototxt");
  std::string trained_file("../GazeCapture/models/snapshots/itracker25x_iter_92000.caffemodel");
  // init network
  std::unique_ptr<caffe::Net<float>> net(new caffe::Net<float>(model_file, caffe::TEST));
  net->CopyTrainedLayersFrom(trained_file);

  cv::Mat left = cv::imread("../images/eye_left.png", cv::IMREAD_COLOR);
  cv::Mat right = cv::imread("../images/eye_right.png", cv::IMREAD_COLOR);
  cv::Mat face = cv::imread("../images/face.png", cv::IMREAD_COLOR);
  cv::Mat mask = cv::imread("../images/map.png", cv::IMREAD_GRAYSCALE) / 255;

  cv::Mat mean_left = load_mean("../GazeCapture/models/mean_images/mean_left_224_new.binaryproto");
  cv::Mat mean_right = get_mean("../GazeCapture/models/mean_images/mean_right_224.binaryproto");
  cv::Mat mean_face = get_mean("../GazeCapture/models/mean_images/mean_face_224.binaryproto");

  std::cout << model_file << ", " << trained_file << std::endl;

  std::vector<cv::Mat> input_images = {left, right, face, mask};
  std::vector<cv::Mat> means = {mean_left, mean_right, mean_face, mask};

  std::cout << "images" << std::endl;
  for (auto i : input_images) {
    double min, max;
cv::minMaxLoc(i, &min, &max);
    std::cout << "Mean: " << cv::mean(i) << " ; min: " << min << " ; max: " << max << std::endl;
  }
  std::cout << "Means" << std::endl;
  for (auto m : means) {
    std::cout << m.at<float>(0, 0, 0) << std::endl;
  }


  for (int i = 0; i < 4; ++i) {
    // Reshape input to batch size 1
    auto input = net->input_blobs()[i];
    std::vector<int> shape = input->shape();
    shape[0] = 1;
    input->Reshape(shape);
  }
  // Propagate batch size
  net->Reshape();

  std::cout << "Inputs" << std::endl;
  for (int i = 0; i < 4; ++i) {
    auto input = net->input_blobs()[i];
    std::vector<int> shape = input->shape();
    std::cout << input->shape_string() << std::endl;

    // Create mat object per channel with pointer to layer data
    std::vector<cv::Mat> channels;
    float* input_data = input->mutable_cpu_data();
    for (int j = 0; j < shape[1]; ++j) {
      cv::Mat channel(shape[2], shape[3], CV_32FC1, input_data);
      channels.push_back(channel);
      input_data += shape[2] * shape[3];
    }

    // Resize image to channel shape (or reshape for the map)
    cv::Mat input_image;
    if (i != 3) {
      cv::Mat resized(shape[2], shape[3], CV_32FC3);
      input_images[i].convertTo(input_image, CV_32FC3);
      cv::resize(input_image, resized, resized.size());
      cv::subtract(resized, means[i], resized);
      cv::split(resized, channels);
    double min, max;
cv::minMaxLoc(resized, &min, &max);
    std::cout << "Mean: " << cv::mean(i) << " ; min: " << min << " ; max: " << max << std::endl;
    } else {
      input_images[i].convertTo(input_image, CV_32FC1);
      for (int j = 0; j < shape[1]; ++j) {
        channels[j] = input_image.at<float>(j);
      }
    }
  }

  // DEBUG
  for (auto blob : net->input_blobs()) {
    int num_of_debug_elems = 100; // blob->shape(0) * blob->shape(1) * blob->shape(2) * blob->shape(3);
    std::cout << "inspecting first " << num_of_debug_elems << " elems" << std::endl;
    float* d = blob->mutable_cpu_data();
    for (int i = 0; i < num_of_debug_elems; ++i) {
      std::cout << *d++ << " ";
    }
    std::cout << std::endl;
  }

  // inference step
  net->Forward();

  // Just copied: read out result
  caffe::Blob<float>* output_layer = net->output_blobs()[0];
  const float* begin = output_layer->cpu_data();
  const float* end = begin + output_layer->channels();
  std::vector<float> out = std::vector<float>(begin, end);
  for (auto o : out) {
    std::cout << "Result " << o << " " << std::endl;
  }

}
