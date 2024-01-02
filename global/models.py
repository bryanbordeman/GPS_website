from django.db import models
from django.core.validators import MaxLengthValidator


class Request(models.Model):
    first_name = models.CharField(max_length=200, null= True)
    last_name = models.CharField(max_length=200, null= True)
    email = models.EmailField(max_length=200, null= True,)
    phone = models.IntegerField()
    company_name = models.CharField(max_length=200)
    description = models.TextField(max_length=250, blank=True,
                                   validators=[MaxLengthValidator(250)])
