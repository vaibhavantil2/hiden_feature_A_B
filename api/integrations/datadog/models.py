from django.db import models

from integrations.common.models import IntegrationsModel
from projects.models import Project
import logging

logger = logging.getLogger(__name__)


class DataDogConfiguration(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="data_dog_config"
    )
    base_url = models.URLField(blank=False, null=False)
    api_key = models.CharField(max_length=100, blank=False, null=False)
