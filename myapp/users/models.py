from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    user_type_choices = (('normal', 'Normal'), ('doctor', 'Doctor'))
    user_type = models.CharField(max_length=10, choices=user_type_choices)

    def save(self, *args, **kwargs):
        # Hash the password before saving if it's not hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
class File(models.Model):
    DOCUMENT = 'document'
    PRESCRIPTION = 'prescription'
    FILE_TYPES = [
        (DOCUMENT, 'Document'),
        (PRESCRIPTION, 'Prescription'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default=DOCUMENT)
    file = models.FileField(upload_to='user_files/')  # Store uploaded files in 'media/user_files/' directory
    file_path = models.CharField(max_length=255, blank=True, null=True)  # Optional field to store a file link or path

    def __str__(self):
        return f'{self.user.username} - {self.file_type}'

