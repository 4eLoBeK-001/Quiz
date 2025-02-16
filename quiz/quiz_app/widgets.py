from django.forms import CheckboxInput

class CustomSwitchCheckBox(CheckboxInput):
    template_name = 'quiz_app/custom_checkbox.html'