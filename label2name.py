import json
import os
from typing import Dict, List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from project_utils import get_labels


class Mapper:
    def __init__(
        self,
        labels_path,
        table_path: str = "traffic_signs.csv",
        dict_path: str = "mapping.json",
    ):
        """

        :param labels_path: Path to the file containing labels
        :param table_path: Path where the parsed table will be saved
        :param dict_path: Path where the final mapping dict will be saved
        """
        self.labels_path = labels_path
        self.table_path = table_path
        self.dict_path = dict_path
        self.signs = []
        self.mapping = {}

    def create(
        self,
        signs: pd.DataFrame = None,
        url: str = "",
        save_table: bool = True,
        save_dict: bool = True,
    ):
        """
        Creates the mapping from sign label to sign name
        :param signs: pandas dataframe containing traffic sign codes (e.g. 1.2, 5.2.1 etc) and their names, if it already exists
        :param url: URL of the webpage to parse in case the `signs` dataframe is not provided
        :param save_table: wheather to save the parsed table
        :param save_dict: wheather to save the final mapping dict
        """
        if signs:
            self.signs = signs
        else:
            self.signs = self.parse_table(url, save=save_table)
        labels = get_labels(self.labels_path)
        self.mapping = self.get_mapping(labels)
        if save_dict:
            with open(self.dict_path, "w") as jf:
                json.dump(self.mapping, jf, ensure_ascii=False)
            print(f"Mapping saved to {self.dict_path}")

    def parse_table(
        self,
        url: str,
        columns: List[str] = ["id", "name", "comment"],
        save: bool = True,
    ) -> pd.DataFrame:
        """
        Parses a table containing info about sign codes (e.g. 1.2, 5.2.1 etc) and their names
        :param url: URL of the webpage to parse
        :param columns: column names
        :param save: wheather to save the parsed table
        :return: dataframe containing info about sign codes (e.g. 1.2, 5.2.1 etc) and their names
        """
        data = []
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        tables = soup.find_all("table", class_="wikitable")
        for table in tables:
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                if cols:
                    data.append([ele for ele in cols if ele])
        df = pd.DataFrame(data, columns=columns)
        df = df.set_index("id")
        if save:
            df.to_csv(self.table_path)
            print(f"Parsed table saved to {self.table_path}")
        return df

    def get_name(self, code: str) -> str:
        """
        Gets a sign name by its code. Sometimes returns empty string or 'nan'
        :param code: sign code with do.ts (e.g. 1.2, 5.2.1 etc)
        :return: sign name
        """
        row = self.signs["name"].loc[self.signs.index == code].values
        if row.any():
            return str(row[0])
        return ""

    def get_name_by_label(self, label: str) -> str:
        """
        Gets a sign name by its label. Sometimes returns empty string or 'nan'
        :param label: label with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: sign name or empty string
        """
        full_label = label.replace("_", ".")
        name = self.get_name(full_label)
        if name:
            return name
        subclass_label = label.replace("_", ".") + "_1"
        name = self.get_name(subclass_label)
        if name:
            return name
        hyperclass_label = ".".join(label.split("_")[:-1])
        name = self.get_name(hyperclass_label)
        return name

    def get_mapping(self, labels: List[str]) -> Dict[str, str]:
        """
        Get a mapping from labels to traffic sign names
        :param labels: list of labels with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: dict with labels as keys and sign names as values
        """
        mapping = []
        for label in labels:
            name = self.get_name_by_label(label)
            mapping.append([label, name])
        mapping = sorted(mapping, key=lambda x: x[0])
        mapping_with_filled_blanks = []
        for i, (label, name) in enumerate(mapping[1:]):
            if name in ["", "nan"]:
                name = mapping_with_filled_blanks[i - 1][1]
            mapping_with_filled_blanks.append((label, name))
        return dict(mapping_with_filled_blanks)

    def label2name(self, label: str) -> str:
        """
        Gets sign name by label from the final mapping
        :param label: label with under_scores (e.g. 1_2, 5_2_1 etc)
        :return: sign name
        """
        assert (
            len(self.mapping) > 0
        ), f"Please create mapping calling the `create` method"
        return self.mapping.get(label, "")
