# Openfisca Extension: NSW Energy Security Safeguard

This is an openfisca extension to openfisca_nsw_base package. It contains the coded rulesets for the **Energy Savings Scheme (ESS)** and the **Peak Demand Reduction Scheme (PDRS)**

## Prerequisite
- Docker - [Installation Guide](https://docs.docker.com/engine/install/)
- Docker Compose - [Installation Guide](https://docs.docker.com/compose/install/)

## How to Run

### Build the Application
```sh
docker-compose up --build -d
```

### Run the Application
```sh
docker-compose up -d
```

## Testing
You can make sure that everything is working by running the provided tests. 
```sh
docker-compose run app make test
```

_Important Note_
__*Make sure to always running the test whenever adding new changes, to make sure everything is working as expected.*__


## Deployment

For deployment, it all happening through CI/CD in Github workflow.
All workflows defined in *.github/workflows/*.
