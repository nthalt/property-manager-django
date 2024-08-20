from django.contrib.admin.widgets import FilteredSelectMultiple

from properties.models import Location


class UniqueLocationFilteredSelectMultiple(FilteredSelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        self.choices.queryset = Location.objects.order_by(
            'name').distinct('name')
        return super().render(name, value, attrs, renderer)
