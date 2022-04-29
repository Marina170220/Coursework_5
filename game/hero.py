from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import Type, Optional

from game.characters import Character
from game.equipment import Weapon, Armor

BASE_STAMINA_PER_ROUND = 0.4  # константа, сколько очков выносливости персонаж восстанавливает за ход. TODO вынести в конфиг приложения


class Hero(ABC):
    def __init__(self, character_class: Type[Character], weapon: Weapon, armor: Armor, name: str):
        self.character_class = character_class
        self.weapon = weapon
        self.armor = armor
        self._stamina = self.character_class.stamina_points
        self._health = self.character_class.health_points
        self._is_skill_used: bool = False
        self.name = name

    @property
    def health(self):
        return round(self._health, 1)

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def _total_armor(self) -> float:  # броня цели
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.character_class.armor_modifier
        return 0

    def base_hit(self, target: Hero) -> Optional[float]:
        # Если выносливости достаточно для удара, идем дальше, иначе возвращаем 0. Считаем урон, который можем нанести,
        # далее считаем броню,  ...
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None
        attacking_hero_damage = self.weapon.damage * self.character_class.attack_modifier  # Урон атакующего
        dealt_damage = attacking_hero_damage - target._total_armor  # тотальный урон
        if dealt_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit  # TODO вынести в отдельную ф-цию
        return round(dealt_damage, 1)

    def take_hit(self, damage: float):  # Принять урон
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def regenerate_stamina(self):  # регенерация
        delta_stamina = BASE_STAMINA_PER_ROUND * self.character_class.stamina_modifier
        if self.stamina + delta_stamina <= self.character_class.stamina_points:
            self.stamina += delta_stamina
        else:
            self.stamina = self.character_class.stamina_points

    def use_skill(self) -> Optional[float]:
        if not self._is_skill_used and self.stamina - self.character_class.skill.stamina:  # TODO можно вынести в отдельную переменную, использовать здесь и в ф-ции hit у Enemy
            self._is_skill_used = True
            return round(self.character_class.skill.damage, 1)
        return None  # Если не получилось использовать скилл, возвращаем None

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        ...


class Enemy(Hero):  # Противник (персонаж, за которого играет комп)
    def hit(self, target: Hero) -> Optional[float]:  # Так наносит удар противник
        if randint(0, 100) < 10 and self.stamina >= self.character_class.skill.stamina and not self._is_skill_used:
            self.use_skill()
        return self.base_hit(target)


class Player(Hero):  # Герой, за которого играет игрок
    def hit(self, target: Hero) -> Optional[float]:  # Наносит удар герой
        return self.base_hit(target)
