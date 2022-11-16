import os
import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def get_new_name(game_name, original_name):
    """

    :param original_name: Level_0086.jpg
    :param game_name: BitMango
    :return: BitMango_86.png
    """
    img_name, suffix = original_name.split('.')
    number = int(img_name.split('_')[1])
    result = '{}_{}.{}'.format(game_name, number, suffix)

    return result


@click.command('insert-images')
def insert_long_graph():
    """
    Insert the images in static folder into db.
    :return:
    """
    db = get_db()

    for img in os.listdir(current_app.config['UPLOAD_FOLDER']):
        if img.endswith('jpg'):
            img_name, suffix = img.split('.')
            game_name, level_number = img_name.split('_')

            long_graph_name = '{}/{}'.format(current_app.config['UPLOAD_FOLDER'], img)

            game = db.execute(
                'SELECT * FROM game WHERE name = ?', (game_name,)
            ).fetchone()

            try:
                db.execute("INSERT INTO level (number, game_id, long_graph) VALUES (?, ?, ?)",
                           (level_number, game['id'], long_graph_name),
                           )
                print('level {} in game {} insert successfully.'.format(level_number, game['name']))
            except sqlite3.IntegrityError:
                print('level {} in game {} already exists.'.format(level_number, game['name']))

    db.commit()

    click.echo('insert long graph.')


def init_app(app):
    app.cli.add_command(insert_long_graph)


if __name__ == '__main__':
    # Rename the files already in folders to db image format.
    fp = 'static/images'
    for fn in os.listdir(fp):
        old_name = '{}/{}'.format(fp, fn)
        new_name = '{}/{}'.format(fp, get_new_name('BitMango', fn))
        os.rename(old_name, new_name)
