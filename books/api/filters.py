from django_filters import filterset
from django.contrib.auth import get_user_model

from main.models import Book


User = get_user_model()


class BookFilterSet(filterset.FilterSet):
    authors = filterset.ModelMultipleChoiceFilter(
        field_name='authors__username',
        to_field_name='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Book
        fields = (
            'authors',
        )
