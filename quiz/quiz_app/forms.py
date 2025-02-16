from django import forms

from quiz_app.widgets import CustomSwitchCheckBox
from quiz_app.models import Quiestion, Quiz


class CreateQuizForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Quiz
        fields = ('name', 'description', 'difficult', 'is_show')

        labels = {
            'name': 'Название',
            'description': 'Описание',
            'difficult': 'Сложность',
            'is_show': 'Сделать общедоступным?'
        }


class CreateQuestionForm(forms.ModelForm):

    class Meta:
        model = Quiestion
        fields = ('question_text', 'question_type', 'is_active')

        labels = {
            'question_text': 'Вопрос',
            'question_type': 'Тип вопроса',
            'is_active': 'Активный?'
        }

        widgets = {
            'is_active': CustomSwitchCheckBox(attrs={'class': 'mleft'})
        }