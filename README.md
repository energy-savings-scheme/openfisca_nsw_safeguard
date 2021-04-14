# Openfisca Extension: NSW Energy Security Safeguard

This is an openfisca extension to openfisca_nsw_base package. It contains the coded rulesets for the **Energy Savings Scheme (ESS)** and the **Peak Demand Reduction Scheme**

## Initialising
You'll need to rename the openfisca_nsw_extension_template directory to the name
of your extension. Also edit README.md, MANIFEST.in, setup.py & Makefile, and replace $EXT_NAME with the
name of your extension. Replace $SHORT_NAME with a shortened name for it, for example
openfisca-nsw-rules-kids-vouchers is shortened to "kids". This just makes it easier to
switch to the virtual env.


## Installing

> We recommend that you use a virtualevn to install OpenFisca. If you don't,
you may need to add `--user` at the end of all commands starting by `pip`.

```sh
python3 -m venv $SHORT_NAME
deactive
source $SHORT_NAME/bin/activate

```
To install your extension, run:

```sh
make install
```

## Testing

You can make sure that everything is working by running the provided tests:

```sh
make test
```

To add your extension to the NSW API, update the openfisca-nsw-API repo's makefile with your
extension's name, and add your extension as a dependency.

> [Learn more about tests](http://openfisca.org/doc/coding-the-legislation/writing_yaml_tests.html).

Your extension package is now installed and ready!
