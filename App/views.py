import datetime
import threading
import time
from App.sync import sync
from django.shortcuts import render
from App.models import Activity, Challenge
from folium import folium

# Create your views here.


def home(request):
    # Make your map object
    main_map = folium.Map(
        location=[54.6872, 25.2797], zoom_start=12)  # Create base map
    main_map_html = main_map._repr_html_()  # Get HTML for website

    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        data = sync(request.user, True)
        data["main_map"] = main_map_html

        def thread_callback(result):
            # Render the template with the result
            result["main_map"] = main_map_html
            print("task done")
            return render(request, 'index.html', result)
        
        # Start the long-running task in a separate thread
        thread = threading.Thread(target=sync(request.user, False))
        thread.daemon = True
        request.thread_callback = thread_callback
        thread.start()

        return render(request, 'home.html', data)


def challenge(request, challengeId):
    _ = sync(request.user, True)
    challenge = Challenge.objects.get(id=challengeId)
    activities = challenge.activities.all()


    if challenge.type == 'Time':
        activities = activities.order_by('-duration')
    elif challenge.type == 'Distance':
        activities = activities.order_by('-distance')

    user_totals = []
    if challenge.type == 'Time':
        for p in challenge.participants.all():
            if not p.first_name == '':
                user_totals.append({
                    'name':p.first_name,
                    'total':sum([activity.duration.total_seconds() for activity in challenge.activities.filter(athlete=p, start_date__gte=challenge.start_date)])
                })
    elif challenge.type == 'Distance':
        for p in challenge.participants.all():
            if not p.first_name == '':
                user_totals.append({
                    'name':p.first_name,
                    'total':sum([activity.distance for activity in challenge.activities.filter(athlete=p, start_date__gte=challenge.start_date)])
                })


    data = {
        "activities":activities,
        "challenge":challenge,
        "totals":user_totals
    }
    return render(request, 'challenge.html', data)


def join_challenge(request):
    _ = sync(request.user, True)
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        challenge = Challenge.objects.get(id=challenge_id)

        # Filter activities by sport_type
        sport_type = challenge.sport_type
        activities = Activity.objects.filter(athlete=request.user, sport_type=sport_type, start_date__lt=challenge.start_date)
        
        # Add filtered activities to the challenge
        challenge.activities.add(*activities)
        challenge.participants.add(request.user)
        challenge.save()

        return home(request)


def leave_challenge(request):
    _ = sync(request.user, True)
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        challenge = Challenge.objects.get(id=challenge_id)

        # Filter activities by sport_type
        sport_type = challenge.sport_type
        activities = Activity.objects.filter(
            athlete=request.user, sport_type=sport_type)

        # Add filtered activities to the challenge
        challenge.activities.remove(*activities)
        challenge.participants.remove(request.user)
        challenge.save()

        return home(request)


def user_profile(request):
    user_challenges = []
    for challenge in Challenge.objects.all():
        if request.user in challenge.participants.all():
            user_challenges.append(challenge)
    user_activities = Activity.objects.all()
    data = {
        "activities": user_activities,
        "challenges": user_challenges
    }
    return render(request, 'user_profile.html', data)
