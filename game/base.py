from random import randint
from typing import Optional

from game.hero import Hero


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=BaseSingleton):
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_is_running = False
        self.game_results = ''

    STAMINA_PER_ROUND = 1

    def start_game(self, player: Hero, enemy: Hero):
        """
        НАЧАЛО ИГРЫ.
        Присваиваем экземпляру класса аттрибуты "игрок" и "противник",
        а также выставляем True для свойства "началась ли игра"
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        if self.player.health <= 0 and self.enemy.health <= 0:
            return self._end_game('В борьбе равных нет победителей')
        if self.player.health <= 0:
            return self._end_game(f'{self.enemy.name.title()} оказался сильнее')
        if self.enemy.health <= 0:
            return self._end_game(f'Победа! {self.enemy.name.title()} повержен.')
        return None

        # TODO ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # TODO проверка здоровья игрока и врага и возвращение результата строкой:
        # TODO может быть три результата:
        # TODO Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # TODO если Здоровья игроков в порядке то ничего не происходит

    def next_turn(self) -> str:  # Удар противника TODO проверить и подкорректировать ф-цию
        if results := self._check_players_hp():
            return results
        if not self.game_is_running:
            return self.game_results
        results = self.enemy_hit()
        self._stamina_regeneration()
        return results

    # # TODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
    #         # TODO срабатывает когда игроп пропускает ход или когда игрок наносит удар.
    #         # TODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
    #         # TODO если result -> возвращаем его
    #         # TODO если же результата пока нет и после завершения хода игра продолжается,
    #         # TODO тогда запускаем процесс регенирации стамины и здоровья для игроков (self._stamina_regeneration)
    #         # TODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага

    def _stamina_regeneration(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

        # TODO регенерация здоровья и стамины для игрока и врага за ход
        # TODO в этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # TODO главное чтобы оно не привысило максимальные значения (используйте if)

    def _end_game(self, results: str) -> str:
        self.game_is_running = False
        self.game_results = results
        return results

        # TODO КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # TODO очищаем синглтон - self._instances = {}
        # TODO останавливаем игру (game_is_running)
        # TODO возвращаем результат

    def enemy_hit(self) -> str:
        # if randint(0, 100) < 10:
        #     self.enemy_use_skill()
        # else:
        delta_damage: Optional[float] = self.enemy.hit(self.player)
        if delta_damage is not None:
            self.player.take_hit(delta_damage)
            results = f'<p>{self.enemy.name.title()}, используя {self.enemy.weapon.name}, пробивает ' \
                      f'вашу броню {self.player.armor.name} и наносит вам {delta_damage} урона.</p>'
        else:
            results = f'<p>Противник {self.enemy.name.title()} попытался использовать {self.enemy.weapon.name},' \
                      f'но у него не хватило выносливости для удара</p>'
        return results

    # TODO КНОПКА УДАР ПРОТИВНИКА -> return result: str
    # TODO получаем результат от функции self.enemy.hit
    # TODO запускаем следующий ход
    # TODO возвращаем результат удара строкой

    def player_hit(self) -> str:
        delta_damage: Optional[float] = self.player.hit(self.enemy)
        if delta_damage is not None:
            self.enemy.take_hit(delta_damage)
            return f'<p>Оружием {self.player.weapon.name} вы нанесли противнику {self.enemy.name.title()} ' \
                   f'{delta_damage} урон</p><p>{self.next_turn()}</p>'
        return f'<p>Недостаточно сил для использования {self.player.weapon.name}</p><p>{self.next_turn()}</p>'

        # TODO КНОПКА УДАР ИГРОКА -> return result: str
        # TODO получаем результат от функции self.player.hit
        # TODO запускаем следующий ход
        # TODO возвращаем результат удара строкой

    def player_use_skill(self) -> str:
        delta_damage: Optional[float] = self.player.use_skill()  # TODO вынести эту часть в отдельную ф-цию (исп-ся так же в player_hit, enemy_hit)
        if delta_damage is not None:
            self.enemy.take_hit(delta_damage)
            return f'<p>С помощью боевого умения {self.player.character_class.skill.name} вы нанесли противнику ' \
                   f'{self.enemy.name.title()} {delta_damage} урон</p><p>{self.next_turn()}</p>'
        return f'<p>Недостаточно сил для использования умения {self.player.character_class.skill.name}</p>' \
               f'<p>{self.next_turn()}</p>'

        # TODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # TODO получаем результат от функции self.use_skill
        # TODO включаем следующий ход
        # TODO возвращаем результат удара строкой

    # def enemy_use_skill(self) -> str:
    #     delta_damage: Optional[float] = self.enemy.use_skill()
    #     if delta_damage is not None:
    #         self.player.take_hit(delta_damage)
    #         return f'<p>Противник использует умение {self.enemy.character_class.skill.name} ' \
    #                f'и наносит вам {delta_damage} урона</p>'
    #     return f'<p>Противник попытался применить к вам {self.enemy.character_class.skill.name}, ' \
    #            f'но у него не хватило сил</p>'
