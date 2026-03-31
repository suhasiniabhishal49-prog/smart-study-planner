from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Subject, Task, Profile
=======
from .models import Subject, Task
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d


# ----- Registration Form -----
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


# ----- Subject Form -----
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'priority', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics, Maths...'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }


# ----- Task Form -----
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
<<<<<<< HEAD
        fields = ['title', 'description', 'subject', 'deadline', 'estimated_time', 'reminder_time']
=======
        fields = ['title', 'description', 'subject', 'deadline', 'estimated_time']
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description...'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
<<<<<<< HEAD
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
=======
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d
        }

    def __init__(self, *args, **kwargs):
        # Only show subjects belonging to the logged-in user
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
<<<<<<< HEAD
        self.fields['subject'].empty_label = 'Select a subject'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
=======
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d
