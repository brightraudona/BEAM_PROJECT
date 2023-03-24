from datetime import timedelta
from django.shortcuts import render
from App.models import Activity, Challenge
from folium import folium
import requests

# Create your views here.
def home(request):
    # Make your map object
    main_map = folium.Map(location=[54.6872, 25.2797], zoom_start = 12) # Create base map
    main_map_html = main_map._repr_html_() # Get HTML for website

    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        user = request.user # Pulls in the Strava User data
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
        if old_count_activities < len(activity_df_list):
            for challenge in challenges:
                if user in challenge.participants.all():
                    print(Activity.objects.count())
                    existing_activities = challenge.activities.filter(athlete=user, sport_type=challenge.sport_type)
                    new_activities = Activity.objects.filter(athlete=user, sport_type=challenge.sport_type).exclude(id__in=existing_activities)
                    print(existing_activities.count())
                    print(new_activities.count())
                    challenge.activities.add(*new_activities)
                    challenge.save()

        data = {
            "user":request.user,
            "main_map":main_map_html,
            "challenges":challenges,
            "ID":request.user.id
        }
        return render(request, 'home.html', data)
    

def challenge(request, challengeId):
    challenge = Challenge.objects.get(id=challengeId)
    activities = challenge.activities.all()
    data = {
        "activities":activities,
        "challenge":challenge
    }
    return render(request, 'challenge.html', data)

def join_challenge(request):
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        challenge = Challenge.objects.get(id=challenge_id)

        # Filter activities by sport_type
        sport_type = challenge.sport_type
        activities = Activity.objects.filter(athlete=request.user, sport_type=sport_type)
        
        # Add filtered activities to the challenge
        challenge.activities.add(*activities)
        challenge.participants.add(request.user)
        challenge.save()

        return home(request)

def leave_challenge(request):
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        challenge = Challenge.objects.get(id=challenge_id)

        # Filter activities by sport_type
        sport_type = challenge.sport_type
        activities = Activity.objects.filter(athlete=request.user, sport_type=sport_type)
        
        # Add filtered activities to the challenge
        challenge.activities.remove(*activities)
        challenge.participants.remove(request.user)
        challenge.save()

        return home(request)