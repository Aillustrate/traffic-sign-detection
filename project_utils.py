import gc
import os
from typing import List

import torch
from ultralytics import YOLO


def get_model(version=None, checkpoint_path=None, model_name="yolov8m") -> YOLO:
    """
    Gets YOLO model: from saved checkpoints or pretrained
    :param version: Last vesrion of the model (number of the most recently changed folder in `runs/detect`)
    :param checkpoint_path: Other path to checkpoints
    :param model_name: Model name (e.g. yolov8m)
    :return: YOLO model
    """
    if version is not None:
        checkpoint_path = os.path.join(
            "runs", "detect", "weights", f"{model_name}{version}", "best.pt"
        )
    else:
        checkpoint_path = checkpoint_path or f"{model_name}.pt"
    return YOLO(checkpoint_path)


def cleanup():
    """
    Releases memory and collect garbage
    :return:
    """
    gc.collect()
    torch.cuda.empty_cache()


def get_labels(path: str) -> List[str]:
    """
    Gets list of labels from txt file
    :param path: path to file with labels
    :return: list of labels
    """
    with open(path) as f:
        labels = list(map(lambda x: x.strip(), f.readlines()))
    return labels
