# O Must Gather (omg)

oc like tool that works with must-gather rather than OpenShift API


# Installation

Simply run:

    $ pip3 install o-must-gather --user

The omg binary is installed at ~/.local/bin, if it is not on your $PATH, create a symlink:

    $ ln -s ~/.local/bin ~/bin


# Usage

Point it to an extracted must-gather:

    $ omg use </path/to/must-gather/>

Use it like oc:

    # omg get clusterVersion
    # omg get clusterOperators
    # omg project openshift-ingress
    # omg get pods -o wide
