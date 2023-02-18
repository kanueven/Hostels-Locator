from datetime import datetime
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hostels_locator.settings')

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
def get_user():
    # Now create user
    user = User.objects.create_user(
        username=fakegen.user_name(),
        email=fakegen.email(),
        password=fakegen.password()
    )
    user.save()
    return user


def populate(N=5):
    '''
    Create N Hostels and populate the system 
    '''

    for entry in range(N):
        location_name = get_location()
        # Now create location object
        loc_obj = models.Location.objects.get_or_create(name=location_name)[0]

        # Now create Hostel
        hostel_name = fakegen.company()
        hostel_address = fakegen.address()
        hostel_location = loc_obj
        hostel_owner = get_user()

        hostel = models.Hostel.objects.get_or_create(
            name=hostel_name,
            address=hostel_address,
            location=hostel_location,
            owner=hostel_owner
        )[0]

        print(f'{(entry+1)/N*100}% complete')
        
            

def get_hostels():
    try:
        hostels = int(input("Number of Hostels : "))
    except:
        print("Can't take empty values")
        return get_hostels()
    else:
        return hostels
        
if __name__ == '__main__':
    hostels = get_hostels()
    print("Adding Hostels...Please Wait")
    populate(hostels)
    print('Populating Complete')
