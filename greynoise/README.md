[![main](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/workflows/Build/badge.svg)](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/actions?query=workflow%3ABuild)
[![main](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/workflows/YAML%20Lint/badge.svg)](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/actions/workflows/yamllint.yaml?query=workflow%3AYAML+Lint)
[![main](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/workflows/python_linters/badge.svg)](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/actions?query=workflow%3Apython_linters)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# GreyNoise Stackstorm Pack

The GreyNoise Stackstorm (ST2) Pack provides a set of actions to be run in ST2 that interact with the GreyNoise API.

## Usage 
This integration reqires and API key for the GreyNoise API.  If you don't have one, sign up for a free trial at
[https://viz.greynoise.io/signup](https://viz.greynoise.io/signup)

To configure the integration, add your GN API Key to the keystore using:

`st2 key set gn_api_key <api_key> -e`

Then configure the pack using:

`st2 pack config greynoise`


Includes the following actions:
* Lookup IP in GreyNoise Context API
* Lookup IP in GreyNoise Quick API
* Lookup IP in GreyNoise RIOT API
* Perform a GreyNoise Query (GNQL)

Includes the following Orchestra workflows:
* Combines Quick, Context and RIOT lookups

 ## Contributing

Please read [CONTRIBUTING.md](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/tags).

## Authors

* **Brad Chiappetta** - *Initial work* - [bradchiappetta](https://github.com/bradchiappetta)

See also the list of [contributors](https://github.com/GreyNoise-Intelligence/greynoise-stackstorm/contributors) who participated in this project.

## Acknowledgments

* Thanks to the StackStorm team for their help in reviewing and releasing this pack


## Links

* [GreyNoise.io](https://greynoise.io)
* [GreyNoise Terms](https://greynoise.io/terms)
* [GreyNoise Developer Portal](https://developer.greynoise.io)

## Contact Us

Have any questions or comments about GreyNoise?  Contact us at [hello@greynoise.io](mailto:hello@greynoise.io)

## Copyright and License

Code released under [MIT License](LICENSE).

