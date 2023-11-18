import os
import gc
import torch
from ultralytics import YOLO

def get_model(version=None, checkpoint_path=None, model_name='yolov8m'):
    if version is not None:
        checkpoint_path = os.path.join('runs', 'detect', f'{model_name}{version}', 'best.pt')
    else:
        checkpoint_path = checkpoint_path or f'{model_name}.pt'
    return YOLO(checkpoint_path)


def cleanup():
    gc.collect()
    torch.cuda.empty_cache()

def get_labels(path):
    labels = []
    with open(path) as f:
        labels = list(map(lambda x: x.strip(), f.readlines()))
    return labels