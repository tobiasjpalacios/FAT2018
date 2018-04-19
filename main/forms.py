from django.forms import ModelForm
from .models import Retired

class RetiredForm(ModelForm):
    class Meta:
        model = Retired
        fields = ['first_name', 'last_name', 'personalID']