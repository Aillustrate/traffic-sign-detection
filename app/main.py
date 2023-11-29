import os

import gradio as gr
import pandas as pd
from inference import Detector
from label2name import Mapper
from project_utils import get_model

MODEL_NAME = "yolov8m"
model = get_model(version="", model_name=MODEL_NAME)

signs = pd.read_csv("components/traffic_signs.csv")
mapper = Mapper(
    signs, labels_path="components/labels.txt", saving_path="components/mapping.json"
)
mapper.create()

detector = Detector(model=model, mapper=mapper)


def video_identity(video, progress=gr.Progress()):
    dir_name, file_name = os.path.split(video)
    new_file_name = "processed_" + file_name
    new_file_path = os.path.join(dir_name, new_file_name)
    detector.process_video(
        video_path=video, saving_path=new_file_path, conf=0.6, progress=progress
    )
    return new_file_path


demo = gr.Interface(
    video_identity,
    gr.Video(),
    "playable_video",
    examples=[os.path.join(os.path.dirname(__file__), "examples/test_video.mp4")],
    cache_examples=True,
)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0")
