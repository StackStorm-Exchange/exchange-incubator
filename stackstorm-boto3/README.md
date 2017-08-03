# boto3 integration pack

The StackStorm boto3 integration pack provides action integration with boto3.

# Configuration

Make sure you system is configured to use boto3, no configuration necessary for Stackstorm pack. For more information on boto3 configuration follow this link,

http://boto3.readthedocs.io/en/latest/guide/configuration.html

# Usage

```
st2 run boto3.action service="ec2" action_name="describe_vpcs" region="us-west-1"
```

## Action with arguments

```
st2 run boto3.action service="ec2" region="us-west-1"  action_name="create_vpc" params='{"CidrBlock": "10.0.0.0/16"}'
```
