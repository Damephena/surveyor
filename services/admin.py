from django.contrib import admin

from services import models

admin.site.register(
    (
        models.AnswerBase,
        models.AnswerInteger,
        models.AnswerRadio,
        models.AnswerSelect,
        models.AnswerSelectMultiple,
        models.AnswerText,
        models.Category,
        models.Question,
        models.Response,
        models.Survey,
    ),
)
