# Reviewboard Integration Pack

This is a stackstorm pack for reviewboard tools. This pack consists of a sample reviewboard sensor and update_review actions.

## Installation

Then install this pack with: `st2 pack install reviewboard`

## Configuration

Copy the example configuration in [reviewboard.yaml.example](./reviewboard.yaml.example)
to `/opt/stackstorm/configs/reviewboard.yaml` and edit as required.

* ``url`` - URL of the Reviewboard instance (e.g. ``https://codereviews.example.tld``)
* ``poll_interval`` - Polling interval - default 30s
* ``verify`` - Verify SSL certificates. Default True. Set to False to disable verification
* ``auth_method`` - Specify either `basic` or `token` authentication

Include the following settings when using the `token` auth_method:
* ``api_token`` - API token

Include the following settings when using the `basic` auth_method:
* ``username`` - Username
* ``password`` - Password

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Sensors

### ReviewBoardSensor

The sensor monitors for new reviews  and sends a trigger into the system whenever there is a new codereview.

## Actions

* ``update_review`` - Action which updates the fields in a review and optionally publishes the review.
* ``update_review_status`` - Action which updates the status to close - submitted, close - discarded states or reopen the review..

