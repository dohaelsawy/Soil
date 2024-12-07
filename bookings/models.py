from django.db import models
from spaces.models import Space

STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Bookings(models.Model):
    username=models.CharField(max_length=255)
    user_email=models.EmailField()
    space_id=models.ForeignKey(Space,on_delete=models.CASCADE)
    start_time=models.TimeField()
    end_time=models.TimeField()
    status=models.CharField(choices=STATUS, default='pending')