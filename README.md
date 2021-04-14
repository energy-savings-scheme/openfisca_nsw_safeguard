# Openfisca Extension: NSW Energy Security Safeguard

This is an openfisca extension to openfisca_nsw_base package. It contains the coded rulesets for the **Energy Savings Scheme (ESS)** and the **Peak Demand Reduction Scheme (PDRS)**


## Installing

> We recommend that you use a virtualenv to install OpenFisca. If you don't,
you may need to add `--user` at the end of all commands starting by `pip`.

```sh
python3 -m venv $SHORT_NAME
deactive
source $SHORT_NAME/bin/activate

```
To install, run:

```sh
make install
```

## Testing

You can make sure that everything is working by running the provided tests:

```sh
make test
```
