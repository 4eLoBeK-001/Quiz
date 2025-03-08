from django import forms

from quiz_app.widgets import CustomSwitchCheckBox
from quiz_app.models import Answer, Question, Quiz


class CreateQuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ('name', 'description', 'difficult', 'is_show')

        labels = {
            'name': 'Название',
            'description': 'Описание',
            'difficult': 'Сложность',
            'is_show': 'Сделать общедоступным?'
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'is_show': forms.CheckboxInput(attrs={'class': 'scale15'})
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
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-field-checkbox scale23'})
        }

    # def clean_answer_text(self):
    #     answer_text = self.cleaned_data['answer_text']
    #     if len(answer_text) > 120:
    #         raise forms.ValidationError('Длинна превышает 120 символов')
    #     return answer_text


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        label='Имя:', 
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    email = forms.EmailField(
        label='Email:', 
        widget=forms.EmailInput(attrs={'class': 'input'})
    )

    message = forms.CharField(
        label='Сообщение:',
        widget=forms.Textarea(attrs={'class': 'input textarea', 'rows': '4'})
    )