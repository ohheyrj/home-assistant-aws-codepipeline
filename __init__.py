"""AWS CodePipeline"""
from .const import (
    DOMAIN,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION,
    CONF_PIPELINE_NAME,
    SERVICE_EXECUTE_PIPELINE,
)
import boto3
import botocore
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ACCESS_KEY_ID): cv.string,
                vol.Required(CONF_SECRET_ACCESS_KEY): cv.string,
                vol.Optional(CONF_REGION, default="us-east-1"): cv.string,
                vol.Required(CONF_PIPELINE_NAME): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    client = boto3.client(
        "codepipeline",
        region_name=config[DOMAIN][CONF_REGION],
        aws_access_key_id=config[DOMAIN][CONF_ACCESS_KEY_ID],
        aws_secret_access_key=config[DOMAIN][CONF_SECRET_ACCESS_KEY],
    )

    hass.data[DOMAIN] = {
        "instance": client,
        "pipeline_name": config[DOMAIN][CONF_PIPELINE_NAME],
    }

    def execute_pipeline(call):
        pipeline = config[DOMAIN][CONF_PIPELINE_NAME]
        try:
            client.start_pipeline_execution(name=pipeline)
        except botocore.exceptions.ClientError:
            raise Warning("Cannot execute pipeline")

    hass.services.register(
        DOMAIN,
        f"SERVICE_EXECUTE_PIPELINE_{config[DOMAIN][CONF_PIPELINE_NAME]}",
        execute_pipeline
    )
    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True
