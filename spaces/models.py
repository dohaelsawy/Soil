from django.db import models


class Space(models.Model):
    SPACE_TYPES = [
        ('private_office', 'Private Office'),
        ('meeting_room', 'Meeting Room'),
        ('hot_desk', 'Hot Desk'),
    ]

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=50, choices=SPACE_TYPES)
    capacity = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)