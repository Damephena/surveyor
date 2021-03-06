# Generated by Django 3.0 on 2020-11-01 21:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20201101_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='services.Question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Response')),
            ],
        ),
        migrations.RemoveField(
            model_name='answerinteger',
            name='answerbase_ptr',
        ),
        migrations.RemoveField(
            model_name='answerradio',
            name='answerbase_ptr',
        ),
        migrations.RemoveField(
            model_name='answerselect',
            name='answerbase_ptr',
        ),
        migrations.RemoveField(
            model_name='answerselectmultiple',
            name='answerbase_ptr',
        ),
        migrations.RemoveField(
            model_name='answertext',
            name='answerbase_ptr',
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 1, 22, 15, 43, 860985), help_text='survey starts accepting submissions on'),
        ),
        migrations.DeleteModel(
            name='AnswerBase',
        ),
        migrations.DeleteModel(
            name='AnswerInteger',
        ),
        migrations.DeleteModel(
            name='AnswerRadio',
        ),
        migrations.DeleteModel(
            name='AnswerSelect',
        ),
        migrations.DeleteModel(
            name='AnswerSelectMultiple',
        ),
        migrations.DeleteModel(
            name='AnswerText',
        ),
    ]
