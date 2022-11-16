import os
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

UPLOAD_FOLDER = 'static/images'


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE'] = os.path.join(app.instance_path, 'level_info.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///level_info.sqlite"
db.init_app(app)

import utils
utils.init_app(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=True)


class Level(db.Model):
    __table_args__ = (
        db.UniqueConstraint('number', 'game_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship("Game", backref=db.backref("game", uselist=False))
    long_graph = db.Column(db.String(80), nullable=True)
    e_count = db.Column(db.Integer)
    e_dict = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('level_detail', level_num=1))


@app.route('/level')
def level_detail():
    level_num = request.args.get('level_num')
    level_list = Level.query.filter_by(number=level_num).all()
    level_count = Level.query.filter_by(game_id=1).count()

    return render_template(
        'index.html', level_list=level_list, level_sequence=range(1, 101),
        level_count=level_count,
    )

