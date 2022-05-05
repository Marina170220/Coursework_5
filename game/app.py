from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from game.base import Game
from game.characters import characters_classes
from game.equipment import EquipmentData
from game.hero import Player, Hero, Enemy
from game.utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False

EQUIPMENT: EquipmentData = load_equipment()
heroes: Dict[str, Hero] = dict()  # словарь с героями
game = Game()  # инициализируем класс игры


def render_choose_character_template(**kwargs):
    """
    Страница выбора героя или противника.
    Return: шаблон страницы выбора персонажа.
    """
    return render_template('hero_choosing.html',
                           classes=characters_classes.keys(),
                           result=EQUIPMENT,
                           **kwargs
                           )


def game_processing(func):
    """
    Функция - декоратор для проверки запуска игры и наличия результатов.
    Return: шаблон страницы боя или главной страницы, если игра окончена.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if game.game_is_running:
            return func(*args, **kwargs)
        if game.game_results:
            results = game.game_results
            return render_template('fight.html', heroes=heroes, result=results)
        return redirect(url_for('menu_page'))

    return wrapper


@app.route("/")
def menu_page():
    """
    Начальная страница.
    Return: шаблон начальной страницы.
    """
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    """
    Страница выбора героя.
    Return: страница выбора героя и переход на страницу выбора противника.
    """
    if request.method == "GET":
        return render_choose_character_template(header='Выберите героя', next_button='Выберите противника')

    elif request.method == "POST":
        heroes['player'] = Player(
            character_class=characters_classes[request.form['character_class']],
            weapon=EQUIPMENT.get_weapon(request.form['weapon']),
            armor=EQUIPMENT.get_armor(request.form['armor']),
            name=request.form['name']
        )

    return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    """
    Страница выбора противника.
    Return: страница выбора противника и переход на страницу начала боя.
    """
    if request.method == "GET":
        return render_choose_character_template(header='Выберите противника', next_button='Начать битву')

    elif request.method == "POST":
        heroes['enemy'] = Enemy(
            character_class=characters_classes[request.form['character_class']],
            weapon=EQUIPMENT.get_weapon(request.form['weapon']),
            armor=EQUIPMENT.get_armor(request.form['armor']),
            name=request.form['name']
        )

    return redirect(url_for('start_fight'))


@app.route("/fight/")
def start_fight():
    """
    Страница начала боя.
    Return: если герой и противник выбраны - страница начала боя, иначе - возврат на начальную страницу.
    """
    if 'player' in heroes and 'enemy' in heroes:
        game.start_game(**heroes)
        return render_template('fight.html', heroes=heroes, result='Битва началась!')
    return redirect(url_for('menu_page'))


@app.route("/fight/hit")
@game_processing
def hit():
    """
    Кнопка нанесения удара.
    Если игра идет - вызываем метод player.hit() экземпляра класса арены,
    иначе пропускаем срабатывание метода (просто рендерим шаблон с текущими данными)
    Return: шаблон с текущими данными.
    """
    results = game.player_hit()
    return render_template('fight.html', heroes=heroes, result=results)


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    """
    Кнопка использования умения героя.
    Return: шаблон с текущими данными.
    """
    results = game.player_use_skill()
    return render_template('fight.html', heroes=heroes, result=results)


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    """
    Кнопка пропуск хода героем. Вызываем здесь функцию хода противника.
    Return: шаблон с текущими данными.
    """
    results = game.next_turn()
    return render_template('fight.html', heroes=heroes, result=results)


@app.route("/fight/end-fight")
def end_fight():
    """
    Кнопка завершения игры.
    Return: переход в главное меню.
    """
    return redirect(url_for('menu_page'))


if __name__ == "__main__":
    app.run(debug=True)
