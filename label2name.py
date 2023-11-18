import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

from project_utils import get_labels

class Mapper:
    def __init__(self, url:str, labels_path, table_path:str='traffic_signs.csv', dict_path:str='mapping.json'):
        self.url = url
        self.labels_path = labels_path
        self.table_path = table_path
        self.dict_path = dict_path
        self.signs = []
        self.mapping = {}
    
    def create(self, signs:pd.DataFrame=None, save_table:bool=True, save_dict:bool=True):
        if signs:
            self.signs = signs
        else:
            self.signs = self.parse_table(save=save_table)
        labels = get_labels(self.labels_path)
        self.mapping = self.get_mapping(labels)
        if save_dict:
            with open(self.dict_path, 'w') as jf:
                json.dump(self.mapping, jf, ensure_ascii=False)
            print(f'Mapping saved to {self.dict_path}')
        
    def parse_table(self, columns=['id','name','comment'], save=True):
        data = []
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
        tables = soup.find_all('table', class_='wikitable')
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:
                    data.append([ele for ele in cols if ele]) 
        df = pd.DataFrame(data, columns=columns)
        df = df.set_index('id')
        if save:
            df.to_csv(self.table_path)
            print(f'Parsed table saved to {self.table_path}')
        return df

    def get_name(self, label):
        row = self.signs['name'].loc[self.signs.index == label].values
        if row.any():
            return str(row[0])
        return ''

    def get_name_by_label(self, label):
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

    def get_mapping(self, labels):
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
    
    def label2name(self, label):
        assert len(self.mapping) > 0, f'Please create mapping calling the `create` method'
        return self.mapping.get(label, '')
