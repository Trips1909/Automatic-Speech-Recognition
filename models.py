from django.db import models

# Create your models here.
class ButtonState(models.Model):
    is_active = models.BooleanField(default=False)
