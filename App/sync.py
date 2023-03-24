from datetime import timedelta
import time
import requests
from App.models import Activity, Challenge


def sync(user, first):
    strava_login = user.social_auth.get(provider='strava') # Strava login
    access_token = strava_login.extra_data['access_token'] # Strava Access token
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}
    old_count_activities = Activity.objects.count()
    activity_df_list = []
    for n in range(5):  # Change this to be higher if you have more than 1000 activities
        param = {'per_page': 10, 'page': n + 1}
        activities_json = requests.get(activites_url, headers=header, params=param).json()

        if not activities_json:
            break
        for activity in activities_json:
            activity_df_list.append(activity)
            Activity.objects.update_or_create(name=activity['name'],
                                            activity_id=activity['id'],
                                            athlete=user,
                                            start_date=activity['start_date'],
                                            distance=activity['distance'],
                                            sport_type=activity['sport_type'],
                                            duration=timedelta(seconds=activity['elapsed_time']))

    challenges = Challenge.objects.all()

    # sync activites
    #if old_count_activities < len(activity_df_list):
    for challenge in challenges:
        if user in challenge.participants.all():
            print(Activity.objects.count())
            existing_activities = challenge.activities.filter(athlete=user, sport_type=challenge.sport_type)
            new_activities = Activity.objects.filter(athlete=user, sport_type=challenge.sport_type, start_date__gte=challenge.start_date).exclude(id__in=existing_activities)
            print(existing_activities.count())
            print(new_activities.count())
            challenge.activities.add(*new_activities)
            challenge.save()

    return {
        "user":user,
        "challenges":challenges,
        "ID":user.id
    }

