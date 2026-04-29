from django import forms
from .models import Choice, Elective


class ChoiceForm(forms.Form):
    """
    Form for submitting 3 ranked elective choices.
    Validates that all 3 choices are distinct.
    """
    choice_1 = forms.ModelChoiceField(
        queryset=Elective.objects.all(),
        label="1st Choice",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    choice_2 = forms.ModelChoiceField(
        queryset=Elective.objects.all(),
        label="2nd Choice",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    choice_3 = forms.ModelChoiceField(
        queryset=Elective.objects.all(),
        label="3rd Choice",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned = super().clean()
        c1 = cleaned.get('choice_1')
        c2 = cleaned.get('choice_2')
        c3 = cleaned.get('choice_3')

        choices = [c for c in [c1, c2, c3] if c]
        if len(choices) != len(set(c.id for c in choices)):
            raise forms.ValidationError("All three choices must be different electives.")
        return cleaned
