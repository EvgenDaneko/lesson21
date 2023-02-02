from .models import Projects, Review
from django.forms import ModelForm
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'slug', 'tags',
                  'description', 'demo_link', 'source_link']
        labels = {
            'title': 'Название проекта',
            'slug': 'Слаг',
            'image': 'Скриншот проекта',
            'tags': 'Теги',
            'description': 'Описание',
            'demo_link':'демо-версия',
            'source_link': 'исходная версия'
        }

        widgets = {'tags': forms.CheckboxSelectMultiple(),}

        def __init__(self, *args, **kwargs):
            super(ProjectForm, self).__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.update({'class':'input'})



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'review_text']
        labels = {
            'value': 'Оцените проект',
            'review_text': 'Добавьте комментарий'
        }

        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

