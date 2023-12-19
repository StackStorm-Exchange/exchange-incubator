# stackstorm-azuredevops
This Package allow to List and Run Ado Pipelines.

# Introduction
This Plugin allow to interact with Azure Devops.
You can
  - list Pipelines
  - run Pipelines
  - Remove branches
  - list Repositories


# Auth
You can using 1 Auth Mode.
1) Personal Acces Token (Pat)
   https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows#create-a-pat

# listPipeline:
List all Pipeline in a Project.
So you can get here the Pipeline ID for the runPipeline action.

## Parameter Explanation:

| Parameter        | Description  | Example  |
| ------------- |:-------------:| -----:|
| org      | AzureDevops ORG   |   schwarzit/schwarzit-wiking |
| project | AzureDevops projectname |  schwarzit.groot-exchange  |
| accesstoken | Access Token Azure Devops |    ********** |


# runPipeline:
Run a Ado Pipeline. You can select your Branche/Tag and your Parameters as JSON string.

## Parameter Explanation:

| Parameter        | Description  | Example  |
| ------------- |:-------------:| -----:|
| pipelineId      | AzureDevops Pipeline ID (You can use the ListPipeline Action to get your Pipeline ID) | 12345678 |
| org      | AzureDevops ORG   |   schwarzit/schwarzit-wiking |
| project | AzureDevops projectname |   schwarzit.groot-exchange |
| accesstoken | Access Token Azure Devops |    ********** |
| refName | RefName of Branche or Tag |  refs/heads/main |
| templateParameters | Parameter Array |  {"key1": "value2", "key2": "value2"} |

# housekeeping_repo_branches:
Removing Branches in your Azure DevOps Repository.

## Parameter Explanation:

| Parameter        | Description  | Example  |
| ------------- |:-------------:| -----:|
| org      | Azure DevOps Organisation   |   schwarzit/schwarzit-wiking |
| project | Azure DevOps Projectname |   schwarzit.groot-exchange |
| repository | Azure DevOps repository name |    st2_aap |
| accesstoken | Personal Access Token |  ************************** |
| filter | Branches to be excluded from housekeeping |  main|tags|dev |
| retention | Maximum days to retain the branches |  30 |

# list_repos:
Get all Repositories in an Azure DevOps project as JSON

## Parameter Explanation:

| Parameter        | Description  | Example  |
| ------------- |:-------------:| -----:|
| org      | Azure DevOps Organisation   |   schwarzit/schwarzit-wiking |
| project | Azure DevOps Projectname |   schwarzit.groot-exchange |
| accesstoken | Personal Access Token |  ************************** |
