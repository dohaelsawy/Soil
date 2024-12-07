from django.test import TestCase
from .models import Bookings
from spaces.models import Space
from django.contrib.auth.models import User
from datetime import time


class BookingsViewTest(TestCase) :

    def setUp(self):
        self.test_space = Space.objects.create(
            name="room1",
            type='private_office',
            capacity=30,
            price_per_hour=100,
            is_available=True
        )
        self.test_space.save()

        self.test_space2 = Space.objects.create(
            name="room2",
            type='private_office',
            capacity=30,
            price_per_hour=100,
            is_available=False
        )
        self.test_space.save()

        self.test_booking = Bookings.objects.create(
            username="doha",
            user_email='doha@gmail.com',
            space_id=self.test_space,
            start_time=time(8,12),
            end_time=time(8,30),
            status='pending'
        )
        self.test_booking.save()

        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpassword'
        )
        self.admin_user.save()

        self.client.force_login(self.admin_user)


    def test_create_booking_success(self):
        instance = Space.objects.first()
        response = self.client.post(
            path='/bookings/',
            data={
                "username":"doha",
                "user_email":"doha@gmail.com",
                "space_id": 1,
                "start_time":time(8,31),
                "end_time":time(8,40)
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,201)

        response_data = response.json()
        self.assertEqual(response_data['username'],"doha")
        self.assertEqual(response_data['user_email'],"doha@gmail.com")
        self.assertEqual(response_data['start_time'],'08:31:00')
        self.assertEqual(response_data['end_time'],'08:40:00')

    def test_create_taken_booking_error(self):
        instance = Space.objects.filter(is_available=True).first()
        response = self.client.post(
            path='/bookings/',
            data={
                "username":"doha",
                "user_email":"doha@gmail.com",
                "space_id": instance.id,
                "start_time":time(8,12),
                "end_time":time(8,30)
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
        response_data = response.json()
        self.assertEqual(response_data['errors']['non_field_errors'],['This time slot is already booked'])


    def test_create_start_time_before_end_time_booking_error(self):
        instance = Space.objects.first()
        response = self.client.post(
            path='/bookings/',
            data={
                "username":"doha",
                "user_email":"doha@gmail.com",
                "space_id": instance.id,
                "start_time":time(8,30),
                "end_time":time(8,00)
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['errors']['non_field_errors'],['Start time must be before end time'])


    def test_create_unavailable_booking_error(self):
        instance = Space.objects.filter(is_available=False).first()
        response = self.client.post(
            path='/bookings/',
            data={
                "username":"doha",
                "user_email":"doha@gmail.com",
                "space_id": instance.id,
                "start_time":time(8,30),
                "end_time":time(8,00)
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
        response_data = response.json()
        self.assertEqual(response_data['errors']['space_id'],['This space is currently not available for booking.'])


    def test_create_overlap_booking_error(self):
        instance = Space.objects.filter(is_available=True).first()
        response = self.client.post(
            path='/bookings/',
            data={
                "username":"doha",
                "user_email":"doha@gmail.com",
                "space_id": instance.id,
                "start_time":time(8,10),
                "end_time":time(8,15)
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
        response_data = response.json()
        self.assertEqual(response_data['errors']['non_field_errors'],['This time slot is already booked'])


    def test_retrieve_booking_success(self):
        instance = Bookings.objects.first()
        response = self.client.get(
            path=f'/bookings/{instance.id}/',
        )
        self.assertEqual(response.status_code,200)
        response_data = response.json()
        self.assertEqual(response_data['username'],instance.username)
        self.assertEqual(response_data['user_email'],instance.user_email)
        self.assertEqual(response_data['start_time'],str(instance.start_time))
        self.assertEqual(response_data['end_time'],str(instance.end_time))
        self.assertEqual(response_data['status'],instance.status)


    def test_gets_booking_success(self):
        instances = Bookings.objects.all()
        booking_size_list = instances.count()
        response = self.client.get(
            path=f'/bookings/',
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),booking_size_list)
        

    
    
    

    def test_update_booking_success(self):
        instance = Bookings.objects.first()
        response = self.client.patch(
            path=f'/bookings/{instance.id}/',
            data={
                "status": "confirmed",
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,200)
        
        response_data = response.json()
        self.assertEqual(response_data['status'],"confirmed")
