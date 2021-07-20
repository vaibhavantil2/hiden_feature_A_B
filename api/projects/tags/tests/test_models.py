import pytest
from django.test import TestCase

from organisations.models import Organisation
from projects.models import Project
from projects.tags.models import Tag


@pytest.mark.django_db
class TagsTestCase(TestCase):
    def setUp(self) -> None:
        self.organisation = Organisation.objects.create(name="Test Org")
        self.project = Project.objects.create(
            name="Test Project", organisation=self.organisation
        )

    def test_create_tag(self):
        # When
        tag = Tag.objects.create(
            label="Test Tag",
            color="#fffff",
            description="Test Tag description",
            project=self.project,
        )

        # Then
        assert tag.project.id == self.project.id
