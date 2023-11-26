import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # Inheriting the user abstract class of django, the built-in login and registration function of django can be used

    email = models.EmailField(null=True, blank=True)
    nickname = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        unique=True,
    )

    avatar = models.ImageField(
        null=True,
        blank=True,
        default='/static/img/default_avatar.jpg',
        upload_to='avatar/',
    )

    class Meta:
        db_table = 'user'


class Country(models.Model):
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'country'


class City(models.Model):
    name = models.CharField(max_length=200)
    # Foreign key, the actual column name in the table is country_ ID, why is it followed by an ID? This is the primary key of the class attribute and foreign key associated table you specified, which is f "{attribute name} _ {primary key of the associated table}"
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'city'


class HotelChain(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'hotel_chain'


class HotelBrand(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'hotel_brand'


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)  # null=True 可以为null blank=True可以为空(创建的时候不传)
    website = models.CharField(max_length=200, null=True, blank=True)
    tel = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    star = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='city_hotels', null=True, blank=True)
    chain = models.ForeignKey(HotelChain, on_delete=models.SET_NULL, related_name='chain_hotels', null=True, blank=True)
    brand = models.ForeignKey(HotelBrand, on_delete=models.SET_NULL, related_name='brand_hotels', null=True, blank=True)

    class Meta:
        db_table = 'hotel'

    # @property
    # def min_price_room(self):
    #     rooms = self.hotel_rooms.all()
    #     min_room = None
    #     for room in rooms:
    #         if not min_room:
    #             min_room = room
    #         else:
    #             if room.base_price < min_room.base_price:
    #                 min_room = room
    #     return min_room

    min_price_room = None


class Room(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    base_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rooms', null=True, blank=True)
    max_adults = models.IntegerField(default=2)
    max_children = models.IntegerField(default=1)
    breakfast = models.BooleanField(default=False)
    cancellation_days = models.IntegerField(default=0, null=True, blank=True)  # 可以提前几天免费取消
    can_smoke = models.BooleanField(default=False)
    window = models.BooleanField(default=False)
    bed_type = models.CharField(max_length=200)
    bed_count = models.IntegerField(default=1)
    inventory = models.IntegerField(default=10)

    class Meta:
        db_table = 'room'


class Order(models.Model):
    order_no = models.CharField(max_length=200, unique=True)
    create_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=200)
    special_requests = models.TextField(default='', null=True, blank=True)
    checkin = models.CharField(max_length=200)
    checkout = models.CharField(max_length=200)
    room_count = models.IntegerField()
    adults = models.IntegerField()
    children = models.IntegerField()
    status_code = models.CharField(max_length=20, choices=(('1', 'Confirmed'),
                                                           ('2', 'Completed'),
                                                           ('3', 'Cancel pending'),
                                                           ('4', 'Cancelled'),
                                                           ('5', 'Cancel failed'),
                                                           ))

    class Meta:
        db_table = 'order'

    @property
    def nights(self):
        checkin = datetime.datetime.strptime(self.checkin, '%Y/%m/%d')
        checkout = datetime.datetime.strptime(self.checkout, '%Y/%m/%d')
        return (checkout - checkin).days


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(max_length=200)
    payment_no = models.CharField(max_length=200)
    payment_status = models.CharField(max_length=200, default='paid')
    price = models.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        db_table = 'payment'


class Images(models.Model):
    url = models.CharField(max_length=255)
    desc = models.CharField(max_length=30)
    hotel = models.ForeignKey(Hotel, related_name='hotel_images', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, related_name='room_images', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'images'
# Create your models here.
