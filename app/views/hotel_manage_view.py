import os.path
import time
import urllib

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import Hotel, Country, HotelBrand, HotelChain, Room, Images


def hotel_manage_list(request):
    """View hotel list in the background"""
    param = request.GET
    page = int(param.get('page', '1'))
    hotel_list = Hotel.objects.all()
    page_size = 15
    hotels = Hotel.objects.all()
    paginator = Paginator(hotels, page_size)
    page_obj = paginator.page(page)
    return render(request,
                  'hotel_page/hotel_manage_list.html',
                  {
                      'page': page_obj,
                  })


def hotel_manage_detail(request, id=None):
    """View or create/modify hotels"""
    print(id)
    if request.method == 'GET':
        param = request.GET
        hotel = None
        if id:
            hotel = Hotel.objects.get(id=id)
        countries = Country.objects.all()
        brands = HotelBrand.objects.all()
        chains = HotelChain.objects.all()
        return render(request,
                      'hotel_page/hotel_manage_detail.html',
                      {
                          'hotel': hotel,
                          'countries': countries,
                          'brands': brands,
                          'chains': chains,
                      })
    elif request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        hotel, _ = Hotel.objects.update_or_create(
            id=id,
            defaults=data
        )
        hotel.city_id = data['city_id']
        hotel.save()
        if id:
            return redirect(reverse('hotel_manage_detail'), id=hotel.id)
        else:
            return redirect(reverse('hotel_manage_list'))


def hotel_delete(request, id):
    """delete hotel"""
    Hotel.objects.filter(id=id).delete()
    return redirect('hotel_manage_list')


def hotel_image_view(request):
    param = request.GET
    hotel_id = param.get('hotel_id')
    room_id = param.get('room_id')
    hotel = None
    room = None
    if request.method == 'GET':
        image_list = []
        if hotel_id:
            hotel = Hotel.objects.get(id=hotel_id)
            image_list = hotel.hotel_images.all()
        elif room_id:
            room = Room.objects.get(id=room_id)
            image_list = room.room_images.all()
        return render(request, 'hotel_page/image_manage.html', {'image_list': image_list,
                                                                  'hotel': hotel,
                                                                  'room': room
                                                                })
    if request.method == 'POST':
        data = request.POST
        file = request.FILES.get('image_file')
        image_id = data.get('image_id')
        image, created = Images.objects.update_or_create(
            id=image_id or None,
            defaults=dict(
                desc=data['desc'],
                hotel_id=hotel_id,
                room_id=room_id
            )
        )
        if file:
            img_url = os.path.join(
                'media',
                'hotel_image',
                f'{time.time()}{file.name}'
            )
            with open(img_url, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            image.url = os.path.join('/', img_url)
            image.save()
        if created:
            messages.success(request, "Create Success")
        else:
            messages.success(request, "Update Success")

        return redirect(reverse('hotel_image') + '?' + urllib.parse.urlencode(request.GET))


def hotel_image_delete(request, id):
    img = Images.objects.get(id=id)
    img.delete()
    messages.success(request, "Delete Success")
    # Because the image may be under hotel management or room management, make a judgment and if it cannot be found, then jump to the hotel management list
    if img.hotel_id:
        return redirect(f"{reverse('hotel_image')}?hotel_id={img.hotel_id}")
    elif img.room_id:
        return redirect(f"{reverse('hotel_image')}?room_id={img.room_id}")
    else:
        return redirect(reverse('hotel_manage_list'))


def room_manage_list(request, hotel_id):
    """View hotel room type list in the background"""
    param = request.GET
    page = int(param.get('page', '1'))
    hotel = Hotel.objects.get(id=hotel_id)
    page_size = 15
    rooms = Room.objects.filter(hotel_id=hotel_id)
    paginator = Paginator(rooms, page_size)
    page_obj = paginator.page(page)
    return render(request,
                  'hotel_page/room_manage_list.html',
                  {
                      'page': page_obj,
                      'hotel': hotel,
                  })


def room_manage_detail(request, id=None):
    """View or create/modify room types"""
    hotel_id = request.GET.get('hotel_id')
    if request.method == 'GET':
        param = request.GET
        room = None
        if id:
            room = Room.objects.get(id=id)
        hotel = Hotel.objects.get(id=hotel_id)
        return render(request,
                      'hotel_page/room_manage_detail.html',
                      {
                          'hotel': hotel,
                          'room': room,
                      })
    elif request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        room, _ = Room.objects.update_or_create(
            id=id,
            defaults=data,
        )
        if id:
            messages.success(request, 'Update Success')
            return redirect(reverse('room_manage_detail', kwargs=dict(id=room.id)))
        else:
            room.hotel_id=hotel_id
            messages.success(request, 'Create Success')
            return redirect(reverse('room_manage_list', kwargs=dict(hotel_id=room.hotel_id)))


def room_delete(request, id):
    """delete room"""
    Hotel.objects.filter(id=id).delete()
    return redirect('hotel_manage_list')
