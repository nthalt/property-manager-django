from django import forms
from .models import Property, Location
from .widgets import UniqueLocationFilteredSelectMultiple


class PropertyAdminForm(forms.ModelForm):
    locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.order_by('name').distinct('name'),
        widget=UniqueLocationFilteredSelectMultiple(
            "Locations", is_stacked=False
        )
    )

    class Meta:
        model = Property
        fields = '__all__'
