import json
from typing import Union
import os

import marshmallow_dataclass

from game.equipment import EquipmentData

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
EQUIPMENT_PATH: str = os.path.join(BASE_DIR, 'data', 'equipment.json')


def read_json(file_path: str, encoding: str = "utf-8") -> Union[dict, list]:
    """
    Чтение данных из json-файла.
    """
    try:
        with open(file_path, encoding=encoding) as f:
            return json.load(f)
    except Exception:
        raise


def load_equipment() -> EquipmentData:
    """
    Функция, которая переводит JSON-данные, полученные из файла equipment.json, в датакласс EquipmentData.
    """
    try:
        return marshmallow_dataclass.class_schema(EquipmentData)().load(
            data=read_json(EQUIPMENT_PATH)
        )
    except Exception:
        raise
