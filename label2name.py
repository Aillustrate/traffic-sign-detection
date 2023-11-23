import os
import re
import json
import requests
from typing import List
import pandas as pd
from ultralytics.engine.results import Boxes
from bs4 import BeautifulSoup

from project_utils import get_labels

class Mapper:
    def __init__(self, signs: pd.DataFrame, labels_path: str, saving_path:str='mapping.json'):
        """
        :param labels_path: Path to the file containing labels
        :param table_path: Path where the parsed table will be saved
        :param dict_path: Path where the final mapping dict will be saved
        """
        self.signs = signs
        self.labels_path = labels_path
        self.saving_path = saving_path
        self.mapping = {}
    
    def create(self, save:bool=True):
        """
        Creates the mapping from sign label to sign name
        :param signs: Pandas dataframe containing traffic sign codes (e.g. 1.2, 5.2.1 etc) and their names, if it already exists
        :param url: URL of the webpage to parse in case the `signs` dataframe is not provided
        :param save_table: Whether to save the parsed table
        :param save_dict: Whether to save the final mapping dict
        """
        labels = get_labels(self.labels_path)
        self.mapping = self.get_mapping(labels)
        if save:
            with open(self.saving_path, 'w') as jf:
                json.dump(self.mapping, jf, ensure_ascii=False)
            print(f'Mapping saved to {self.saving_path}')

    def get_name(self, label:str):
        """
        Gets a sign name by its code. Sometimes returns empty string or 'nan'
        :param code: Sign code with do.ts (e.g. 1.2, 5.2.1 etc)
        :return: Sign name
        """
        row = self.signs['name'].loc[self.signs.id == label].values
        if row.any():
            return str(row[0])
        return ''

    def get_name_by_label(self, label:str):
        """
        Gets a sign name by its label. Sometimes returns empty string or 'nan'
        :param label: Label with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: Sign name or empty string
        """
        full_label = label.replace('_', '.')
        name = self.get_name(full_label)
        if name:
            return name
        subclass_label = label.replace('_', '.')+'_1'
        name = self.get_name(subclass_label)
        if name:
            return name
        hyperclass_label = '.'.join(label.split('_')[:-1])
        name = self.get_name(hyperclass_label)
        return name

    def get_mapping(self, labels:List[str]):
        """
        Get a mapping from labels to traffic sign names
        :param labels: List of labels with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: Dict with labels as keys and sign names as values
        """
        mapping = []
        for label in labels:
            name = self.get_name_by_label(label)
            mapping.append([label, name])
        mapping = sorted(mapping, key=lambda x: x[0])
        mapping_with_filled_blanks = []
        for i, (label, name) in enumerate(mapping[1:]):
            if name in ['', 'nan']:
                name = mapping_with_filled_blanks[i-1][1]
            mapping_with_filled_blanks.append((label, name))
        return dict(mapping_with_filled_blanks)
    
    def label2name(self, label:str):
        """
        Gets sign name by label from the final mapping
        :param label: Label with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: Sign name
        """
        assert len(self.mapping) > 0, f'Please create mapping calling the `create` method'
        return self.mapping.get(label, '')
    
    def replace_names(self, result:Boxes) -> Boxes:
        """
        Replaces label names in the model (e.g. {0 : '2_1'} -> {0 : 'Главная дорога'})
        :param label: yolo model
        """
        for key, label in result.names.items():
            if re.match('(.*_.*)+', label):
                code = label.replace('_', '.')
                result.names[key] = self.label2name(label)
        return result
        
