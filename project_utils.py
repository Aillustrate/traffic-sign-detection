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
            "runs", "detect", f"{model_name}{version}", "weights", "best.pt"
        )
    else:
        checkpoint_path = checkpoint_path or f"{model_name}.pt"
    return YOLO(checkpoint_path)


def cleanup():
    """
    Releases memory and collect garbage
    """
    gc.collect()
    torch.cuda.empty_cache()


def get_labels(path: str) -> List[str]:
    """
    Gets list of labels from txt file
    :param path: Path to file with labels
    :return: List of labels
    """
    with open(path) as f:
        labels = list(map(lambda x: x.strip(), f.readlines()))
    return labels

def parse_table(self, url:str, columns:List[str] =['id','name','comment'], save:bool=True, saving_path:str = 'traffic_signs.csv'):
    """
        Parses a table containing info about sign codes (e.g. 1.2, 5.2.1 etc) and their names
        :param url: URL of the webpage to parse
        :param columns: Column names
        :param save: Whether to save the parsed table
        :param saving_path: Path to save the parsed table
        :return: Dataframe containing info about sign codes (e.g. 1.2, 5.2.1 etc) and their names
        """
    data = []
    r = requests.get(url)
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
        df.to_csv(saving_path)
        print(f'Parsed table saved to {saving_path}')
    return df
