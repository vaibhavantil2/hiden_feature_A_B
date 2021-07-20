from django.conf.urls import include, url
from rest_framework_nested import routers

from organisations.views import OrganisationWebhookViewSet
from .invites.views import InviteViewSet, InviteLinkViewSet
from users.views import FFAdminUserViewSet, UserPermissionGroupViewSet

from . import views

router = routers.DefaultRouter()
router.register(r"", views.OrganisationViewSet, basename="organisation")

organisations_router = routers.NestedSimpleRouter(router, r"", lookup="organisation")
organisations_router.register(
    r"invites", InviteViewSet, basename="organisation-invites"
)
organisations_router.register(
    r"invite-links", InviteLinkViewSet, basename="organisation-invite-links"
)
organisations_router.register(
    r"users", FFAdminUserViewSet, basename="organisation-users"
)
organisations_router.register(
    r"groups", UserPermissionGroupViewSet, basename="organisation-groups"
)
organisations_router.register(
    r"webhooks", OrganisationWebhookViewSet, basename="organisation-webhooks"
)

app_name = "organisations"

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^", include(organisations_router.urls)),
]
