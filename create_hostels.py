from datetime import datetime
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hostel_locator.settings')

import django
django.setup()
import random
from django.contrib.auth.models import User
from hostel_app import models
from faker import Faker
import random

fakegen = Faker()

cities = ['Kisumu', ' Nairobi', 'Nakuru', 'Mombasa', 'Malindi', 'Kakamega','Busia','Bungoma']

def get_location():
    return random.choice(cities)

def populate(N=5):
    '''
    Create N Entries of Dates Accessed
    '''

    for entry in range(N):
        location_name = get_location()
        # Now create location object
        loc_obj = Location.objects.get_or_create(name=location_name)[0]

        # then create 3 venues per location
        for i in range(1):
            venue_name = fakegen.company()
            ven_obj = Venue.objects.get_or_create(
                name=venue_name, location=loc_obj)[0]
            print(f"created {venue_name}")
            

def get_party():
    try:
        parties = int(input("Number of Parties : "))
    except:
        print("Can't take empty values")
        return get_party()
    else:
        return parties
        
if __name__ == '__main__':
    venues = int(input("How many venues do you want : "))
    print("Adding Venues...Please Wait")
    populate(venues)
    print('Populating Complete')
