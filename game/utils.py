import json
from typing import Union
import os

import marshmallow_dataclass

from game.equipment import EquipmentData

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
EQUIPMENT_PATH: str = os.path.join(BASE_DIR, 'data', 'equipment.json')


def read_json(file_path: str, encoding: str = "utf-8") -> Union[dict, list]:
    try:
        with open(file_path, encoding=encoding) as f:
            return json.load(f)
    except Exception:
        raise  # TODO: дописать исключение!


def load_equipment() -> EquipmentData:
    try:
        return marshmallow_dataclass.class_schema(EquipmentData)().load(
            data=read_json(EQUIPMENT_PATH)
        )
    except Exception:
        raise  # TODO: дописать исключение!

    #
    #
    #         equipment_file = open("data/equipment.json")
    # data = json.load(...)
    # equipment_schema = marshmallow_dataclass.class_schema(...)
    # try:
    #     return equipment_schema().load(data)
    # except marshmallow.exceptions.ValidationError:
    #     raise ValueError

#
# eq = load_equipment()
# print(eq.get_weapon('топорик'))
# print(eq.armors)
# print(eq.get_armor_names)
