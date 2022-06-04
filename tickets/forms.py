from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('choice', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].widget.attrs.update({'class': 'form-control', 'style':'font-size:1.5rem; direction:ltr;'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'متن توضیحات', 'style':'font-size:1.5rem;'})