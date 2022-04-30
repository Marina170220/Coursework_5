from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from game.base import Game
from game.characters import characters_classes, Character
from game.equipment import EquipmentData
from game.hero import Player, Hero, Enemy
from game.utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False

EQUIPMENT: EquipmentData = load_equipment()
heroes: Dict[str, Hero] = dict()  # словарь с героями
game = Game() # TODO инициализируем класс арены

def render_choose_character_template(*args, **kwargs):
    return render_template('hero_choosing.html',
                           classes=characters_classes.keys(),
                           result=EQUIPMENT,
                           **kwargs
                           )

def game_processing(func):
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
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
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

    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы


@app.route("/fight/")
def start_fight():
    if 'player' in heroes and 'enemy' in heroes:
        game.start_game(**heroes)
        return render_template('fight.html', heroes=heroes, result='Битва началась!')
    return redirect(url_for('menu_page'))

    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)


@app.route("/fight/hit")
@game_processing
def hit():
    results = game.player_hit()
    return render_template('fight.html', heroes=heroes, result=results)


    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    results = game.player_use_skill()
    return render_template('fight.html', heroes=heroes, result=results)
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    results = game.next_turn()
    return render_template('fight.html', heroes=heroes, result=results)
    # TODO кнопка пропуск хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    return redirect(url_for('menu_page'))

    # TODO кнопка завершить игру - переход в главное меню



if __name__ == "__main__":
    app.run(debug=True)
