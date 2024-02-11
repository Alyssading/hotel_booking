import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse

from app.models import Room, Order, Payment

@login_required(login_url='/login')
def booking_room(request):
    """Booking Room"""
    params = request.GET
    room_id = params.get('room_id')
    checkin, checkout = params.get('daterange').split(' - ') # splite checkin and checkout date
    adults = int(params.get('adults'))
    children = int(params.get('children'))
    room_count = int(params.get('room_count'))
    room = Room.objects.get(id=room_id)
    if request.method == 'GET':
        return render(request, 'booking_page/booking_room.html', {
            'room': room,
            'hotel': room.hotel,
            'adults': adults,
            'children': children,
            'checkin': checkin,
            'checkout': checkout,
            'daterange': params.get('daterange'),
            'room_count': room_count,
        })
    else:
        data = request.POST
        order = Order.objects.create(
            order_no=f'No-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}{random.randint(1, 10)}',
            user=request.user,
            hotel=room.hotel,
            room=room,
            customer_name=data['first_name'] + ' ' + data['last_name'],
            customer_email=data['email'],
            customer_phone=data['phone'],
            special_requests=data['special_requests'],
            adults=adults,
            children=children,
            checkout=checkout,
            checkin=checkin,
            room_count=room_count
        )
        payment = Payment.objects.create(
            payment_no=data['payment_no'],
            payment_status='paid',
            order=order,
            price=room.base_price,
            payment_type=data['payment_type']
        )
        messages.add_message(
            request,
            level=messages.SUCCESS,
            message='Booking successful'
        )
        return redirect(reverse('booking_list'))

@login_required(login_url='/login')
def booking_list(request):
    """Booking list for user"""
    param = request.GET
    user = request.user
    page_size = 10
    page = int(param.get('page', '1'))
    orders = Order.objects.filter(user=user).order_by('-id') 
    # 'select * from order where user_id=1 order by id desc'
    paginator = Paginator(orders, page_size) # fen ye
    page_obj = paginator.page(page)
    return render(request,
                  'booking_page/booking_list.html',
                  {
                      'page': page_obj,
                      'orders': page_obj.object_list
                  })

@login_required(login_url='/login')
def booking_detail(request, id):
    """booking details"""
    order = Order.objects.get(id=id)
    return render(request, 'booking_page/booking_detail.html', {'order': order})

@login_required(login_url='/login')
def booking_cancel(request, id):
    """user cancel bookings"""
    # order.object.filter(id=id).update(status_code=3) ba fu he tiao jian de (quan bu) geng xin
    order = Order.objects.get(id=id)
    order.status_code = '3'
    order.save() 
    messages.success(request,
                     'The application has been successfully cancelled and is waiting for customer service to process.')
    return redirect(reverse('booking_list'))

@login_required(login_url='/login')
def booking_status(request, id):
    """admin modify booking status"""
    order = Order.objects.get(id=id)
    order.status_code = request.GET.get('status')
    order.save()
    messages.success(request,
                     'Status modification successful.')
    return redirect(reverse('booking_manage_list'))

@login_required(login_url='/login')
def booking_manage_list(request):
    """admin checking bookings"""
    param = request.GET
    orders = Order.objects.all().order_by('-id')
    page_size = 20
    page = int(param.get('page', '1'))
    paginator = Paginator(orders, page_size)
    page_obj = paginator.page(page)
    return render(request,
                  'booking_page/booking_manage_list.html',
                  {
                      'page': page_obj,
                      'orders': page_obj.object_list
                  })
