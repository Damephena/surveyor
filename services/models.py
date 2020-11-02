import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from utils.validate_list import validate_list
from rest_framework.exceptions import ValidationError


class Survey(models.Model):

    '''Survey model.'''
    name = models.CharField(max_length=300)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='survey/covers/%Y%m/%d/', blank=True, null=True)
    start_at   = models.DateTimeField(
        default=datetime.datetime.now(),
        help_text='survey starts accepting submissions on',
        blank=True
    )
    closes_at  = models.DateTimeField(
        help_text='survey stops accepting submissions on',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))

    def get_questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        return None
    
    def get_categories(self):
        if self.pk:
            return Category.objects.filter(survey=self.pk)
        return None
    
    def get_responses(self):
        if self.pk:
            return Response.objects.filter(survey=self.pk)
        return None


class Category(models.Model):

    '''Category model'''
    name = models.CharField(max_length=120)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))


class Question(models.Model):

    '''Question model'''
    QUESTION_TYPES = (
        ('text', 'text'),
        ('radio', 'radio'),
        ('select', 'select'),
        ('select-multiple', 'select multiple'),
        ('integer', 'integer'),
    )

    text = models.TextField()
    required = models.BooleanField(default=False, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='text'
    )
    choices = models.TextField(
        null=True,
        blank=True,
        help_text='if question_type is "radio", "select" or "select-multiple" provide a list of \
            comma-separated options list for this question'
    )

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        options = ['radio', 'select', 'select-multiple']
        if(self.question_type in options):
            validate_list(self.choices)
        super().save(*args, **kwargs)
    
    def get_clean_choices(self):

        '''Return split and stripped list of choices with no null values.'''
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(','):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    def get_choices(self):

        '''
        parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.
        '''
        choices = self.choices.split(',')
        choices_list = [(choice.strip(), choice.strip()) for choice in choices]

        choices_tuple = tuple(choices_list)
        return choices_tuple


class Response(models.Model):
    
    '''
    Model which contains all surveys with basic information about the `user`s who responded to surveys and surveyors.
    '''
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    surveyor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    interviewee_email = models.EmailField()
    comments = models.TextField(
        'Any additional comments', 
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Response to {self.survey} created by {self.surveyor.first_name}'


class Answer(models.Model):

    '''Answer model'''
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    response = models.ForeignKey('Response', on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs["question_id"])
        except KeyError:
            question = kwargs.get("question")
        body = kwargs.get("body")
        if question and body:
            self.check_answer_body(question, body)
        super(Answer, self).__init__(*args, **kwargs)

    @property
    def values(self):
        if self.body is None:
            return [None]
        
        if len(self.body) < 3 or self.body[0:3] != "[u'":
            return [self.body]

        values = []
        raw_values = self.body.split("', u'")
        nb_values = len(raw_values)
        for i, value in enumerate(raw_values):
            if i == 0:
                value = value[3:]
            if i + 1 == nb_values:
                value = value[:-2]
            values.append(value)
        return values

    def check_answer_body(self, question, body):

        '''Method to check provided answer to question is listed in possible options'''
        if question.type in ['radio', 'select', 'select-multiple']:
            choices = question.get_clean_choices()
            if body:
                if body[0] == "[":
                    answers = []
                    for i, part in enumerate(body.split("'")):
                        if i % 2 == 1:
                            answers.append(part)
                else:
                    answers = [body]
            for answer in answers:
                if answer not in choices:
                    msg = "Impossible answer '{}'".format(body)
                    msg += " should be in {} ".format(choices)
                    raise ValidationError(msg)

