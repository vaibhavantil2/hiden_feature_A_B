from app_analytics.views import SDKAnalyticsFlags, SelfHostedTelemetryAPIView
from django.conf.urls import url
from django.urls import include
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import authentication, permissions, routers

from environments.identities.traits.views import SDKTraits
from environments.identities.views import SDKIdentities
from features.views import SDKFeatureStates
from organisations.views import chargebee_webhook

schema_view = get_schema_view(
    openapi.Info(
        title="Flagsmith API",
        default_version="v1",
        description="",
        license=openapi.License(name="BSD License"),
        contact=openapi.Contact(email="support@flagsmith.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.SessionAuthentication,),
)

traits_router = routers.DefaultRouter()
traits_router.register(r"", SDKTraits, basename="sdk-traits")

app_name = "v1"

urlpatterns = [
    url(r"^organisations/", include("organisations.urls"), name="organisations"),
    url(r"^projects/", include("projects.urls"), name="projects"),
    url(r"^environments/", include("environments.urls"), name="environments"),
    url(r"^features/", include("features.urls"), name="features"),
    url(r"^users/", include("users.urls")),
    url(r"^e2etests/", include("e2etests.urls")),
    url(r"^audit/", include("audit.urls")),
    url(r"^auth/", include("custom_auth.urls")),
    # Chargebee webhooks
    url(r"cb-webhook/", chargebee_webhook, name="chargebee-webhook"),
    # Client SDK urls
    url(r"^flags/$", SDKFeatureStates.as_view(), name="flags"),
    url(r"^identities/$", SDKIdentities.as_view(), name="sdk-identities"),
    url(r"^traits/", include(traits_router.urls), name="traits"),
    url(r"^analytics/flags/$", SDKAnalyticsFlags.as_view()),
    url(r"^analytics/telemetry/$", SelfHostedTelemetryAPIView.as_view()),
    # API documentation
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
