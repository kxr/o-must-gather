# O Must Gather (omg)

oc like tool that works with must-gather rather than OpenShift API

![GitHub release (latest by date)](https://img.shields.io/github/v/release/kxr/o-must-gather)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/o-must-gather)
![GitHub](https://img.shields.io/github/license/kxr/o-must-gather?color=blue)


## Installation

Simply run:

    $ pip3 install o-must-gather --user


## Usage

Point it to an extracted must-gather:

    $ omg use </path/to/must-gather/>

Use it like oc:

    # omg get clusterVersion
    # omg get clusterOperators
    # omg project openshift-ingress
    # omg get pods -o wide


## Development and Contribution

Contributions are most welcomed. Please refer [here](./CONTRIBUTING.md) for instructions on setting up development environment and learning more about the internal architecture of o-must-gather.

This project is licensed under GPLv3.
