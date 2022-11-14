from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Level, Competitor
from .forms import NameForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class LevelsView(generic.ListView):
    template_name = 'polls/levels_index.html'

    def get_queryset(self):
        return Level.objects.filter(game__name='BS')


class LevelDetailView(generic.DetailView):
    model = Level
    template_name = 'polls/level_detail.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def level_detail(request):
    if request.method == 'GET':
        level_num = request.GET.get('level_num')
        level_list = Level.objects.filter(number=level_num)
        comp_bs = Competitor.objects.get(name='BS')

        return render(request, 'polls/level_detail.html', {
            'level_list': level_list,
            'total_level_iter': range(comp_bs.level_set.count()),
        })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def bootstrap_test(request):
    form = NameForm()
    return render(request, 'polls/bootstrap_test.html', {
        'form': form,
    })
