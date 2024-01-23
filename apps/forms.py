from django import forms
from .models import district_info, school_info

# Create your models here.
class TodoForm(forms.ModelForm):
    class Meta:
        model = district_info
        fields = ('name', 'city', 'district')
        
        