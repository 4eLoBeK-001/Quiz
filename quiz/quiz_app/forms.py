from django import forms

from quiz_app.models import Quiz


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