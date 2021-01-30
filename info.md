# Home Assistant AWS Codepipeline Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

{% if prerelease %}
### NB!: This is a Beta version!
{% endif %}

An integration to monitor and execute AWS Codepipeline projects within Home Assistant.

## Features

This integration provides one sensor and one service.

### Sensor

The integration will create one sensor for each pipeline specified in the config. The sensor reports back the current status of the pipeline with additional information such as the last runtime and the last trigger.

### Service

The integration will create one service to execute a given pipeline. The service required the `pipeline_name` variable to run, and will use the same access keys provided in the config.

## Configuration

You will require a IAM user with access keys and an IAM policy to grant the user access to codepipeline (example policy to come.)

To configure this integration add the following to your `configuration.yaml` file:

```yaml
# Example configuration
aws_codepipeline:
  aws_access_key_id: your-access-key-id
  aws_secret_access_key: your-secret-access-key
  region_name: your pipeline region (default - us-east-1)
  pipeline_names:
    - test-pipeline-1
    - test-pipeline-2
```

You should store your access keys using the `secrets.yaml` file.
