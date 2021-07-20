import json
import typing

from django.urls import reverse
from rest_framework.test import APIClient

from features.feature_types import STANDARD, MULTIVARIATE
from features.value_types import STRING


def create_feature_with_api(
    client: APIClient,
    project_id: int,
    feature_name: str,
    initial_value: str,
    multivariate_options: typing.List[typing.Tuple[str, float]] = None,
) -> int:
    """
    Create a feature against the API using the provided test client.

    :param client: DRF api client to use to make the request
    :param feature_name: Name of the feature to create
    :param initial_value: Initial value to give the feature
    :param multivariate_options: List of 2-tuples containing the string value and percentage allocation
    :return: id of the created feature
    """
    multivariate_options = multivariate_options or []

    create_feature_url = reverse(
        "api-v1:projects:project-features-list", args=[project_id]
    )
    create_standard_feature_data = {
        "name": feature_name,
        "type": MULTIVARIATE if multivariate_options else STANDARD,
        "initial_value": initial_value,
        "default_enabled": True,
        "multivariate_options": [
            {
                "type": STRING,
                "string_value": mv_option[0],
                "default_percentage_allocation": mv_option[1],
            }
            for mv_option in multivariate_options
        ],
    }
    create_standard_feature_response = client.post(
        create_feature_url,
        data=json.dumps(create_standard_feature_data),
        content_type="application/json",
    )
    return create_standard_feature_response.json()["id"]
