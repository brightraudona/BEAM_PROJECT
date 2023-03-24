from django import forms
from django.contrib import admin
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        exclude = ('activities',)

class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeForm
    list_display = ('name', 'sport_type', 'start_date', 'end_date')

admin.site.register(Challenge, ChallengeAdmin)
