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

* `project.list` - Returns a list of gitlab projects

### Pipelines

* `project.pipelines.list` - List all pipelines in a project
* `project.pipelines.run` - Create a new Pipeline

### Artifacts

* `artifact.unzip` - Download the latest artifact and unzip it

## Dependencies

### packs

* [tools](https://github.com/nullkarma/stackstorm-tools) - used by `artifact.unzip` workflow.

Since `artifact.unzip` is a workflow build from a 3rd party pack,
it won't be able to read `url` and `token` from your `gitlab.yaml` config.
