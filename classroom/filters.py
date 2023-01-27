import django_filters
from classroom.models import Customer

class CustomerFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(lookup_expr='iexact')
	class Meta:

		model = Customer
		fields = ['car_model','parking_time']