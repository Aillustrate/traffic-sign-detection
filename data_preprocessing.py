import os
import sys
import json
from typing import Set
from tqdm.auto import tqdm
from shutil import copyfile, move

sys.path.append('./JSON2YOLO')
from JSON2YOLO.general_json2yolo import convert_coco_json
from project_utils import get_labels

class DataPreprocessor:
    def __init__(self, source_dir:str, images_dir:str, labels_fname:str='labels.txt', data_path:str='trafic_signs.yaml'):
        self.source_dir = source_dir
        self.source_img_dir = os.path.join(source_dir, images_dir)
        self.labels_path = os.path.join(source_dir, labels_fname)
        self.data_path = data_path
        self.__TEMP_DIR = 'new_dir'
        self.__train_dir = os.path.join('datasets', 'train_annotation')
        self.__val_dir = os.path.join('datasets', 'val_annotation')
    
    def convert2yolo(self):
        train_labels = self.__covert_labels(train=True)
        val_labels = self.__covert_labels(train=False)
        train_counter, val_counter = self.__split_images(train_labels, val_labels)
        print(f'Data was successfully converted to YOLO format. The dataset contains {train_counter} train images and {val_counter} val images')
        save_data()
        print(f'{self.data_path} file created. Use it as `data` parameter to train the model.')
        

    def __covert_labels(self, train:bool):
        split = 'train' if train else 'val'
        target_dir = os.path.join('datasets', f'{split}_annotation')
        json_fname = f'{split}_anno.json'
        temp_labels_dir = f'{split}_anno'
        os.makedirs(target_dir, exist_ok=True)
        move(os.path.join(self.source_dir, json_fname), os.path.join(target_dir, json_fname))
        for folder in ['labels', 'images']:
            os.makedirs(os.path.join(target_dir, folder), exist_ok=True)
        convert_coco_json(target_dir)
        for fname in tqdm(os.listdir(os.path.join(self.__TEMP_DIR, 'labels', temp_labels_dir))):
            move(os.path.join(self.__TEMP_DIR, 'labels', temp_labels_dir, fname), os.path.join(target_dir, 'labels', fname))
        labels = set([label.split('.')[0] for label in os.listdir(os.path.join(target_dir, 'labels'))])
        return labels

    def __split_images(self, train_labels:Set[str], val_labels:Set[str]):
        train_counter = 0
        val_counter = 0
        for img_fname in os.listdir(self.source_img_dir):
            name = img_fname.split('.')[0]
            if name in train_labels:
                move(os.path.join(self.source_img_dir, img_fname), os.path.join(self.__train_dir,'images', img_fname))
                train_counter += 1
            if name in val_labels:
                move(os.path.join(self.source_img_dir, img_fname), os.path.join(self.__val_dir,'images', img_fname))
                val_counter += 1
        return train_counter, val_counter

    def prepare_data(self):
        labels = get_labels(self.labels_path)
        data = [{'train': self.__train_die, 'val': self.__val_dir, 'nc':len(labels), 'names': labels}]
        return data
    
    def save_data(self):
        data = self.prepare_data()
        with open(self.data_path, 'w+',) as f:
            yaml.dump_all(data, f, sort_keys=False)
        
    
