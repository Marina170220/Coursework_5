from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from game.skills import Skill, powerful_thrust, ferocious_bite


class Character(ABC):
    """
    Базовый класс персонажа
    """

    name: str
    max_health: float  # Максимальное число очков здоровья
    max_stamina: float  # Максимальное число очков выносливости
    attack_modifier: float  # Модификатор атаки
    stamina_modifier: float  # Модификатор выносливости
    armor_modifier: float  # Модификатор защиты
    skill: Skill  # Умение


class Warrior(Character):
    """
    Класс персонажа Богатырь
    """

    name = "Богатырь"
    max_health = 60.0
    max_stamina = 30.0
    attack_modifier = 0.8
    stamina_modifier = 0.9
    armor_modifier = 1.2
    skill = powerful_thrust


class Snake(Character):
    """
    Класс персонажа Змей
    """

    name = "Горыныч"
    max_health = 50.0
    max_stamina = 25.0
    attack_modifier = 1.8
    stamina_modifier = 1.2
    armor_modifier = 1.0
    skill = ferocious_bite


characters_classes: Dict[str, Type[Character]] = {Warrior.name: Warrior, Snake.name: Snake}
