from django import forms
from django.contrib import admin
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        exclude = ('activities',)

class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeForm

admin.site.register(Challenge, ChallengeAdmin)
