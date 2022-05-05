from random import randint
from typing import Optional, Dict

from game.hero import Hero


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=BaseSingleton):
    """
    Класс игры.
    """

    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_is_running = False
        self.game_results = ''

    def start_game(self, player: Hero, enemy: Hero):
        """
        НАЧАЛО ИГРЫ.
        Присваиваем экземпляру класса аттрибуты "игрок" и "противник",
        а также выставляем True для свойства "началась ли игра".
        Param player: игрок (герой, за которого играет пользователь).
        Param enemy: противник (герой, за которого играет копм).
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        Проверка здоровья игрока и врага.
        Return: результат проверки в виде строки. Может быть три результата:
         - Игрок проиграл битву
         - Игрок выиграл битву
         - Ничья
         Если показатель здоровья игроков в порядке, то ничего не происходит.
        """
        if self.player.health <= 0 and self.enemy.health <= 0:
            return self._end_game('В борьбе равных нет победителей')
        if self.player.health <= 0:
            return self._end_game(f'{self.enemy.name.title()} оказался сильнее')
        if self.enemy.health <= 0:
            return self._end_game(f'Победа! {self.enemy.name.title()} повержен.')
        return None

    def next_turn(self) -> str:
        """
        Функция удара противника, срабатывает, когда игрок пропускает ход или наносит удар.
        Создаем поле result и проверяем, что вернется в результате проверки здоровья игроков.
        Если есть result -> возвращаем его, если же результата пока нет и после завершения хода игра продолжается,
        тогда запускаем процесс регенерации выносливости для игроков и вызываем функцию ответного удара противника.
        Когда противник выполняет ответное действие, он имеет 10%-ный шанс воспользоваться умением.
        Если шанс срабатывает, а умение уже было применено, то компьютер наносит обычный удар.
        Return: строка с результатом удара.
        """
        if results := self._check_players_hp():
            return results
        if not self.game_is_running:
            return self.game_results
        if randint(0, 100) < 10:
            results = self.enemy_use_skill()
            self._stamina_regeneration()
            return results
        results = self.enemy_hit()
        self._stamina_regeneration()
        return results

    def _stamina_regeneration(self):
        """
        Регенерация здоровья и выносливости для игрока и врага за ход.
        """
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def _end_game(self, results: str) -> str:
        """
        ЗАВЕРШЕНИЕ ИГРЫ.
        Останавливаем игру, очищаем синглтон и записываем результат.
        Param results: результат игры.
        Return: строка с результатом игры.
        """
        self.game_is_running = False
        self._instances = {}
        self.game_results = results
        return results

    def enemy_hit(self) -> str:
        """
        Удар противника.
        Return: строка с результатом удара.
        """
        delta_damage: Optional[float] = self.enemy.hit(self.player)
        if delta_damage is not None:
            self.player.take_hit(delta_damage)
            return f'<p>{self.enemy.name.title()}, используя {self.enemy.weapon.name}, пробивает ' \
                   f'вашу броню {self.player.armor.name} и наносит вам {delta_damage} урона.</p>'
        return f'<p>Противник {self.enemy.name.title()} попытался использовать {self.enemy.weapon.name},' \
               f'но у него не хватило выносливости для удара</p>'

    def player_hit(self) -> str:
        """
        Удар игрока.
        После того как игрок нанёс удар, запускаем следующий ход противника.
        Return: строка с результатом удара.
        """
        delta_damage: Optional[float] = self.player.hit(self.enemy)
        if delta_damage is not None:
            self.enemy.take_hit(delta_damage)
            return f'<p>Оружием {self.player.weapon.name} вы нанесли противнику {self.enemy.name.title()} ' \
                   f'{delta_damage} урон</p><p>{self.next_turn()}</p>'
        return f'<p>Недостаточно сил для использования {self.player.weapon.name}</p><p>{self.next_turn()}</p>'

    def player_use_skill(self) -> str:
        """
        Игрок использует умение.
        Return: строка с результатом удара.
        """
        delta_damage: Optional[float] = self.player.use_skill()
        if delta_damage is not None:
            self.enemy.take_hit(delta_damage)
            return f'<p>С помощью боевого умения {self.player.character_class.skill.name} вы нанесли противнику ' \
                   f'{self.enemy.name.title()} {delta_damage} урон</p><p>{self.next_turn()}</p>'
        return f'<p>Недостаточно сил для использования умения {self.player.character_class.skill.name}</p>' \
               f'<p>{self.next_turn()}</p>'

    def enemy_use_skill(self) -> str:
        """
        Противник использует умение.
        Return: строка с результатом удара.
        """
        delta_damage: Optional[float] = self.enemy.use_skill()
        if delta_damage is not None:
            self.player.take_hit(delta_damage)
            return f'<p>Противник использует умение {self.enemy.character_class.skill.name} ' \
                   f'и наносит вам {delta_damage} урона</p>'
        return f'<p>Противник попытался применить к вам {self.enemy.character_class.skill.name}, ' \
               f'но у него не хватило сил</p>'
