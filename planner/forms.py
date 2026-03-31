from django import forms
from django.contrib.auth.models import User
from .models import Subject, Task, Profile

# ----- Registration Form -----

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'deadline', 'estimated_time', 'reminder_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description...'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        self.fields['subject'].empty_label = 'Select a subject'
