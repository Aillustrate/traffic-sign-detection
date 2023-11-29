import logging
import os
import sys
from shutil import move
from typing import Any, Dict, List, Set, Tuple

import yaml
from tqdm.auto import tqdm

sys.path.append("./JSON2YOLO")
from JSON2YOLO.general_json2yolo import convert_coco_json
from project_utils import get_labels

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DataPreprocessor:
    def __init__(
        self,
        source_dir: str,
        images_dir: str,
        labels_fname: str = "labels.txt",
        data_path: str = "trafic_signs.yaml",
    ):
        """

        :param source_dir: Dataset directory
        :param images_dir: Directory where images are stored (located inside the dataset directory)
        :param labels_fname: Filename containing the list of target labels
        :param data_path: Path to yaml file that is fed to YOLO as `data` argument
        """
        self.source_dir = source_dir
        self.source_img_dir = os.path.join(source_dir, images_dir)
        self.labels_path = os.path.join(source_dir, labels_fname)
        self.data_path = data_path
        self.__TEMP_DIR = "new_dir"
        self.__train_dir = os.path.join("datasets", "train_annotation")
        self.__val_dir = os.path.join("datasets", "val_annotation")

    def preprocess(self):
        """
        Preprocesses data: converts it to YOLO fomat, splits into train and val, creates yaml file for the model
        """
        train_labels = self.__covert_labels(train=True)
        val_labels = self.__covert_labels(train=False)
        train_counter, val_counter = self.__split_images(train_labels, val_labels)
        logging.info(
            f"Data was successfully converted to YOLO format. The dataset contains {train_counter} train images and {val_counter} val images"
        )
        self.save_data()
        logging.info(
            f"{self.data_path} file created. Use it as `data` parameter to train the model."
        )

    def __covert_labels(self, train: bool) -> Set[str]:
        """
        Converts labels to YOLO format
        :param train: Whether the split is train (otherwise val)
        :return: Labels of train/validation images
        """
        split = "train" if train else "val"
        target_dir = os.path.join("datasets", f"{split}_annotation")
        json_fname = f"{split}_anno.json"
        temp_labels_dir = f"{split}_anno"
        os.makedirs(target_dir, exist_ok=True)
        move(
            os.path.join(self.source_dir, json_fname),
            os.path.join(target_dir, json_fname),
        )
        for folder in ["labels", "images"]:
            os.makedirs(os.path.join(target_dir, folder), exist_ok=True)
        convert_coco_json(target_dir)
        for fname in tqdm(
            os.listdir(os.path.join(self.__TEMP_DIR, "labels", temp_labels_dir))
        ):
            move(
                os.path.join(self.__TEMP_DIR, "labels", temp_labels_dir, fname),
                os.path.join(target_dir, "labels", fname),
            )
        labels = set(
            [
                label.split(".")[0]
                for label in os.listdir(os.path.join(target_dir, "labels"))
            ]
        )
        return labels

    def __split_images(
        self, train_labels: Set[str], val_labels: Set[str]
    ) -> Tuple[int, int]:
        """
        Splits images into train and validation
        :param train_labels: Labels of train images
        :param val_labels: Labels of test images
        :return: Numbers of train and val images
        """
        train_counter = 0
        val_counter = 0
        for img_fname in os.listdir(self.source_img_dir):
            name = img_fname.split(".")[0]
            if name in train_labels:
                move(
                    os.path.join(self.source_img_dir, img_fname),
                    os.path.join(self.__train_dir, "images", img_fname),
                )
                train_counter += 1
            if name in val_labels:
                move(
                    os.path.join(self.source_img_dir, img_fname),
                    os.path.join(self.__val_dir, "images", img_fname),
                )
                val_counter += 1
        return train_counter, val_counter

    def prepare_data(self) -> List[Dict[str, Any]]:
        """
        Creates data dict to save into yaml file
        :return: data dict to save into yaml file
        """
        labels = get_labels(self.labels_path)
        data = [
            {
                "train": self.__train_die,
                "val": self.__val_dir,
                "nc": len(labels),
                "names": labels,
            }
        ]
        return data

    def save_data(self):
        """
        Creates the data dict and saves it into the yaml file, which will be used by YOLO
        """
        data = self.prepare_data()
        with open(self.data_path, "w+") as f:
            yaml.dump_all(data, f, sort_keys=False)
