from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class CustomPaymentManager(models.Manager):    
    def get_payment_by_id(self, id):
        return self.filter(id=id).first()
