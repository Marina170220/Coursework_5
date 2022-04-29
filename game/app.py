from typing import Dict, Type

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
game = Game()

def render_choose_character_template(*args, **kwargs):
    return render_template('hero_choosing.html',
                           classes=characters_classes.keys(),
                           result=EQUIPMENT,
                           **kwargs
                           )


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




# heroes = {
#     "player": BaseUnit,
#     "enemy": BaseUnit
# }
#
# arena =  ... # TODO инициализируем класс арены
#
#

#
#
#
#
# @app.route("/fight/hit")
# def hit():
#     # TODO кнопка нанесения удара
#     # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
#     # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
#     # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
#     pass
#
#
# @app.route("/fight/use-skill")
# def use_skill():
#     # TODO кнопка использования скилла
#     # TODO логика пркатикчески идентична предыдущему эндпоинту
#     pass
#
#
# @app.route("/fight/pass-turn")
# def pass_turn():
#     # TODO кнопка пропуск хода
#     # TODO логика пркатикчески идентична предыдущему эндпоинту
#     # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
#     pass
#
#
# @app.route("/fight/end-fight")
# def end_fight():
#     # TODO кнопка завершить игру - переход в главное меню
#     return render_template("index.html", heroes=heroes)
#

if __name__ == "__main__":
    app.run(debug=True)
