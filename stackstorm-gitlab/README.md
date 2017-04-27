# Gitlab Integration Pack

Gitlab API v4 supported.

## Configuraton

```yaml
url: http://gitlab.example.com
token: private-token
verify_ssl: False
```

## Actions

### Projects

* `project.info` - Returns project information

### Pipelines

* `pipeline.list` - List all pipelines in a project
* `pipeline.trigger` - Create a new pipeline

### Artifacts

* `artifact.unzip` - Download the latest artifact and unzip it

depends on tools pack
