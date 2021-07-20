import json
from unittest.case import TestCase

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from environments.models import Environment
from integrations.amplitude.models import AmplitudeConfiguration
from organisations.models import Organisation, OrganisationRole
from projects.models import Project
from util.tests import Helper


@pytest.mark.django_db
class AmplitudeConfigurationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = Helper.create_ffadminuser()
        self.client.force_authenticate(user=user)

        self.organisation = Organisation.objects.create(name="Test Org")
        user.add_organisation(
            self.organisation, OrganisationRole.ADMIN
        )  # admin to bypass perms

        self.project = Project.objects.create(
            name="Test project", organisation=self.organisation
        )
        self.environment = Environment.objects.create(
            name="Test Environment", project=self.project
        )
        self.list_url = reverse(
            "api-v1:environments:integrations-amplitude-list",
            args=[self.environment.api_key],
        )

    def test_should_create_amplitude_config_when_post(self):
        # Given
        data = {"api_key": "abc-123"}

        # When
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type="application/json",
        )

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert (
            AmplitudeConfiguration.objects.filter(environment=self.environment).count()
            == 1
        )

    def test_should_return_BadRequest_when_duplicate_amplitude_config_is_posted(self):
        # Given
        config = AmplitudeConfiguration.objects.create(
            api_key="api_123", environment=self.environment
        )

        # When
        data = {"api_key": config.api_key}
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type="application/json",
        )

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            AmplitudeConfiguration.objects.filter(environment=self.environment).count()
            == 1
        )

    def test_should_update_configuration_when_put(self):
        # Given
        config = AmplitudeConfiguration.objects.create(
            api_key="api_123", environment=self.environment
        )

        api_key_updated = "new api"
        data = {"api_key": api_key_updated}

        # When
        url = reverse(
            "api-v1:environments:integrations-amplitude-detail",
            args=[self.environment.api_key, config.id],
        )
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json",
        )
        config.refresh_from_db()

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert config.api_key == api_key_updated

    def test_should_return_amplitude_config_list_when_requested(self):
        # Given - set up data

        # When
        response = self.client.get(self.list_url)

        # Then
        assert response.status_code == status.HTTP_200_OK

    def test_should_remove_configuration_when_delete(self):
        # Given
        config = AmplitudeConfiguration.objects.create(
            api_key="api_123", environment=self.environment
        )

        # When
        url = reverse(
            "api-v1:environments:integrations-amplitude-detail",
            args=[self.environment.api_key, config.id],
        )
        res = self.client.delete(url)

        # Then
        assert res.status_code == status.HTTP_204_NO_CONTENT
        #  and
        assert not AmplitudeConfiguration.objects.filter(
            environment=self.environment
        ).exists()
