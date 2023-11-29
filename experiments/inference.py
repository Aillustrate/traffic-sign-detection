import logging

import cv2
import numpy as np

from label2name import Mapper
from ultralytics import YOLO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Detector:
    def __init__(self, model: YOLO, mapper: Mapper):
        """
        param model: the YOLO model
        param mapper: initialized mapper object, which maps labels to names
        """
        self.model = model
        self.mapper = mapper

    def process_frame(
        self, frame, verbose: bool = False, conf: float = 0.5
    ) -> np.ndarray:
        """
        Detects traffic signs on an image
        param frame: frame from a video or path to the image
        param verbose: verbose predictions
        param conf: confidence threshold
        return: annotated image
        """
        results = self.model(frame, verbose=verbose, conf=conf)
        result = self.mapper.replace_names(results[0])
        annotated_frame = result.plot()
        return annotated_frame

    def process_video(self, video_path: str, saving_path: str = None, **kwargs):
        """
        Detects traffic signs on a video
        param video_path: path to the video
        param saving_path: path where the annotated video will be saved
        """
        if not saving_path:
            name, extension = video_path.split(".")
            saving_path = f"{name}_annotated.{extension}"
        cap = cv2.VideoCapture(video_path)
        frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(
            saving_path, fourcc, 30, (frame_width, frame_height)
        )

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                annotated_frame = self.process_frame(frame, verbose=False, **kwargs)
                video_writer.write(annotated_frame)
            else:
                break
        cap.release()
        logging.info(f"Annotated video saved to {saving_path}")
