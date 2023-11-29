# ⛔️🚗🚦 Russian Traffic Signs Detection With YOLO

> Detection of traffic signs with YOLO on the [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset) dataset.

A prototype of an assistant for drivers that will notify them of road signs. The assistant can recognize road signs in various lighting and weather conditions, informing the driver about speed limits, prohibitions, warnings and other important instructions on the road in accordance with Russian traffic rules. Currently it works with dash cam videos.

Please visit the branch (⚙️ service ⚙️)[https://github.com/Aillustrate/traffic-sign-detection/tree/service] to get acquainted with all the technical details such as instructions for deployment, scaling, and performance evaluations

**Example of the resulting video**

![gif](example_video.gif)

## Experiments

### Dataset

For training and evaluation of the models in our experimets we chose the [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset) dataset. RTSD dataset contains frames provided by [Geocenter Consulting company](http://geocenter-consulting.ru). Frames are obtained from widescreen digital video recorder which captures 5 frames per second. Frames are captured in different seasons (spring, autumn, winter), time of day (morning, afternoon, evening) and in different weather conditions (rain, snow, bright sun). Total dataset contains 156 types of signs from Russian traffic rules.

### Models

We conducted experiments with 2 models: [yolo8m](https://github.com/ultralytics/ultralytics) и [yolo5m](https://github.com/ultralytics/yolov5). We decided to try these models because different versions of YOLO have been a universal solution for object detection and classification for several years, and YOLO 8 was SOTA model until recently. In addition, YOLO is a scalable solution because it is easy to use and can learn to detect and classify any classes of objects. In our specific case, the classes were the numbers of signs in the Russian Traffic Rules and then the postprocessing with the mappings to their names was done.

### Metrics
To evaluate the performance of the models we decided to use 2 metrics: MAP@50 and MAP@50-95.

- Mean Average Precision(mAP) is the current benchmark metric used by the computer vision research community to evaluate the robustness of object detection models.
- mAP encapsulates the tradeoff between precision and recall and maximizes the effect of both metrics.
- Calculating mAP over an IoU threshold range avoids the ambiguity of picking the optimal IoU threshold for evaluating the model's accuracy.

### Results

We trained both models for about 70 epochs. All metrics of last epohs of traing for both models are avaliable in [metrics](metrics) directory. Overall, it can be said that with about the same training time yolo8m gives metrics slightly higher than yolo5m. Code for training and evaluation of the models is avaliable in notebook [experiments.ipynb](experiments.ipynb).


| Model  | MAP@50 | MAP@50-95 |
| ------ | ------ | --------- |
| yolo8m |  0.95  |   0.74    |
| yolo5m |  0.91  |   0.69    |
