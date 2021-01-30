"""AWS CodePipeline Integration."""
import boto3
import botocore
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (CONF_ACCESS_KEY_ID, CONF_PIPELINE_NAMES, CONF_REGION,
                    CONF_SECRET_ACCESS_KEY, DOMAIN, SERVICE_EXECUTE_PIPELINE)

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
    """Setup the client and register service with HA."""
    client = boto3.client(
        "codepipeline",
        region_name=config[DOMAIN][CONF_REGION],
        aws_access_key_id=config[DOMAIN][CONF_ACCESS_KEY_ID],
        aws_secret_access_key=config[DOMAIN][CONF_SECRET_ACCESS_KEY],
    )

    # Save client and pipeline names to config data for later use.
    hass.data[DOMAIN] = {
        "instance": client,
        "pipeline_names": config[DOMAIN][CONF_PIPELINE_NAMES],
    }

    def execute_pipeline(call):
        """Execute a given pipeline by name."""
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
