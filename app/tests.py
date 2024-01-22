# Create your tests here.
import datetime

from django.test import TestCase

from app.models import Hotel, Country, City, Order, User, Room, Payment


class HotelTestCase(TestCase):
    def setUp(self):
        test_hotel = Hotel.objects.create(
            name='testname',
            address='testaddress',
            email='testemail',
            website='testwebsite',
            tel='testtel',
            postcode='testpostcode',
            latitude='testlatitude',
            longitude='testlongitude',
            star='5',
        )
        test_country = Country.objects.create(name='test', country_code='ts')
        city = City.objects.create(name='test', country=test_country)
        test_hotel.city = city
        test_hotel.save()

    def test_create_hotel(self):
        hotel = Hotel.objects.get(name="testname")
        self.assertEqual(hotel.name, 'testname')
        self.assertEqual(hotel.city.name, 'test')
        self.assertEqual(hotel.city.country.name, 'test')


class RoomTestCase(TestCase):
    def setUp(self):
        test_hotel = Hotel.objects.create(
            name='testname',
            address='testaddress',
            email='testemail',
            website='testwebsite',
            tel='testtel',
            postcode='testpostcode',
            latitude='testlatitude',
            longitude='testlongitude',
            star='5',
        )
        test_country = Country.objects.create(name='test', country_code='ts')
        city = City.objects.create(name='test', country=test_country)
        test_hotel.city = city
        test_hotel.save()
        test_room = Room.objects.create(
            name='testroom',
            area='20m²',
            base_price=100,
            hotel=test_hotel,
            max_adults=2,
            max_children=1,
            breakfast=False,
            cancellation_days=30,
            can_smoke=False,
            window=True,
            bed_type='King bed',
            bed_count=1,
            inventory=10,
        )

    def test_create_room(self):
        room = Room.objects.get(name='testroom')
        self.assertEqual(room.name, 'testroom')
        self.assertEqual(room.hotel.name, 'testname')


class OrderTestCase(TestCase):

    def setUp(self):
        test_hotel = Hotel.objects.create(
            name='testname',
            address='testaddress',
            email='testemail',
            website='testwebsite',
            tel='testtel',
            postcode='testpostcode',
            latitude='testlatitude',
            longitude='testlongitude',
            star='5',
        )
        test_country = Country.objects.create(name='test', country_code='ts')
        city = City.objects.create(name='test', country=test_country)
        test_hotel.city = city
        test_hotel.save()
        test_room = Room.objects.create(
            name='testroom',
            area='20m²',
            base_price=100,
            hotel=test_hotel,
            max_adults=2,
            max_children=1,
            breakfast=False,
            cancellation_days=30,
            can_smoke=False,
            window=True,
            bed_type='King bed',
            bed_count=1,
            inventory=10,
        )
        order = Order.objects.create(
            order_no='No-test123456',
            user=User.objects.first(),
            hotel=test_hotel,
            room=test_room,
            customer_name='test',
            customer_email='test@gmail.com',
            customer_phone='123456789',
            special_requests='No',
            checkin='2024/01/01',
            checkout='2024/01/01',
            room_count=2,
            adults=1,
            children=0,
            status_code=1
        )
        payment = Payment.objects.create(
            payment_type=1,
            payment_no=order.order_no,
            order=order,
            price=test_room.base_price
        )

    def test_create_order(self):
        order = Order.objects.get(order_no='No-test123456')
        self.assertEqual(order.payment.price, 100)
        self.assertEqual(order.order_no, 'No-test123456')
        self.assertEqual(order.create_date, datetime.date.today())
