from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntries
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import boto3
import botocore
from .const import (
    DOMAIN,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION,
    CONF_PIPELINE_NAMES,
    ICON,
    ATTR_PIPELINE_LAST_UPDATE_TIME,
    ATTR_PIPELINE_TRIGGER,
    ATTRIBUTION
)
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
import logging

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    client = hass.data[DOMAIN]["instance"]

    pipelines = hass.data[DOMAIN][CONF_PIPELINE_NAMES]

    for p in pipelines:
        add_entities([AwsCodepipelineSensor(client, p)])

    return True

class AwsCodepipelineSensor(Entity):
    def __init__(self, client, pipeline_name):
        _LOGGER.info("Init logger")
        """Init the sensor."""
        self._name = f"AWS Codepipeline {pipeline_name}"
        self._state = None
        self._client = client
        self._last_update = None
        self._pipeline_trigger = None
        self._pipeline_name = pipeline_name

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return ICON

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_PIPELINE_LAST_UPDATE_TIME: self._last_update,
            ATTR_PIPELINE_TRIGGER: self._pipeline_trigger
        }

    def update(self):
        _LOGGER.info("Getting sensor update")
        try:
            data = self._client.list_pipeline_executions(
                pipelineName=self._pipeline_name
            )['pipelineExecutionSummaries'][0]
        except:
            raise Warning(f"Problem finding pipeline {self._pipeline_name}")

        self._state = data['status']
        self._last_update = data['lastUpdateTime']
        self._pipeline_trigger = data['trigger']['triggerType']
