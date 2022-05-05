from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, Optional

from game.characters import Character
from game.equipment import Weapon, Armor

BASE_STAMINA_PER_ROUND = 1  # константа, показывающая, сколько очков выносливости персонаж восстанавливает за ход.


class Hero(ABC):
    def __init__(self, character_class: Type[Character], weapon: Weapon, armor: Armor, name: str):
        self.character_class = character_class  # Класс персонажа
        self.weapon = weapon
        self.armor = armor
        self._stamina = self.character_class.max_stamina
        self._health = self.character_class.max_health
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
    def _total_armor(self) -> float:
        """
        Броня цели. Если у персонажа, которого атакуют, достаточно очков выносливости для использования своей брони,
        тогда рассчитываем показатель брони цели.
        Return: показатель брони цели либо 0 (броня игнорируется).
        """
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.character_class.armor_modifier
        return 0

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        ...

    def base_hit(self, target: Hero) -> Optional[float]:
        """
        Нанесение удара. Проверяем, если выносливости достаточно для удара, идем дальше, иначе возвращаем None
        (герой пропускает ход). Считаем урон, который можем нанести, и выносливость после удара.
        Param target: герой или противник.
        Return: урон либо 0, если недостаточно выносливости для удара.
        """
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None
        attacking_hero_damage = self.weapon.damage * self.character_class.attack_modifier  # Урон атакующего
        total_damage = attacking_hero_damage - target._total_armor  # тотальный урон от удара
        if total_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(total_damage, 1)

    def take_hit(self, damage: float):
        """
        Принимаем удар и рассчитываем оставшийся уровень здоровья.
        Вычитаем из очков здоровья цели показатель урона.
        Param damage: наносимый урон при ударе.
        """
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def regenerate_stamina(self):
        """
        Регенерация. Восстанавливаем выносливость атакующего и защищающего.
        Прибавляем к очкам выносливости персонажа константу, умноженную на его модификатор выносливости.
        Проверяем, чтобы количество выносливости после восстановления не превысило максимальное значение.
        """
        delta_stamina = BASE_STAMINA_PER_ROUND * self.character_class.stamina_modifier
        if self.stamina + delta_stamina <= self.character_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.character_class.max_stamina

    def use_skill(self) -> Optional[float]:
        """
        Использование умения героя.
        Как игрок, так и компьютер могут использовать умение только один раз за бой.
        Return: Если умением удалось воспользоваться, возвращаем нанесённый противнику урон.
        Если умение не получилось использовать, возвращаем None.
        """
        if not self._is_skill_used and self.stamina >= self.character_class.skill.stamina:
            self._is_skill_used = True
            return round(self.character_class.skill.damage, 1)
        return None


class Enemy(Hero):
    """
    Класс противника (персонажа, за которого играет комп)
    """

    def hit(self, target: Hero) -> Optional[float]:
        """
        Удар наносит противник.
        Param target: герой пользователя.
        Return: удар.
        """
        return self.base_hit(target)


class Player(Hero):
    """
    Класс героя (персонажа, за которого играет пользователь)
    """

    def hit(self, target: Hero) -> Optional[float]:
        """
        Удар наносит герой.
        Param target: герой противника.
        Return: удар.
        """
        return self.base_hit(target)
