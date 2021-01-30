"""AWS CodePipeline"""
from .const import (
    DOMAIN,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION,
    CONF_PIPELINE_NAMES,
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
                vol.Required(CONF_PIPELINE_NAMES): vol.All(
                    cv.ensure_list, [cv.string]
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

EXECUTE_PIPELINE_SERVICE_SCHEMA = vol.Schema({vol.Required("pipeline_name"): cv.string})

def setup(hass, config):
    client = boto3.client(
        "codepipeline",
        region_name=config[DOMAIN][CONF_REGION],
        aws_access_key_id=config[DOMAIN][CONF_ACCESS_KEY_ID],
        aws_secret_access_key=config[DOMAIN][CONF_SECRET_ACCESS_KEY],
    )

    hass.data[DOMAIN] = {
        "instance": client,
        "pipeline_names": config[DOMAIN][CONF_PIPELINE_NAMES],
    }

    def execute_pipeline(call):
        pipeline_name = call.data["pipeline_name"]
        try:
            client.start_pipeline_execution(name=pipeline_name)
        except botocore.exceptions.ClientError:
            raise Warning("Cannot execute pipeline")

    hass.services.register(
        DOMAIN,
        SERVICE_EXECUTE_PIPELINE,
        execute_pipeline,
        schema=EXECUTE_PIPELINE_SERVICE_SCHEMA
    )
    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True
