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


#### omg use

- When run without any arguments i.e, just `omg use`, omg will show you the details of the currently selected must-gather. For example:

        # omg use ./must-gather.local.2723199189299891619
        Now using project "openshift-monitoring" on must-gather "/home/knaeem/Downloads/must-gather.local.2723199189299891619/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-d7c882054a4528eda72e69a7988c5931b5a1643913b11bfd2575a78a8620808f"
    
        # omg use
        Current must-gather: /home/knaeem/Downloads/must-gather.local.2723199189299891619/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-d7c882054a4528eda72e69a7988c5931b5a1643913b11bfd2575a78a8620808f
            Current Project: openshift-monitoring
            Cluster API URL: ['https://api.ocp4.aidemo.local:6443']
           Cluster Platform: ['oVirt']

- To facilitate users working with multiple must-gathers, you can now set the current working directory to be used as the must-gather path. In this case, simply switching the current working directory to the desired must-gather will be enough to start using that must-gather. To use this mode, simply run `omg use --cwd`. For example:

        # omg use --cwd
        Using your current working directory

        # cd /home/knaeem/Downloads/must-gather.local.2723199189299891619/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-d7c882054a4528eda72e69a7988c5931b5a1643913b11bfd2575a78a8620808f

        # omg use
        Current must-gather: .
            Current Project: openshift-monitoring
            Cluster API URL: ['https://api.ocp4.aidemo.local:6443']
           Cluster Platform: ['oVirt']

        # cd /home/knaeem/Downloads/must-gather.local.7890185621691109993/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-549bd48582a9fa615b8728bc6e1d66f3a9c829f415d9ddd58f95eb978be50274

        # omg use
        Current must-gather: .
            Current Project: openshift-monitoring
            Cluster API URL: ['https://api.ocpprod.example.com:6443']
           Cluster Platform: ['None']




## Development and Contribution

Contributions are most welcomed. Please refer [here](./CONTRIBUTING.md) for instructions on setting up development environment and learning more about the internal architecture of o-must-gather.

This project is licensed under GPLv3.
