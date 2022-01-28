from django.shortcuts import (
    render, # helps render html templates
    get_object_or_404, # returns the desired object if it exists or raises a 404 error
    reverse, # lookup the path associated with a view name
)
from django.http import HttpResponse, HttpResponseRedirect ,Http404


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    QuestionDetailSerializer,
    ChoiceSerializer
)

# import the models from the Polls app
from .models import Question, Choice

from users.models import CustomUser

def index(request):
    return render(request, 'polls/index.html')


@api_view(['GET'])
def polls_list(request):
    # create blank JSON response
    response = Response()

    questions = Question.objects.all().order_by('-pub_date')

    # many=True allows multiple instances to be serialized
    question_serializer = QuestionDetailSerializer(questions, many=True)

    response.data = {
        'questions': question_serializer.data
    }

    return response
    
@api_view(['POST'])
def vote(request):
    response = Response()

    # the fetch request's body data is in request.data
    choice_id = request.data.get('choiceId')

    choice = get_object_or_404(Choice, id=choice_id)

    # increase the choice's vote count
    choice.votes += 1

    # save the updates
    choice.save()

    questions = Question.objects.all().order_by('-pub_date')

    # many=True allows multiple instances to be serialized
    question_serializer = QuestionDetailSerializer(questions, many=True)

    response.data = {
        'questions': question_serializer.data
    }

    return response


def create_question(request):

    print('user requesting to create a question:', request.user)

    # the form data is available through the request object
    form = request.POST

    # grab the values from the form
    question_text = form['question_text']
    number_of_choices = int(form['number_of_choices'])

    # create the new question in the database
    new_question = Question()
    # set the question text
    new_question.question_text = question_text

    # assign a user to the question
    new_question.user = request.user

    # save the object to the database
    new_question.save()

    # generate a list of choice numbers
    choice_numbers = [number for number in range(1, number_of_choices + 1)]

    # gather data to render into the template
    context = {
        'choice_numbers': choice_numbers,
        'question': new_question
    }

    # render the add_choices.html template using the context data
    return render(request, 'polls/add_choices.html', context)



def add_choices(request):
    form = request.POST

    # find the question object that has the question_id from the form
    question = get_object_or_404(Question, id=form['question_id'])

    for key in form:
        if key.startswith('choice'):
            # create a new Choice database object
            new_choice = Choice()

            # set the choice_text
            # form['choice1'], form['choice2'], etc
            new_choice.choice_text = form[key]

            # associate the choice to the question
            new_choice.question = question

            # save the changes to the database
            new_choice.save()

    # redirect to the home page to view all the polls
    return HttpResponseRedirect(reverse('polls:home'))


def user_polls_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    questions = Question.objects.filter(user=user)
    
    context = {
        'questions': questions
    }

    return render(request, 'polls/polls-list.html', context)