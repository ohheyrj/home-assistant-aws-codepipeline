"""AWS Codepipeline Sensor."""
import logging

import boto3
import botocore
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntries
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity

from .const import (ATTR_PIPELINE_LAST_UPDATE_TIME, ATTR_PIPELINE_TRIGGER,
                    ATTRIBUTION, CONF_ACCESS_KEY_ID, CONF_PIPELINE_NAMES,
                    CONF_REGION, CONF_SECRET_ACCESS_KEY, DOMAIN, ICON)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup sensor platform."""
    # Grab client from data storage
    client = hass.data[DOMAIN]["instance"]

    pipelines = hass.data[DOMAIN][CONF_PIPELINE_NAMES]

    # For each pipeline, register the sensor.
    for p in pipelines:
        add_entities([AwsCodepipelineSensor(client, p)])

    return True

class AwsCodepipelineSensor(Entity):
    def __init__(self, client, pipeline_name):
        """Init the sensor."""
        self._name = f"AWS Codepipeline {pipeline_name}"
        self._state = None
        self._client = client
        self._last_update = None
        self._pipeline_trigger = None
        self._pipeline_name = pipeline_name

    @property
    def name(self):
        """Return sensor name."""
        return self._name

    @property
    def icon(self):
        """Return sensor icon."""
        return ICON

    @property
    def state(self):
        """Return sensor state."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return sensor attributes."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_PIPELINE_LAST_UPDATE_TIME: self._last_update,
            ATTR_PIPELINE_TRIGGER: self._pipeline_trigger
        }

    def update(self):
        """Update the sensor."""
        _LOGGER.debug(f"Getting AWS Codepipeline sensor update for pipeline {self._pipeline_name}")
        try:
            data = self._client.list_pipeline_executions(
                pipelineName=self._pipeline_name
            )['pipelineExecutionSummaries'][0]
        except:
            raise Warning(f"Problem finding pipeline {self._pipeline_name}")

        self._state = data['status']
        self._last_update = data['lastUpdateTime']
        self._pipeline_trigger = data['trigger']['triggerType']
