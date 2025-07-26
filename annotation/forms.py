from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['selected_text', 'note_text']
        widgets = {
            'selected_text': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'note_text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
