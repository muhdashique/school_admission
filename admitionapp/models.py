from django.db import models

class User(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.mobile

