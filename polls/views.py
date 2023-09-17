from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.contrib.auth.decorators import login_required
from .models import Vote
from .models import Choice, Question


class IndexView(generic.ListView):
    """
    Redirect to index.html
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    Redirect to detail.html
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    Redirect to results.html
    """
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """
    A function for voting and checking if the user voted or not
    """
    question = get_object_or_404(Question, pk=question_id)
    this_user = request.user

    if not question.can_vote():
        messages.error(request, f"Poll number {question.id}"
                                f"id not available to vote")
        return redirect("polls:index")

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    else:
        try:
            # find a vote for this user and this question
            vote = Vote.objects.get(user=this_user, choice__question=question)
            # update his vote
            vote.choice = selected_choice
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=this_user, choice=selected_choice).save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

        #     # no matching votes - create a new vote
        #     vote = Vote(user=this_user, choice=selected_choice)
        #     vote.save()
        #     vote = Vote.objects.create(user=this_user, choice=selected_choice)
        #
        # try:
        #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # except (KeyError, Choice.DoesNotExist):
        #     # Redisplay the question voting form.
        #     return render(request, 'polls/detail.html', {
        #         'question': question,
        #         'error_message': "You didn't select a choice.",
        #     })
        # else:
        #     selected_choice.votes += 1
        #     selected_choice.save()
        #     # Always return an HttpResponseRedirect after successfully dealing
        #     # with POST data. This prevents data from being posted twice if a
        #     # user hits the Back button.
        #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def poll_detail(request, poll_id):
#     """
#     get requests for detail page
#     """
#     poll = get_object_or_404(Question
#                              , pk=poll_id)
#     if not poll.can_vote():
#         messages.error(request, "Voting for this poll is not allowed.")
#         return HttpResponseRedirect(reverse('polls:index'))
#     return render(request, 'polls/detail.html', {'question': poll})
