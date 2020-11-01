from rest_framework import serializers

from services import models


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Survey
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Response
        fields = '__all__'


class AnswerBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnswerBase
        fields = '__all__'

