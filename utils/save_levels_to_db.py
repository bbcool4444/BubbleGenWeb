import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LevelGeneratorWEB.settings")
django.setup()

from polls.models import Competitor, Level
from pathlib import Path
from django.core.files import File
from django.db.utils import IntegrityError


def get_level_number_from_file_name(level_name):
    return int(os.path.split(level_name)[1].split('.')[0].split('_')[1])


competitor = Competitor.objects.get(name='BS')
print('{} levels *before* insertion'.format(competitor.level_set.count()))

fp = 'E:/Python_Project/LevelGenerator/Frames/BitMango'
for fn in os.listdir(fp):
    if fn.endswith('jpg'):
        path = Path(fp + '/' + fn)
        level = Level(
            game=competitor,
            number=get_level_number_from_file_name(fn),
        )
        try:
            level.save()
            # Only create png file when the db insertion succeed.
            f = path.open(mode='rb')
            level.long_graph = File(f, name=path.name)
            level.save()
            print('Succeed: {}'.format(fn))
        except IntegrityError:
            print('Failed: {}'.format(path))


print('{} levels *after* insertion'.format(competitor.level_set.count()))
