# O Must Gather (omg) v2 (WORK IN PROGRESS)

With the previous (v1) implementation of omg, there were some major limitations. A major restructuring is being done to implement some advance features that are necessary, for example:

- **Multi directory support**:  Often times a single must-gather is not enough to capture all the components that are being investigated hence multiple must-gathers (or combination of must-gathes and oc-adm-inspect) are collected. omg needs to be able to look at them at once (using v1 omg we have to switch to these directories individually, which is very inconvenient).

- **Dynamic CRDs**: The CRDs in OpenShift are huge in number and growing. In the current implementation of omg, every CRD needs to be "handled" manually for omg to recoginze it. A [resource map](https://github.com/kxr/o-must-gather/blob/172f84afc2b81ab523edf78eb6d4a0e64d34cd32/omg/common/resource_map.py#L62-L625) to handle each CRD is hard to scale and fails to pick any new/undefined CRDs. In the newer implementation, CRDs will be automatically detected and recognized. This idea was orignally pitched by Robert Bost [here](https://github.com/kxr/o-must-gather/issues/34).

- **API Groups**: Handling API Groups for each CRD is important. For example to differentiate between `oc get config.operator` and `oc get config.imageregistry`.

- **Components Output**: Provide an easy way to see outputs of other components like elasticsearch and ceph when component specific must-gathers are collected (ODF, Logging, CNV, etc.)

- **High Level Summary**: A high level summary of a must-gather would be very useful. For exmaple `omg show summary` and `omg show issues`. 

- **Console Logging**: A proper console logging library [loguru](https://github.com/Delgan/loguru) is being used that supports standard/debug output and can separate standard and error outputs.

