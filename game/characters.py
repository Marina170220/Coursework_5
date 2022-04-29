from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict, Type
from game.skills import Skill, powerful_thrust, ferocious_bite


class Character(ABC):
    """
    Базовый класс персонажа
    """

    name: str
    health_points: float
    stamina_points: float
    attack_modifier: float
    stamina_modifier: float
    armor_modifier: float
    skill: Skill


class Hero(Character):
    """
    Класс персонажа Богатырь
    """

    name = "Богатырь"
    health_points = 60.0
    stamina_points = 30.0
    attack_modifier = 0.8
    stamina_modifier = 0.9
    armor_modifier = 1.2
    skill: powerful_thrust


class Snake(Character):
    """
    Класс персонажа Змей
    """

    name = "Горыныч"
    health_points = 50.0
    stamina_points = 25.0
    attack_modifier = 1.8
    stamina_modifier = 1.2
    armor_modifier = 1.0
    skill: ferocious_bite


characters_classes: Dict[str, Type[Character]] = {Hero.name: Hero, Snake.name: Snake}

#     @property
#     def health_points(self):
#         return # TODO возвращаем аттрибут hp в красивом виде
#
#     @property
#     def stamina_points(self):
#         return  # TODO возвращаем аттрибут hp в красивом виде
#
#     def equip_weapon(self, weapon: Weapon):
#         # TODO присваиваем нашему герою новое оружие
#         return f"{self.name} экипирован оружием {self.weapon.name}"
#
#     def equip_armor(self, armor: Armor):
#         # TODO одеваем новую броню
#         return f"{self.name} экипирован броней {self.weapon.name}"
#
#     def _count_damage(self, target: Character) -> int:
#         # TODO Эта функция должна содержать:
#         #  логику расчета урона игрока
#         #  логику расчета брони цели
#         #  здесь же происходит уменьшение выносливости атакующего при ударе
#         #  и уменьшение выносливости защищающегося при использовании брони
#         #  если у защищающегося нехватает выносливости - его броня игнорируется
#         #  после всех расчетов цель получает урон - target.get_damage(damage)
#         #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
#         return damage
#
#     def get_damage(self, damage: int) -> Optional[int]:
#         # TODO получение урона целью
#         #      присваиваем новое значение для аттрибута self.hp
#         pass
#
#     @abstractmethod
#     def hit(self, target: Character) -> str:
#         """
#         этот метод будет переопределен ниже
#         """
#         pass
#
#     def use_skill(self, target: Character) -> str:
#         """
#         метод использования умения.
#         если умение уже использовано возвращаем строку
#         Навык использован
#         Если же умение не использовано тогда выполняем функцию
#         self.unit_class.skill.use(user=self, target=target)
#         и уже эта функция вернем нам строку которая характеризует выполнение умения
#         """
#         pass
#
#
# class PlayerUnit(Character):
#
#     def hit(self, target: Character) -> str:
#         """
#         функция удар игрока:
#         здесь происходит проверка достаточно ли выносливости для нанесения удара.
#         вызывается функция self._count_damage(target)
#         а также возвращается результат в виде строки
#         """
#         pass
#         # TODO результат функции должен возвращать следующие строки:
#         f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
#         f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
#         f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
#
# class EnemyUnit(Character):
#
#     def hit(self, target: Character) -> str:
#         """
#         функция удар соперника
#         должна содержать логику применения соперником умения
#         (он должен делать это автоматически и только 1 раз за бой).
#         Например, для этих целей можно использовать функцию randint из библиотеки random.
#         Если умение не применено, противник наносит простой удар, где также используется
#         функция _count_damage(target
#         """
#         # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
#         f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
#         f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
#         f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
#

