from django import forms

from .models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "league", "is_top_team"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Название команды"}),
        }

