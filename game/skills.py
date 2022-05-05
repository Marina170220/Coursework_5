from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skill:
    """
    Класс умения персонажа.
    """
    name: str
    damage: float  # урон
    stamina: float  # требуемая выносливость


powerful_thrust = Skill("мощный укол", 12, 6)
ferocious_bite = Skill("свирепый кусь", 15, 5)
