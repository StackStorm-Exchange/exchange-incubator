# Stackstorm Keycloak Pack

Pack built on python-keycloak module

# Current Status & Capabilities
Runs keycloak admin operations:
  - getters for user, client and role
  - create/delete user
  - create client
  - create role
  - assign client role to user

# Roadmap
Features to add:
  - client create/delete
  - ID Provider operations
  - SMTP config
  - Realm config

## Configuration

configs/keycloak.yaml defines connection and authentication parameters for target keycloak instance.
