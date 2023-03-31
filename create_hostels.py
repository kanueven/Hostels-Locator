from faker import Faker
import random
import django
from datetime import datetime
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostels_locator.settings')

django.setup()

from hostel_app import models
from django.contrib.auth.models import User
fakegen = Faker()

cities = ['Kisumu', ' Nairobi', 'Nakuru', 'Mombasa',
          'Malindi', 'Kakamega', 'Busia', 'Kajiado']
services = ['Transport', 'Food', 'wifi', 'hot-shower']
categories = ['Shared', 'Double', 'Single']


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


def get_services():
    num = random_number = random.randint(1, 3)
    services_list = []
    for i in range(num):
        service_obj,created = models.Service.objects.get_or_create(
            name=services[i])
        if created:
            service_obj.description = fakegen.text()
            
        services_list.append(service_obj)
    return services_list


def get_categories(hostel: models.Hostel):
    num = random_number = random.randint(1, 2)
    for i in range(num):
        cat_obj = models.RoomCategory.objects.get_or_create(name=categories[i], description=fakegen.text(
        ), quantity=random.randint(10, 20), price=random.randint(5000, 10000), hostel=hostel)[0]


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

        services_list = get_services()
        for sv in services_list:
            hostel.services.add(sv)

        get_categories(hostel=hostel)

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
