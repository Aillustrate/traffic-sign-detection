# ⛔️🚗🚦 Russian Traffic Signs Detection With YOLO

> Detection of traffic signs with YOLO on the [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset) dataset.

A prototype of an assistant for drivers that will notify them of road signs. The assistant can recognize road signs in various lighting and weather conditions, informing the driver about speed limits, prohibitions, warnings and other important instructions on the road in accordance with Russian traffic rules. Currently it works with dash cam videos.

**Example of working with video**

![gif](example_video.gif)

## Experiments

### Dataset

For training and evaluation of the models in our experimets we chose the [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset) dataset. RTSD dataset contains frames provided by [Geocenter Consulting company](http://geocenter-consulting.ru). Frames are obtained from widescreen digital video recorder which captures 5 frames per second. Frames are captured in different seasons (spring, autumn, winter), time of day (morning, afternoon, evening) and in different weather conditions (rain, snow, bright sun). Total dataset contains 156 types of signs from Russian traffic rules.

### Models

We conducted experiments with 2 models: [yolo8m](https://github.com/ultralytics/ultralytics) и [yolo5m](https://github.com/ultralytics/yolov5). We decided to try these models because different versions of YOLO have been a universal solution for object detection and classification for several years, and YOLO 8 was SOTA model until recently. In addition, YOLO is a scalable solution because it is easy to use and can learn to detect and classify any classes of objects. In our specific case, the classes were the numbers of signs in the Russian Traffic Rules and then the postprocessing with the mappings to their names was done.

### Metrics
To evaluate the performance of the models we decided to use 2 metrics: MAP@50 and MAP@50-95.
