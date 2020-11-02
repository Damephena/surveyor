from django.contrib import admin

from services import models

admin.site.register(
    (
        models.Answer,
        models.Category,
        models.Question,
        models.Response,
        models.Survey,
    ),
)
