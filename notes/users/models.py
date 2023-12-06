from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from pathlib import Path

# Create your models here.
# Extending User Model Using a One-To-One Link


def validator(value):
    file_size = value.size
    if file_size > 1_000_000:
        return ValidationError('Max size 1Mb')
    return value


def upload_avatar(instance, filename):
    upload_to = Path(instance.user.username)
    ext = Path(filename).suffix
    new_filename = f'{uuid4().hex}{ext}'
    return str(upload_to/new_filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default_avatar.png', upload_to=upload_avatar, validators=[validator])

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 240 or img.width > 240:
            new_img = (240, 240)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
