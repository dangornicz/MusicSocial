from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.utils.datetime_safe import datetime


# Create your views here.
def ticketmaster_home(request):
    response_info = "none"
    if request.method == 'POST':
        genre = request.POST['genre']
        location = request.POST['location']
        print(request.POST)

        if not genre:
            messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            redirect('home')
        elif not location:
            messages.info(request, 'City cannot be empty. Please enter a city.')
            redirect('home')

        event_data = default_api_call(genre, location)

        if event_data is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            redirect('home')

        else:
            response_info = event_data['page']['totalElements']
            events = event_data['_embedded']['events']
            event_list = []
            print(events[0]['name'])
            for event in events:
                event_name = event['name']
                event_date_time = event['dates']['start']['dateTime']
                event_venue = event['_embedded']['venues'][0]['name']
                event_address = event['_embedded']['venues'][0]['address']['line1']
                event_city = event['_embedded']['venues'][0]['city']['name']
                event_state = event['_embedded']['venues'][0]['state']['name']
                event_image = event['images'][0]['url']
                event_url = event['url']

                # code from APIExamples github repo to format date
                date_object = datetime.strptime(event_date_time[:10], "%Y-%m-%d")
                event_date = date_object.strftime("%a %b %d %Y")

                dictionary_placeholder = {
                    'event_name': event_name,
                    'event_date': event_date,
                    'event_venue': event_venue,
                    'event_address': event_address,
                    'event_city': event_city,
                    'event_state': event_state,
                    'event_image': event_image,
                    'event_url': event_url,
                }
                event_list.append(dictionary_placeholder)

            context = {'events': event_list, 'response_info': response_info}
            return render(request, 'home.html', context)

    context = {'response_info': response_info}
    return render(request, 'home.html', context)


def default_api_call(genre, location):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events"
        API_KEY = "N6Wb0GS4E52znrUuz80QTgHqGo5jdiTM"
        parameters = {
            "classificationName": genre,
            "city": location,
            "sort": "date,asc",
            "apikey": API_KEY
        }
        response = requests.get(url, params=parameters)
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None
