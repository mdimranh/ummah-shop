from django.db.models import QuerySet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class CRUDView(APIView):
    serializer_class = None
    lookup_field = None

    def get_queryset(self):
        assert self.queryset is not None, "add queryset or override get_queryset class"
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            return queryset.all()
        return queryset

    # def get(self, request, *args, **kwargs):


#
