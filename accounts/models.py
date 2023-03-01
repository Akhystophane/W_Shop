from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm



# Create your models here.
class Shopper(AbstractUser):
    address = models.CharField(("address"), max_length=150, blank=True)
    zipcode = models.CharField(("zipcode"), max_length=150, blank=True)
    state = models.CharField(("state"), max_length=150, blank=True)
    city = models.CharField(("city"), max_length=150, blank=True)
    is_registered = models.BooleanField(default=False)
    device = models.CharField(("device"), max_length=150, blank=True)

class FormShopper(ModelForm):
    class Meta:
        model = Shopper
        fields = ['address', 'zipcode', 'state', 'city']