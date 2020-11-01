import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

def validate_list(args):

    """Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = args.split(',')

    if len(values) < 2:
        raise ValidationError(
        'A list of choices separated by "," is expected. Choices must contain more than one item.'
    )

class Survey(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    cover_image = models.FileField(upload_to='survey/covers/%Y%m/%d/', blank=True, null=True)
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
    
    def get_question(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        return None


class Category(models.Model):
    name = models.CharField(max_length=120)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))


class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'text'),
        ('radio', 'radio'),
        ('select', 'select'),
        ('select-multiple', 'select multiple'),
        ('integer', 'integer'),
    )

    text = models.TextField()
    required = models.BooleanField(default=False, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20)
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

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''

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


class AnswerBase(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    response = models.ForeignKey('Response', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
	body = models.IntegerField(blank=True, null=True)
