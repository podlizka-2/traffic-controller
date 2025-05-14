import django_filters
from .models import DDSRecords, Status, Type, Category, subcategory

class DDSRecordsFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name='date', label='Период дат')
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    type = django_filters.ModelChoiceFilter(queryset=Type.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    subcategory = django_filters.ModelChoiceFilter(queryset=subcategory.objects.all())

    class Meta:
        model = DDSRecords
        fields = []