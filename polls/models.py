import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Competitor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Level(models.Model):
    number = models.IntegerField()
    game = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    long_graph = models.ImageField(upload_to='long_graphs')

    class Meta:
        unique_together = ['number', 'game']

    def __str__(self):
        return '{}({})'.format(self.game, self.number)
