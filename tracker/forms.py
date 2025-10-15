from django import forms
from django.forms import ModelForm
from .models import Skill, ProgressEntry, Goal, LearningResource

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'difficulty', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe this skill...'})
        }

class ProgressEntryForm(ModelForm):
    class Meta:
        model = ProgressEntry
        fields = ['skill', 'date', 'hours_spent', 'description']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours_spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What did you practice today?'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # show all available skills
            self.fields['skill'].queryset = Skill.objects.all()

class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ['skill', 'title', 'description', 'deadline']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your goal'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your goal...'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # limit skills to available ones
            self.fields['skill'].queryset = Skill.objects.all()

class LearningResourceForm(ModelForm):
    class Meta:
        model = LearningResource
        fields = ['skill', 'title', 'url', 'resource_type', 'notes']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource title'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your notes about this resource...'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['skill'].queryset = Skill.objects.all()
