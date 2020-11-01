from django.urls import path
from rest_framework.routers import SimpleRouter
from services import views

router = SimpleRouter()
router.register('categories', views.CategoryViewset, basename='category')
router.register('surveys', views.SurveyViewset, basename='survey')
router.register('questions', views.QuestionViewset, basename='question')
router.register('responses', views.ResponseViewset, basename='response')

urlpatterns = router.urls
