from django import forms

from quiz_app.widgets import CustomSwitchCheckBox
from quiz_app.models import Answer, Question, Quiz


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
        model = Question
        fields = ('question_text', 'question_type', 'is_active')

        labels = {
            'question_text': 'Вопрос',
            'question_type': 'Тип вопроса',
            'is_active': 'Активный?'
        }

        widgets = {
            'is_active': CustomSwitchCheckBox(attrs={'class': 'mleft'})
        }


class AddAnswerForm(forms.ModelForm):

    answer_text = forms.CharField(label='Вариант ответа: ', max_length=120)

    class Meta:
        model = Answer
        fields = ('answer_text', 'is_correct')

        labels = {
            'is_correct': 'Верный?'
        }

        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-field'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-field-checkbox scale'})
        }

    # def clean_answer_text(self):
    #     answer_text = self.cleaned_data['answer_text']
    #     if len(answer_text) > 120:
    #         raise forms.ValidationError('Длинна превышает 120 символов')
    #     return answer_text