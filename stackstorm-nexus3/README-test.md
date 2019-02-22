## Testing locally


Copy component files
    
    cp -rf actions/*  /opt/stackstorm/packs/nexus3/actions/

If any *.yaml file is changed, run reload accordingly.

    st2ctl reload --register-configs
    st2ctl reload --register-actions
    st2ctl reload --register-rules


trigger Execution
  
  List Repository:
  
    ST2_ACTION_CMD='st2 action execute nexus3.list_repositories config_profile=dev'

  Create  Repository

    ST2_ACTION_CMD='st2 action execute nexus3.create_repositories config_profile=dev type=hosted name=maven2-dumy format=maven write_policy=ALLOW'

  Get Repository

    ST2_ACTION_CMD='st2 action execute nexus3.get_repositories config_profile=dev name=maven2-dumy'

  Delete Repository

    ST2_ACTION_CMD='st2 action execute nexus3.delete_repositories config_profile=dev name=maven2-dumy'

  List Scripts:
  
    ST2_ACTION_CMD='st2 action execute nexus3.list_scripts config_profile=dev'

  Get scripts  

    ST2_ACTION_CMD='st2 action execute nexus3.get_scripts config_profile=dev name=nexus3-cli-repository-create'

  Delete Scripts

    ST2_ACTION_CMD='st2 action execute nexus3.delete_scripts config_profile=dev name=nexus3-cli-repository-delete'

  Excecute it:

    $ST2_ACTION_CMD | grep "execution get"  | xargs -0 -I{} bash -c "sleep 2; {}";

  Running them continuously:

    while true; do mkdir -p /opt/stackstorm/packs/nexus3; cp -rf ./*  /opt/stackstorm/packs/nexus3/; chmod -R --reference /opt/stackstorm/packs/linux /opt/stackstorm/packs/nexus3; chown -R --reference /opt/stackstorm/packs/linux/pack.yaml /opt/stackstorm/packs/nexus3/*; $ST2_ACTION_CMD | grep "execution get"  | xargs -0 -I{} bash -c "sleep 2; {}" sleep 2; done;



If any `yaml` file is updated , update it:

    #eg. updating action list_repositories.yaml
    st2 action update nexus3.list_repositories  ./actions/list_repositories.yaml

Get  executions

    st2 execution list  -n 1


``` json
{
  "success": true,
  "data": {
    "name": "dummy1",
    "type": "hosted",
    "format": "maven2",
    "recipe": "maven2-hosted",
    "online": true,
    "attributes": {
      "cleanup": {
        "policyName": "None"
      },
      "maven": {
        "versionPolicy": "RELEASE",
        "layoutPolicy": "STRICT"
      },
      "storage": {
        "strictContentTypeValidation": true,
        "writePolicy": "ALLOW_ONCE",
        "blobStoreName": "default"
      }
    },
    "url": "http://localhost:8081/repository/dummy1/",
    "status": {
      "repositoryName": "dummy1",
      "online": true,
      "description": null,
      "reason": null
    }
  }
}
``