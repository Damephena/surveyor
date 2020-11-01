from django.shortcuts import render

from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser

from utils.permissions import IsAdminOrReadOnly
from services import models, serializers


class CategoryViewset(viewsets.ModelViewSet):

    '''
    list:
        Gets all categories on the platform
    create:
        Create a new category as an `admin`
    read:
        Retrieve a category.
    update:
        Update an existing category as an `admin`.
    partial_update:
        Make patch update to an existing category as an `admin`.
    delete:
        Delete a category as an `admin`.
    '''
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SurveyViewset(viewsets.ModelViewSet):

    '''
    list:
        Gets all surveys on the platform
    create:
        Create a new survey as an `admin`
    read:
        Retrieve a survey.
    update:
        Update an existing survey as an `admin`.
    partial_update:
        Make patch update to an existing survey as an `admin`.
    delete:
        Delete a survey as an `admin`.
    '''
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_parsers(self):
    
        '''To enable file uploads via Swagger API endpoint'''
        if getattr(self, 'swagger_fake_view', False):
            return [MultiPartParser]
        return super().get_parsers()


class QuestionViewset(viewsets.ModelViewSet):

    '''
    list:
        Gets all questions on the platform
    create:
        Create a new question as an `admin`
    read:
        Retrieve a question.
    update:
        Update an existing question as an `admin`.
    partial_update:
        Make patch update to an existing question as an `admin`.
    delete:
        Delete a question as an `admin`.
    '''
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


class ResponseViewset(viewsets.ModelViewSet):

    '''
    list:
        Gets all responses on the platform
    create:
        Create a new response as an `admin`
    read:
        Retrieve a response.
    update:
        Update an existing response as an `admin`.
    partial_update:
        Make patch update to an existing response as an `admin`.
    delete:
        Delete a response as an `admin`.
    '''
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    permission_classes = [IsAdminOrReadOnly]
