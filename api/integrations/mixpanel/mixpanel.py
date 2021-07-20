import json
import logging
import typing

import requests

from integrations.common.wrapper import AbstractBaseIdentityIntegrationWrapper

if typing.TYPE_CHECKING:
    from environments.identities.models import Identity
    from features.models import FeatureState

logger = logging.getLogger(__name__)

MIXPANEL_API_URL = "https://api.mixpanel.com"


class MixpanelWrapper(AbstractBaseIdentityIntegrationWrapper):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = f"{MIXPANEL_API_URL}/engage#profile-set"
        self.headers = {
            "Accept": "text/plain",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _identify_user(self, user_data: dict) -> None:
        data = {"data": json.dumps(user_data)}
        response = requests.post(self.url, headers=self.headers, data=data)

        logger.debug(
            "Sent event to Mixpanel. Response code was: %s" % response.status_code
        )
        logger.debug("Sent event to Mixpanel. Body code was: %s" % response.content)

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
            "$token": self.api_key,
            "$distinct_id": identity.identifier,
            "$set": feature_properties,
        }
