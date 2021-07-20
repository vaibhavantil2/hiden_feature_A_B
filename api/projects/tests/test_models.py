from unittest import mock

import pytest
from django.conf import settings
from django.db.models import QuerySet
from django.test import TransactionTestCase

from organisations.models import Organisation
from projects.models import Project
from segments.models import EQUAL, Condition, Segment, SegmentRule


@pytest.mark.django_db()
def test_get_segments_from_cache(project, monkeypatch):
    # Given
    mock_project_segments_cache = mock.MagicMock()
    mock_project_segments_cache.get.return_value = None

    monkeypatch.setattr(
        "projects.models.project_segments_cache", mock_project_segments_cache
    )

    # When
    segments = project.get_segments_from_cache()

    # Then
    mock_project_segments_cache.get.assert_called_with(project.id)
    mock_project_segments_cache.set.assert_called_with(
        project.id, segments, timeout=settings.CACHE_PROJECT_SEGMENTS_SECONDS
    )


@pytest.mark.django_db()
def test_get_segments_from_cache_set_not_called(project, segments, monkeypatch):
    # Given
    mock_project_segments_cache = mock.MagicMock()
    mock_project_segments_cache.get.return_value = project.segments.all()

    monkeypatch.setattr(
        "projects.models.project_segments_cache", mock_project_segments_cache
    )

    # When
    segments = project.get_segments_from_cache()

    # Then
    assert segments

    # And correct calls to cache are made
    mock_project_segments_cache.get.assert_called_once_with(project.id)
    mock_project_segments_cache.set.assert_not_called()
