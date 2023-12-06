from django.forms import ModelForm, CharField, TextInput, Textarea

from .models import Tag, Note


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter the tag name'}))

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter note name'}))
    description = CharField(min_length=10, max_length=150, required=True, widget=Textarea(
        attrs={'class': "form-control", 'rows': '4', 'placeholder': 'Enter description'}))

    class Meta:
        model = Note
        fields = ['name', 'description']
        exclude = ['tags']
