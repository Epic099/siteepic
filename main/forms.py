from django import forms
from .models import ChessRoom


class ChessRoomForm(forms.Form):
    name = forms.CharField(max_length=50)