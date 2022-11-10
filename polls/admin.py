from django.contrib import admin
from .models import Question, Competitor, Level


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Competitor)
admin.site.register(Level)
