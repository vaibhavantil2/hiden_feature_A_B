import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from environments.exceptions import EnvironmentHeaderNotPresentError
from environments.identities.models import Identity
from environments.models import Environment
from util.views import SDKAPIView

from .serializers import SegmentSerializer
from .permissions import SegmentPermissions

logger = logging.getLogger()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "identity",
                openapi.IN_QUERY,
                "Optionally provide the id of an identity to get only the segments they match",
                required=False,
                type=openapi.TYPE_INTEGER,
            )
        ]
    ),
)
class SegmentViewSet(viewsets.ModelViewSet):
    serializer_class = SegmentSerializer
    permission_classes = [IsAuthenticated, SegmentPermissions]

    def get_queryset(self):
        project = get_object_or_404(
            self.request.user.get_permitted_projects(["VIEW_PROJECT"]),
            pk=self.kwargs["project_pk"],
        )
        queryset = project.segments.all()

        identity_pk = self.request.query_params.get("identity")
        if identity_pk:
            identity = Identity.objects.get(pk=identity_pk)
            queryset = queryset.filter(
                id__in=[segment.id for segment in identity.get_segments()]
            )

        return queryset
