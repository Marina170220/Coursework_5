from dataclasses import dataclass
from typing import List
from random import uniform


@dataclass
class Armor:
    """
    Класс брони персонажа.
    """
    id: int
    name: str
    defence: float  # Очки защиты
    stamina_per_turn: float  # Количество затрачиваемой выносливости за ход


@dataclass
class Weapon:
    """
    Класс оружия персонажа.
    """
    id: int
    name: str
    min_damage: float  # Минимальный урон
    max_damage: float  # Максимальный урон
    stamina_per_hit: float  # Количество затрачиваемой выносливости за удар

    @property
    def damage(self) -> float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    """
    Экипировка персонажа, включает в себя оружие и броню.
    """
    weapons: List[Weapon]
    armors: List[Armor]

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.weapons:
            if weapon.name == weapon_name:
                return weapon
        raise RuntimeError  # TODO: написать своё исключение!

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.armors:
            if armor.name == armor_name:
                return armor
        raise RuntimeError  # TODO: написать своё исключение!

    @property
    def get_weapon_names(self) -> List[str]:
        return [weapon.name for weapon in self.weapons]

    @property
    def get_armor_names(self) -> List[str]:
        return [armor.name for armor in self.armors]
