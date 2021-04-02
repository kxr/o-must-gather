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


## Additional Features

### Shell Autocompletion

- `omg` has shell autocompletion (huge thanks to @bostrt). It can auto complete both, the commands (e.g, `get`, `project` etc.) and the objects present in the selected must-gather. Currently autocompletion is only available for `bash` shell however the support for `zsh` and `fish` shells should come soon.

  You can enable the autocompletion functionality in a bash shell by running:
  
        # eval "$(omg completion bash)"
        
  To make it permanent, append this line to `~/.bashrc` (if installed on system level) or to the activation script (if installed in venv):
  
        # If installed on system level
        # echo 'eval "$(omg completion bash)"' >> ~/.bashrc
        
        # If installed in a venv
        # echo 'eval "$(omg completion bash)"' >> /path/to/vevn/bin/activate

### `omg use`

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

### `omg machine-config`

This feature assist you in exploring the MachineConfigs in a more human-friendly way. You can use it in the following two ways:

- `omg machine-config extract [MachineConfig1 MachineConfig2 ...]`

    This will "extract" the MachineConfigs and place them under `<must-gather>/extracted-machine-configs`. The encoded files are decoded so they can be examined in a better way. If no MachineConfigs are passed (e.g, you simply run `omg machine-config extract`), all the MachineConfigs are extracted. Example usage:

    - Extract all MachineConfigs

            # omg machine-config extract

    - Extract specific MachineConfig

            # omg machine-config extract rendered-worker-261eed0b6fe6793c8b609de8e77958fa

- `omg machine-config compare MachineConfig1 MachineConfig2 [--show-contents]`

    This allows you to compare two MachineConfigs. It will list all the changes, addition and deletion in the two MachineConfigs. If `--show-contents` is passed it will show the `diff` between the contents as well (diff will be on deocded content if the content is encoded). Example usage:

    - Compare two MachineConfigs on a high level

            # omg machine-config compare rendered-worker-261eed0b6fe6793c8b609de8e77958fa rendered-worker-f9020f5c66ce72eee5f02a58b3c816c5

    - Compare two MachineConfigs with while also showing the diff of changed content

            # omg machine-config compare rendered-worker-261eed0b6fe6793c8b609de8e77958fa rendered-worker-f9020f5c66ce72eee5f02a58b3c816c5 --show-contents



## Development and Contribution

Contributions are most welcomed. Please refer [here](./CONTRIBUTING.md) for instructions on setting up development environment and learning more about the internal architecture of o-must-gather.

This project is licensed under GPLv3.
