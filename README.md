# Openfisca Extension: NSW Energy Security Safeguard

This is an openfisca extension to openfisca_nsw_base package. It contains the coded rulesets for the **Energy Savings Scheme (ESS)** and the **Peak Demand Reduction Scheme (PDRS)**

## Prerequisite
- Docker

## Build
Need to run command below to build the project for the first time or whenever adding new custom variable
```sh
docker-compose up --build -d
```

Otherwise, we can just run command below to serve the OpenFisca API
```sh
docker-compose up -d
```

## Testing
You can make sure that everything is working by running the provided tests. 
We can run the test from inside of the container.
```sh
docker exec -it <container_name> /bin/bash # this to go to inside container
# Run the test command
make test
```

Or we can also run the test from local / outside the container
```sh
docker exec <container_name> make test
```

_Important Note_
__*Make sure to always running the test whenever adding new changes, to make sure everything is working as expected.*__
