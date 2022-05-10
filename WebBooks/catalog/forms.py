from django import forms
from django.forms import ModelForm
from .models import Book
from datetime import date

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label='Имя автора')
    last_name = forms.CharField(label='Фамилия автора')
    date_of_birth = forms.DateField(label='Дата рождения', initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type':'date'}))
    date_of_death = forms.DateField(label='Дата рождения', initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type':'date'}))

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
        labels = {'summary': ('Аннотация')}
        help_texts = {'summary': ('Не более 1000 символов')}