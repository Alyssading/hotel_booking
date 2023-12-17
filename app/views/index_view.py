import datetime
import urllib

from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import Hotel, Order



# Viewing function
def index(request):
    if request.method == 'GET':
        checkin = datetime.datetime.today()
        print(checkin)
        checkout = checkin + datetime.timedelta(days=1)
        date_range = f'{checkin.strftime("%Y/%m/%d")} - {checkout.strftime("%Y/%m/%d")}'
        # The view function returned a template through the render method:index.html
        return render(request, 'index.html', {'default_date_range': date_range})

def hotel_list(request):
    params = request.GET.dict()
    hotel_name = params.get('hotel_name')
    price_per_night = params.get('price_per_night')
    filter_star = params.get('filter_star')
    checkin, checkout = params.get('daterange').split(' - ')
    adults = int(params.get('adults'))
    children = int(params.get('children'))
    room_count = int(params.get('room_count'))
    page = int(params.get('page', 1))
    hotels = Hotel.objects.select_related("city").prefetch_related('hotel_rooms').filter(
        Q(name__contains=hotel_name) | Q(address__contains=hotel_name) | Q(city__name__contains=hotel_name)
    )
    hotels_res = []
    if filter_star:
        hotels = hotels.filter(star=filter_star)

    for hotel in hotels:
        hotel_min_price_room = None
        rooms = hotel.hotel_rooms.all()
        if price_per_night:
            min_price, max_price = price_per_night.split('-')
            if min_price:
                rooms = rooms.filter(base_price__gte=int(min_price))
            if max_price:
                rooms = rooms.filter(base_price__lt=int(max_price))

        for room in rooms:
            orders = Order.objects.filter(
                checkin=checkin,
                checkout=checkout,
                room=room
            )
            inventory = room.inventory - sum([order.room_count for order in orders])
            if inventory > 0:
                if not hotel_min_price_room:
                    hotel_min_price_room = room
                else:
                    if room.base_price < hotel_min_price_room.base_price:
                        hotel_min_price_room = room
        hotel.min_price_room = hotel_min_price_room
        if hotel_min_price_room:
            hotels_res.append(hotel)

    if len(hotels_res) == 1:  # If only one hotel is found, redirect to the hotel details page
        params['hotel_id'] = hotels_res[0].id
        return redirect(reverse('hotel_search_detail') + '?' + urllib.parse.urlencode(params))
    else:  # If there are multiple, redirect to the hotel list page
        return render(request, 'hotel_page/hotel_search_list.html', {'hotels': hotels_res,
                                                                     'hotel_name': hotel_name,
                                                                     'adults': adults,
                                                                     'children': children,
                                                                     'checkin': checkin,
                                                                     'checkout': checkout,
                                                                     'room_count': room_count,
                                                                     'page': page,
                                                                     'price_per_night': price_per_night,
                                                                     'filter_star': filter_star,
                                                                     })

def hotel_search_detail(request):
    pass