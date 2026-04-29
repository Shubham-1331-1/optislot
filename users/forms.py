from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    usn = forms.CharField(max_length=20, required=True, label="USN")
    cgpa = forms.DecimalField(
        max_digits=4, decimal_places=2,
        min_value=0.0, max_value=10.0,
        label="CGPA"
    )

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'usn', 'cgpa', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StudentLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
