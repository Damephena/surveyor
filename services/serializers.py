from rest_framework import serializers

from services import models


class SurveySerializer(serializers.ModelSerializer):

    '''
    Survey serializer contains associated
    questions and categories linked to a Survey object.
    '''
    survey_questions = serializers.SerializerMethodField()
    survey_categories = serializers.SerializerMethodField()

    class Meta:
        model = models.Survey
        fields = '__all__'
    
    def get_survey_questions(self, obj):
        return obj.get_questions().values()
    
    def get_survey_categories(self, obj):
        return obj.get_categories().values()


class CategorySerializer(serializers.ModelSerializer):

    '''Category serializer'''
    class Meta:
        model = models.Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    '''Question serializer'''
    # choices = serializers.CharField(source='get_choices')

    class Meta:
        model = models.Question
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    
    '''Response serializer'''
    class Meta:
        model = models.Response
        fields = '__all__'


class AnswerBaseSerializer(serializers.ModelSerializer):

    '''AnswerBase serializer'''
    class Meta:
        model = models.AnswerBase
        fields = '__all__'
