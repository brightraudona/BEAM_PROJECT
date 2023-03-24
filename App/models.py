from django.db import models
from django.contrib.auth.models import User

from App.enums import SportType

class Activity(models.Model):
    name = models.CharField(max_length=255)
    activity_id = models.IntegerField(unique=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    sport_type = models.CharField(max_length=255)
    distance = models.FloatField()
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    sport_type = models.CharField(max_length=255, choices=[(sport.value, sport.name) for sport in SportType])
    activities = models.ManyToManyField(Activity, related_name='challenges', blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='challenges', blank=True, null=True)

    def get_total_distance(self):
        return sum([activity.distance for activity in self.activities.all()])
    
    def get_total_duration(self):
        return sum([activity.duration for activity in self.activities.all()])