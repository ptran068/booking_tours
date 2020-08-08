import uuid
from django.db import models
from django.conf import settings
from tours.models import Tours
from .managers import CustomPaymentManager

User = settings.AUTH_USER_MODEL


PAYMENT_STATUS = (
    ('PENDING','PENDING'),
    ('PAID','PAID')
)


class Payments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    charge_id = models.CharField(max_length=255, blank=True, null=True)
    card_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    tour = models.ForeignKey(Tours, blank=False, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    status = models.CharField(choices=PAYMENT_STATUS, default='PENDING', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomPaymentManager()

    def __str__(self):
        return self.caption
