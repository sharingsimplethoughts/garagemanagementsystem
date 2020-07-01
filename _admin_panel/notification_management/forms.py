from django import forms

from _user_panel.uaccounts.models import *

class UnknownForm(forms.Form):
    select = forms.ModelMultipleChoiceField(
        queryset = RegisteredUser.objects.filter(user__is_active=True), # not optional, use .all() if unsure
        widget  = forms.CheckboxSelectMultiple,
    )
