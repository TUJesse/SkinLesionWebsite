from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import forms
from django import forms

def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg']
    extension = str(value.name).lower().split('.')[-1]
    if extension not in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload a JPG file.")

class ImageForm(forms.Form):
    image = forms.ImageField(required=True)
