from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'webp']
    extension = str(value.name).lower().split('.')[-1]
    if extension not in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload a JPG file.")

def validate_image_size(value):
    max_size = 100 * 1024
    if value.size > max_size:
        raise ValidationError("File size exceeds the maximum allowed limit of 100 MB.")

class ImageForm(forms.Form):
    image = forms.ImageField(required=True, validators=[validate_image_extension, validate_image_size])

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
