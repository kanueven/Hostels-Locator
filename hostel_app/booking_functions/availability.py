from hostel_app.models import Room,Booking
import datetime

def check_availability(room,start_date,end_date):
    #is the new checkin after the checkout or the checkout is before pre existing booking
    avail_list=[]
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.start_date > end_date or booking.end_date < start_date:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)