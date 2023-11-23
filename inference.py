import numpy as np
import cv2
from ultralytics import YOLO
from label2name import Mapper

def process_frame(frame, model:YOLO, mapper:Mapper) -> np.ndarray:
    """
    Detects traffic signs on an image
    param frame: frame from a video or path to the image
    param model: the YOLO model
    param mapper: initialized mapper object, which maps labels to names
    return: annotated image
    """
    results = model(frame, verbose=False)
    result = mapper.replace_names(results[0])
    annotated_frame = result.plot()
    return annotated_frame

def process_video(video_path:str, model:YOLO, mapper:Mapper, saving_path:str=None):
    """
    Detects traffic signs on a video
    param video_path: path to the video
    param model: the YOLO model
    param mapper: initialized mapper object, which maps labels to names
    param saving_path: path where the annotated video will be saved
    """
    if not saving_path:
        name, extension = video_path.split('.')
        saving_path = f'{name}_annotated.{extension}'
    cap = cv2.VideoCapture(video_path)
    frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(saving_path, fourcc,30,(frame_width,frame_height))

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model(frame)
            annotated_frame = process_frame(frame, model, mapper)
            video_writer.write(annotated_frame)
        else:
            break
    cap.release()
    print(f'Annotated video saved to {saving_path}')