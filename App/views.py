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
        activity_df_list = []
        for n in range(5):  # Change this to be higher if you have more than 1000 activities
            param = {'per_page': 5, 'page': n + 1}

            activities_json = requests.get(activites_url, headers=header, params=param).json()
            if not activities_json:
                break
            activity_df_list.append(activities_json)
            Activity.objects.update_or_create(name = activities_json[0]['name'],
                            activity_id = activities_json[0]['id'],
                            athlete = user,
                            start_date = activities_json[0]['start_date'],
                            distance = activities_json[0]['distance'],
                            sport_type = activities_json[0]['sport_type'],
                            duration = timedelta(seconds=activities_json[0]['elapsed_time']))

        challenge = Challenge.objects.all()
        
        data = {
            "user":request.user,
            "main_map":main_map_html,
            "challenges":challenge,
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
        challenge.participants.add(request.user)

        # Filter activities by sport_type
        sport_type = challenge.sport_type
        activities = Activity.objects.filter(athlete=request.user, sport_type=sport_type)
        
        # Add filtered activities to the challenge
        challenge.activities.add(*activities)
        challenge.participants.add(request.user)
        challenge.save()

        return home(request)