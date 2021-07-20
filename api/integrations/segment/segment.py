import logging
import typing

from analytics.client import Client as SegmentClient
from integrations.common.wrapper import AbstractBaseIdentityIntegrationWrapper

if typing.TYPE_CHECKING:
    from environments.identities.models import Identity
    from features.models import FeatureState

logger = logging.getLogger(__name__)


class SegmentWrapper(AbstractBaseIdentityIntegrationWrapper):
    def __init__(self, api_key: str):
        self.analytics = SegmentClient(write_key=api_key)

    def _identify_user(self, data: dict) -> None:
        self.analytics.identify(**data)
        logger.debug(f"Sent event to Segment.")

    def generate_user_data(
        self, identity: "Identity", feature_states: typing.List["FeatureState"]
    ) -> dict:
        feature_properties = {}

        for feature_state in feature_states:
            value = feature_state.get_feature_state_value(identity=identity)
            feature_properties[feature_state.feature.name] = (
                value if (feature_state.enabled and value) else feature_state.enabled
            )

        return {
            "user_id": identity.identifier,
            "traits": feature_properties,
        }
