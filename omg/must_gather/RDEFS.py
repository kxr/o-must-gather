# Built-in Resource Definitions (rdefs)
RDEFS = [
    {
        "kind": "Binding",
        "singular": "binding",
        "plural": "bindings",
        "scope": "Namespaced",
        "group": "core"
    },
    {
        "kind": "ComponentStatus",
        "singular": "componentstatuse",
        "plural": "componentstatuses",
        "scope": "Cluster",
        "shortNames": ["cs"],
        "group": "core"
    },
    {
        "kind": "ConfigMap",
        "singular": "configmap",
        "plural": "configmaps",
        "scope": "Namespaced",
        "shortNames": ["cm"],
        "group": "core"
    },
    {
        "kind": "Endpoints",
        "singular": "endpoint",
        "plural": "endpoints",
        "scope": "Namespaced",
        "shortNames": ["ep"],
        "group": "core"
    },
    {
        "kind": "Event",
        "singular": "event",
        "plural": "events",
        "scope": "Namespaced",
        "shortNames": ["ev"],
        "group": "core"
    },
    {
        "kind": "LimitRange",
        "singular": "limitrange",
        "plural": "limitranges",
        "scope": "Namespaced",
        "shortNames": ["limits"],
        "group": "core"
    },
    {
        "kind": "Namespace",
        "singular": "namespace",
        "plural": "namespaces",
        "scope": "Cluster",
        "shortNames": ["ns"],
        "group": "core"
    },
    {
        "kind": "Node",
        "singular": "node",
        "plural": "nodes",
        "scope": "Cluster",
        "shortNames": ["no"],
        "group": "core"
    },
    {
        "kind": "PersistentVolumeClaim",
        "singular": "persistentvolumeclaim",
        "plural": "persistentvolumeclaims",
        "scope": "Namespaced",
        "shortNames": ["pvc"],
        "group": "core"
    },
    {
        "kind": "PersistentVolume",
        "singular": "persistentvolume",
        "plural": "persistentvolumes",
        "scope": "Cluster",
        "shortNames": ["pv"],
        "group": "core"
    },
    {
        "kind": "Pod",
        "singular": "pod",
        "plural": "pods",
        "scope": "Namespaced",
        "shortNames": ["po"],
        "group": "core"
    },
    {
        "kind": "PodTemplate",
        "singular": "podtemplate",
        "plural": "podtemplates",
        "scope": "Namespaced",
        "group": "core"
    },
    {
        "kind": "ReplicationController",
        "singular": "replicationcontroller",
        "plural": "replicationcontrollers",
        "scope": "Namespaced",
        "shortNames": ["rc"],
        "group": "core"
    },
    {
        "kind": "ResourceQuota",
        "singular": "resourcequota",
        "plural": "resourcequotas",
        "scope": "Namespaced",
        "shortNames": ["quota"],
        "group": "core"
    },
    {
        "kind": "Secret",
        "singular": "secret",
        "plural": "secrets",
        "scope": "Namespaced",
        "group": "core"
    },
    {
        "kind": "ServiceAccount",
        "singular": "serviceaccount",
        "plural": "serviceaccounts",
        "scope": "Namespaced",
        "shortNames": ["sa"],
        "group": "core"
    },
    {
        "kind": "Service",
        "singular": "service",
        "plural": "services",
        "scope": "Namespaced",
        "shortNames": ["svc"],
        "group": "core"
    },
    {
        "kind": "MutatingWebhookConfiguration",
        "singular": "mutatingwebhookconfiguration",
        "plural": "mutatingwebhookconfigurations",
        "scope": "Cluster",
        "group": "admissionregistration.k8s.io"
    },
    {
        "kind": "ValidatingWebhookConfiguration",
        "singular": "validatingwebhookconfiguration",
        "plural": "validatingwebhookconfigurations",
        "scope": "Cluster",
        "group": "admissionregistration.k8s.io"
    },
    {
        "kind": "CustomResourceDefinition",
        "singular": "customresourcedefinition",
        "plural": "customresourcedefinitions",
        "scope": "Cluster",
        "shortNames": ["crd", "crds"],
        "group": "apiextensions.k8s.io"
    },
    {
        "kind": "APIService",
        "singular": "apiservice",
        "plural": "apiservices",
        "scope": "Cluster",
        "group": "apiregistration.k8s.io"
    },
    {
        "kind": "APIRequestCount",
        "singular": "apirequestcount",
        "plural": "apirequestcounts",
        "scope": "Cluster",
        "group": "apiserver.openshift.io"
    },
    {
        "kind": "ControllerRevision",
        "singular": "controllerrevision",
        "plural": "controllerrevisions",
        "scope": "Namespaced",
        "group": "apps"
    },
    {
        "kind": "DaemonSet",
        "singular": "daemonset",
        "plural": "daemonsets",
        "scope": "Namespaced",
        "shortNames": ["ds"],
        "group": "apps"
    },
    {
        "kind": "Deployment",
        "singular": "deployment",
        "plural": "deployments",
        "scope": "Namespaced",
        "shortNames": ["deploy"],
        "group": "apps"
    },
    {
        "kind": "ReplicaSet",
        "singular": "replicaset",
        "plural": "replicasets",
        "scope": "Namespaced",
        "shortNames": ["rs"],
        "group": "apps"
    },
    {
        "kind": "StatefulSet",
        "singular": "statefulset",
        "plural": "statefulsets",
        "scope": "Namespaced",
        "shortNames": ["sts"],
        "group": "apps"
    },
    {
        "kind": "DeploymentConfig",
        "singular": "deploymentconfig",
        "plural": "deploymentconfigs",
        "scope": "Namespaced",
        "shortNames": ["dc"],
        "group": "apps.openshift.io"
    },
    {
        "kind": "TokenReview",
        "singular": "tokenreview",
        "plural": "tokenreviews",
        "scope": "Cluster",
        "group": "authentication.k8s.io"
    },
    {
        "kind": "LocalSubjectAccessReview",
        "singular": "localsubjectaccessreview",
        "plural": "localsubjectaccessreviews",
        "scope": "Namespaced",
        "group": "authorization.k8s.io"
    },
    {
        "kind": "SelfSubjectAccessReview",
        "singular": "selfsubjectaccessreview",
        "plural": "selfsubjectaccessreviews",
        "scope": "Cluster",
        "group": "authorization.k8s.io"
    },
    {
        "kind": "SelfSubjectRulesReview",
        "singular": "selfsubjectrulesreview",
        "plural": "selfsubjectrulesreviews",
        "scope": "Cluster",
        "group": "authorization.k8s.io"
    },
    {
        "kind": "SubjectAccessReview",
        "singular": "subjectaccessreview",
        "plural": "subjectaccessreviews",
        "scope": "Cluster",
        "group": "authorization.k8s.io"
    },
    {
        "kind": "ClusterRoleBinding",
        "singular": "clusterrolebinding",
        "plural": "clusterrolebindings",
        "scope": "Cluster",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "ClusterRole",
        "singular": "clusterrole",
        "plural": "clusterroles",
        "scope": "Cluster",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "LocalResourceAccessReview",
        "singular": "localresourceaccessreview",
        "plural": "localresourceaccessreviews",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "LocalSubjectAccessReview",
        "singular": "localsubjectaccessreview",
        "plural": "localsubjectaccessreviews",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "ResourceAccessReview",
        "singular": "resourceaccessreview",
        "plural": "resourceaccessreviews",
        "scope": "Cluster",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "RoleBindingRestriction",
        "singular": "rolebindingrestriction",
        "plural": "rolebindingrestrictions",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "RoleBinding",
        "singular": "rolebinding",
        "plural": "rolebindings",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "Role",
        "singular": "role",
        "plural": "roles",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "SelfSubjectRulesReview",
        "singular": "selfsubjectrulesreview",
        "plural": "selfsubjectrulesreviews",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "SubjectAccessReview",
        "singular": "subjectaccessreview",
        "plural": "subjectaccessreviews",
        "scope": "Cluster",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "SubjectRulesReview",
        "singular": "subjectrulesreview",
        "plural": "subjectrulesreviews",
        "scope": "Namespaced",
        "group": "authorization.openshift.io"
    },
    {
        "kind": "HorizontalPodAutoscaler",
        "singular": "horizontalpodautoscaler",
        "plural": "horizontalpodautoscalers",
        "scope": "Namespaced",
        "shortNames": ["hpa"],
        "group": "autoscaling"
    },
    {
        "kind": "ClusterAutoscaler",
        "singular": "clusterautoscaler",
        "plural": "clusterautoscalers",
        "scope": "Cluster",
        "shortNames": ["ca"],
        "group": "autoscaling.openshift.io"
    },
    {
        "kind": "MachineAutoscaler",
        "singular": "machineautoscaler",
        "plural": "machineautoscalers",
        "scope": "Namespaced",
        "shortNames": ["ma"],
        "group": "autoscaling.openshift.io"
    },
    {
        "kind": "CronJob",
        "singular": "cronjob",
        "plural": "cronjobs",
        "scope": "Namespaced",
        "shortNames": ["cj"],
        "group": "batch"
    },
    {
        "kind": "Job",
        "singular": "job",
        "plural": "jobs",
        "scope": "Namespaced",
        "group": "batch"
    },
    {
        "kind": "BuildConfig",
        "singular": "buildconfig",
        "plural": "buildconfigs",
        "scope": "Namespaced",
        "shortNames": ["bc"],
        "group": "build.openshift.io"
    },
    {
        "kind": "Build",
        "singular": "build",
        "plural": "builds",
        "scope": "Namespaced",
        "group": "build.openshift.io"
    },
    {
        "kind": "CertificateSigningRequest",
        "singular": "certificatesigningrequest",
        "plural": "certificatesigningrequests",
        "scope": "Cluster",
        "shortNames": ["csr"],
        "group": "certificates.k8s.io"
    },
    {
        "kind": "CredentialsRequest",
        "singular": "credentialsrequest",
        "plural": "credentialsrequests",
        "scope": "Namespaced",
        "group": "cloudcredential.openshift.io"
    },
    {
        "kind": "APIServer",
        "singular": "apiserver",
        "plural": "apiservers",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Authentication",
        "singular": "authentication",
        "plural": "authentications",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Build",
        "singular": "build",
        "plural": "builds",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "ClusterOperator",
        "singular": "clusteroperator",
        "plural": "clusteroperators",
        "scope": "Cluster",
        "shortNames": ["co"],
        "group": "config.openshift.io"
    },
    {
        "kind": "ClusterVersion",
        "singular": "clusterversion",
        "plural": "clusterversions",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Console",
        "singular": "console",
        "plural": "consoles",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "DNS",
        "singular": "dnse",
        "plural": "dnses",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "FeatureGate",
        "singular": "featuregate",
        "plural": "featuregates",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Image",
        "singular": "image",
        "plural": "images",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Infrastructure",
        "singular": "infrastructure",
        "plural": "infrastructures",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Ingress",
        "singular": "ingresse",
        "plural": "ingresses",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Network",
        "singular": "network",
        "plural": "networks",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "OAuth",
        "singular": "oauth",
        "plural": "oauths",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "OperatorHub",
        "singular": "operatorhub",
        "plural": "operatorhubs",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Project",
        "singular": "project",
        "plural": "projects",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Proxy",
        "singular": "proxie",
        "plural": "proxies",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "Scheduler",
        "singular": "scheduler",
        "plural": "schedulers",
        "scope": "Cluster",
        "group": "config.openshift.io"
    },
    {
        "kind": "ConsoleCLIDownload",
        "singular": "consoleclidownload",
        "plural": "consoleclidownloads",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsoleExternalLogLink",
        "singular": "consoleexternalloglink",
        "plural": "consoleexternalloglinks",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsoleLink",
        "singular": "consolelink",
        "plural": "consolelinks",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsoleNotification",
        "singular": "consolenotification",
        "plural": "consolenotifications",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsolePlugin",
        "singular": "consoleplugin",
        "plural": "consoleplugins",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsoleQuickStart",
        "singular": "consolequickstart",
        "plural": "consolequickstarts",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "ConsoleYAMLSample",
        "singular": "consoleyamlsample",
        "plural": "consoleyamlsamples",
        "scope": "Cluster",
        "group": "console.openshift.io"
    },
    {
        "kind": "PodNetworkConnectivityCheck",
        "singular": "podnetworkconnectivitycheck",
        "plural": "podnetworkconnectivitychecks",
        "scope": "Namespaced",
        "group": "controlplane.operator.openshift.io"
    },
    {
        "kind": "Lease",
        "singular": "lease",
        "plural": "leases",
        "scope": "Namespaced",
        "group": "coordination.k8s.io"
    },
    {
        "kind": "EndpointSlice",
        "singular": "endpointslice",
        "plural": "endpointslices",
        "scope": "Namespaced",
        "group": "discovery.k8s.io"
    },
    {
        "kind": "Event",
        "singular": "event",
        "plural": "events",
        "scope": "Namespaced",
        "shortNames": ["ev"],
        "group": "events.k8s.io"
    },
    {
        "kind": "Ingress",
        "singular": "ingresse",
        "plural": "ingresses",
        "scope": "Namespaced",
        "shortNames": ["ing"],
        "group": "extensions"
    },
    {
        "kind": "FlowSchema",
        "singular": "flowschema",
        "plural": "flowschemas",
        "scope": "Cluster",
        "group": "flowcontrol.apiserver.k8s.io"
    },
    {
        "kind": "PriorityLevelConfiguration",
        "singular": "prioritylevelconfiguration",
        "plural": "prioritylevelconfigurations",
        "scope": "Cluster",
        "group": "flowcontrol.apiserver.k8s.io"
    },
    {
        "kind": "HelmChartRepository",
        "singular": "helmchartrepositorie",
        "plural": "helmchartrepositories",
        "scope": "Cluster",
        "group": "helm.openshift.io"
    },
    {
        "kind": "Image",
        "singular": "image",
        "plural": "images",
        "scope": "Cluster",
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageSignature",
        "singular": "imagesignature",
        "plural": "imagesignatures",
        "scope": "Cluster",
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageStreamImage",
        "singular": "imagestreamimage",
        "plural": "imagestreamimages",
        "scope": "Namespaced",
        "shortNames": ["isimage"],
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageStreamImport",
        "singular": "imagestreamimport",
        "plural": "imagestreamimports",
        "scope": "Namespaced",
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageStreamMapping",
        "singular": "imagestreammapping",
        "plural": "imagestreammappings",
        "scope": "Namespaced",
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageStream",
        "singular": "imagestream",
        "plural": "imagestreams",
        "scope": "Namespaced",
        "shortNames": ["is"],
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageStreamTag",
        "singular": "imagestreamtag",
        "plural": "imagestreamtags",
        "scope": "Namespaced",
        "shortNames": ["istag"],
        "group": "image.openshift.io"
    },
    {
        "kind": "ImageTag",
        "singular": "imagetag",
        "plural": "imagetags",
        "scope": "Namespaced",
        "shortNames": ["itag"],
        "group": "image.openshift.io"
    },
    {
        "kind": "Config",
        "singular": "config",
        "plural": "configs",
        "scope": "Cluster",
        "group": "imageregistry.operator.openshift.io"
    },
    {
        "kind": "ImagePruner",
        "singular": "imagepruner",
        "plural": "imagepruners",
        "scope": "Cluster",
        "group": "imageregistry.operator.openshift.io"
    },
    {
        "kind": "DNSRecord",
        "singular": "dnsrecord",
        "plural": "dnsrecords",
        "scope": "Namespaced",
        "group": "ingress.operator.openshift.io"
    },
    {
        "kind": "NetworkAttachmentDefinition",
        "singular": "network-attachment-definition",
        "plural": "network-attachment-definitions",
        "scope": "Namespaced",
        "shortNames": ["net-attach-def"],
        "group": "k8s.cni.cncf.io"
    },
    {
        "kind": "MachineHealthCheck",
        "singular": "machinehealthcheck",
        "plural": "machinehealthchecks",
        "scope": "Namespaced",
        "shortNames": ["mhc", "mhcs"],
        "group": "machine.openshift.io"
    },
    {
        "kind": "Machine",
        "singular": "machine",
        "plural": "machines",
        "scope": "Namespaced",
        "group": "machine.openshift.io"
    },
    {
        "kind": "MachineSet",
        "singular": "machineset",
        "plural": "machinesets",
        "scope": "Namespaced",
        "group": "machine.openshift.io"
    },
    {
        "kind": "ContainerRuntimeConfig",
        "singular": "containerruntimeconfig",
        "plural": "containerruntimeconfigs",
        "scope": "Cluster",
        "shortNames": ["ctrcfg"],
        "group": "machineconfiguration.openshift.io"
    },
    {
        "kind": "ControllerConfig",
        "singular": "controllerconfig",
        "plural": "controllerconfigs",
        "scope": "Cluster",
        "group": "machineconfiguration.openshift.io"
    },
    {
        "kind": "KubeletConfig",
        "singular": "kubeletconfig",
        "plural": "kubeletconfigs",
        "scope": "Cluster",
        "group": "machineconfiguration.openshift.io"
    },
    {
        "kind": "MachineConfigPool",
        "singular": "machineconfigpool",
        "plural": "machineconfigpools",
        "scope": "Cluster",
        "shortNames": ["mcp"],
        "group": "machineconfiguration.openshift.io"
    },
    {
        "kind": "MachineConfig",
        "singular": "machineconfig",
        "plural": "machineconfigs",
        "scope": "Cluster",
        "shortNames": ["mc"],
        "group": "machineconfiguration.openshift.io"
    },
    {
        "kind": "BareMetalHost",
        "singular": "baremetalhost",
        "plural": "baremetalhosts",
        "scope": "Namespaced",
        "shortNames": ["bmh", "bmhost"],
        "group": "metal3.io"
    },
    {
        "kind": "Provisioning",
        "singular": "provisioning",
        "plural": "provisionings",
        "scope": "Cluster",
        "group": "metal3.io"
    },
    {
        "kind": "NodeMetrics",
        "singular": "node",
        "plural": "nodes",
        "scope": "Cluster",
        "group": "metrics.k8s.io"
    },
    {
        "kind": "PodMetrics",
        "singular": "pod",
        "plural": "pods",
        "scope": "Namespaced",
        "group": "metrics.k8s.io"
    },
    {
        "kind": "StorageState",
        "singular": "storagestate",
        "plural": "storagestates",
        "scope": "Cluster",
        "group": "migration.k8s.io"
    },
    {
        "kind": "StorageVersionMigration",
        "singular": "storageversionmigration",
        "plural": "storageversionmigrations",
        "scope": "Cluster",
        "group": "migration.k8s.io"
    },
    {
        "kind": "AlertmanagerConfig",
        "singular": "alertmanagerconfig",
        "plural": "alertmanagerconfigs",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "Alertmanager",
        "singular": "alertmanager",
        "plural": "alertmanagers",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "PodMonitor",
        "singular": "podmonitor",
        "plural": "podmonitors",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "Probe",
        "singular": "probe",
        "plural": "probes",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "Prometheus",
        "singular": "prometheuse",
        "plural": "prometheuses",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "PrometheusRule",
        "singular": "prometheusrule",
        "plural": "prometheusrules",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "ServiceMonitor",
        "singular": "servicemonitor",
        "plural": "servicemonitors",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "ThanosRuler",
        "singular": "thanosruler",
        "plural": "thanosrulers",
        "scope": "Namespaced",
        "group": "monitoring.coreos.com"
    },
    {
        "kind": "ClusterNetwork",
        "singular": "clusternetwork",
        "plural": "clusternetworks",
        "scope": "Cluster",
        "group": "network.openshift.io"
    },
    {
        "kind": "EgressNetworkPolicy",
        "singular": "egressnetworkpolicie",
        "plural": "egressnetworkpolicies",
        "scope": "Namespaced",
        "group": "network.openshift.io"
    },
    {
        "kind": "HostSubnet",
        "singular": "hostsubnet",
        "plural": "hostsubnets",
        "scope": "Cluster",
        "group": "network.openshift.io"
    },
    {
        "kind": "NetNamespace",
        "singular": "netnamespace",
        "plural": "netnamespaces",
        "scope": "Cluster",
        "group": "network.openshift.io"
    },
    {
        "kind": "EgressRouter",
        "singular": "egressrouter",
        "plural": "egressrouters",
        "scope": "Namespaced",
        "group": "network.operator.openshift.io"
    },
    {
        "kind": "OperatorPKI",
        "singular": "operatorpki",
        "plural": "operatorpkis",
        "scope": "Namespaced",
        "group": "network.operator.openshift.io"
    },
    {
        "kind": "IngressClass",
        "singular": "ingressclasse",
        "plural": "ingressclasses",
        "scope": "Cluster",
        "group": "networking.k8s.io"
    },
    {
        "kind": "Ingress",
        "singular": "ingresse",
        "plural": "ingresses",
        "scope": "Namespaced",
        "shortNames": ["ing"],
        "group": "networking.k8s.io"
    },
    {
        "kind": "NetworkPolicy",
        "singular": "networkpolicie",
        "plural": "networkpolicies",
        "scope": "Namespaced",
        "shortNames": ["netpol"],
        "group": "networking.k8s.io"
    },
    {
        "kind": "RuntimeClass",
        "singular": "runtimeclasse",
        "plural": "runtimeclasses",
        "scope": "Cluster",
        "group": "node.k8s.io"
    },
    {
        "kind": "OAuthAccessToken",
        "singular": "oauthaccesstoken",
        "plural": "oauthaccesstokens",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "OAuthAuthorizeToken",
        "singular": "oauthauthorizetoken",
        "plural": "oauthauthorizetokens",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "OAuthClientAuthorization",
        "singular": "oauthclientauthorization",
        "plural": "oauthclientauthorizations",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "OAuthClient",
        "singular": "oauthclient",
        "plural": "oauthclients",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "TokenReview",
        "singular": "tokenreview",
        "plural": "tokenreviews",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "UserOAuthAccessToken",
        "singular": "useroauthaccesstoken",
        "plural": "useroauthaccesstokens",
        "scope": "Cluster",
        "group": "oauth.openshift.io"
    },
    {
        "kind": "Authentication",
        "singular": "authentication",
        "plural": "authentications",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "CloudCredential",
        "singular": "cloudcredential",
        "plural": "cloudcredentials",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "ClusterCSIDriver",
        "singular": "clustercsidriver",
        "plural": "clustercsidrivers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "Config",
        "singular": "config",
        "plural": "configs",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "Console",
        "singular": "console",
        "plural": "consoles",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "CSISnapshotController",
        "singular": "csisnapshotcontroller",
        "plural": "csisnapshotcontrollers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "DNS",
        "singular": "dnse",
        "plural": "dnses",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "Etcd",
        "singular": "etcd",
        "plural": "etcds",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "ImageContentSourcePolicy",
        "singular": "imagecontentsourcepolicie",
        "plural": "imagecontentsourcepolicies",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "IngressController",
        "singular": "ingresscontroller",
        "plural": "ingresscontrollers",
        "scope": "Namespaced",
        "group": "operator.openshift.io"
    },
    {
        "kind": "KubeAPIServer",
        "singular": "kubeapiserver",
        "plural": "kubeapiservers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "KubeControllerManager",
        "singular": "kubecontrollermanager",
        "plural": "kubecontrollermanagers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "KubeScheduler",
        "singular": "kubescheduler",
        "plural": "kubeschedulers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "KubeStorageVersionMigrator",
        "singular": "kubestorageversionmigrator",
        "plural": "kubestorageversionmigrators",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "Network",
        "singular": "network",
        "plural": "networks",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "OpenShiftAPIServer",
        "singular": "openshiftapiserver",
        "plural": "openshiftapiservers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "OpenShiftControllerManager",
        "singular": "openshiftcontrollermanager",
        "plural": "openshiftcontrollermanagers",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "ServiceCA",
        "singular": "serviceca",
        "plural": "servicecas",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "Storage",
        "singular": "storage",
        "plural": "storages",
        "scope": "Cluster",
        "group": "operator.openshift.io"
    },
    {
        "kind": "CatalogSource",
        "singular": "catalogsource",
        "plural": "catalogsources",
        "scope": "Namespaced",
        "shortNames": ["catsrc"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "ClusterServiceVersion",
        "singular": "clusterserviceversion",
        "plural": "clusterserviceversions",
        "scope": "Namespaced",
        "shortNames": ["csv", "csvs"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "InstallPlan",
        "singular": "installplan",
        "plural": "installplans",
        "scope": "Namespaced",
        "shortNames": ["ip"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "OperatorCondition",
        "singular": "operatorcondition",
        "plural": "operatorconditions",
        "scope": "Namespaced",
        "shortNames": ["condition"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "OperatorGroup",
        "singular": "operatorgroup",
        "plural": "operatorgroups",
        "scope": "Namespaced",
        "shortNames": ["og"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "Operator",
        "singular": "operator",
        "plural": "operators",
        "scope": "Cluster",
        "group": "operators.coreos.com"
    },
    {
        "kind": "Subscription",
        "singular": "subscription",
        "plural": "subscriptions",
        "scope": "Namespaced",
        "shortNames": ["sub", "subs"],
        "group": "operators.coreos.com"
    },
    {
        "kind": "PackageManifest",
        "singular": "packagemanifest",
        "plural": "packagemanifests",
        "scope": "Namespaced",
        "group": "packages.operators.coreos.com"
    },
    {
        "kind": "PodDisruptionBudget",
        "singular": "poddisruptionbudget",
        "plural": "poddisruptionbudgets",
        "scope": "Namespaced",
        "shortNames": ["pdb"],
        "group": "policy"
    },
    {
        "kind": "PodSecurityPolicy",
        "singular": "podsecuritypolicie",
        "plural": "podsecuritypolicies",
        "scope": "Cluster",
        "shortNames": ["psp"],
        "group": "policy"
    },
    {
        "kind": "ProjectRequest",
        "singular": "projectrequest",
        "plural": "projectrequests",
        "scope": "Cluster",
        "group": "project.openshift.io"
    },
    {
        "kind": "Project",
        "singular": "project",
        "plural": "projects",
        "scope": "Cluster",
        "group": "project.openshift.io"
    },
    {
        "kind": "AppliedClusterResourceQuota",
        "singular": "appliedclusterresourcequota",
        "plural": "appliedclusterresourcequotas",
        "scope": "Namespaced",
        "group": "quota.openshift.io"
    },
    {
        "kind": "ClusterResourceQuota",
        "singular": "clusterresourcequota",
        "plural": "clusterresourcequotas",
        "scope": "Cluster",
        "shortNames": ["clusterquota"],
        "group": "quota.openshift.io"
    },
    {
        "kind": "ClusterRoleBinding",
        "singular": "clusterrolebinding",
        "plural": "clusterrolebindings",
        "scope": "Cluster",
        "group": "rbac.authorization.k8s.io"
    },
    {
        "kind": "ClusterRole",
        "singular": "clusterrole",
        "plural": "clusterroles",
        "scope": "Cluster",
        "group": "rbac.authorization.k8s.io"
    },
    {
        "kind": "RoleBinding",
        "singular": "rolebinding",
        "plural": "rolebindings",
        "scope": "Namespaced",
        "group": "rbac.authorization.k8s.io"
    },
    {
        "kind": "Role",
        "singular": "role",
        "plural": "roles",
        "scope": "Namespaced",
        "group": "rbac.authorization.k8s.io"
    },
    {
        "kind": "Route",
        "singular": "route",
        "plural": "routes",
        "scope": "Namespaced",
        "group": "route.openshift.io"
    },
    {
        "kind": "Config",
        "singular": "config",
        "plural": "configs",
        "scope": "Cluster",
        "group": "samples.operator.openshift.io"
    },
    {
        "kind": "PriorityClass",
        "singular": "priorityclasse",
        "plural": "priorityclasses",
        "scope": "Cluster",
        "shortNames": ["pc"],
        "group": "scheduling.k8s.io"
    },
    {
        "kind": "RangeAllocation",
        "singular": "rangeallocation",
        "plural": "rangeallocations",
        "scope": "Cluster",
        "group": "security.internal.openshift.io"
    },
    {
        "kind": "PodSecurityPolicyReview",
        "singular": "podsecuritypolicyreview",
        "plural": "podsecuritypolicyreviews",
        "scope": "Namespaced",
        "group": "security.openshift.io"
    },
    {
        "kind": "PodSecurityPolicySelfSubjectReview",
        "singular": "podsecuritypolicyselfsubjectreview",
        "plural": "podsecuritypolicyselfsubjectreviews",
        "scope": "Namespaced",
        "group": "security.openshift.io"
    },
    {
        "kind": "PodSecurityPolicySubjectReview",
        "singular": "podsecuritypolicysubjectreview",
        "plural": "podsecuritypolicysubjectreviews",
        "scope": "Namespaced",
        "group": "security.openshift.io"
    },
    {
        "kind": "RangeAllocation",
        "singular": "rangeallocation",
        "plural": "rangeallocations",
        "scope": "Cluster",
        "group": "security.openshift.io"
    },
    {
        "kind": "SecurityContextConstraints",
        "singular": "securitycontextconstraint",
        "plural": "securitycontextconstraints",
        "scope": "Cluster",
        "shortNames": ["scc"],
        "group": "security.openshift.io"
    },
    {
        "kind": "VolumeSnapshotClass",
        "singular": "volumesnapshotclasse",
        "plural": "volumesnapshotclasses",
        "scope": "Cluster",
        "group": "snapshot.storage.k8s.io"
    },
    {
        "kind": "VolumeSnapshotContent",
        "singular": "volumesnapshotcontent",
        "plural": "volumesnapshotcontents",
        "scope": "Cluster",
        "group": "snapshot.storage.k8s.io"
    },
    {
        "kind": "VolumeSnapshot",
        "singular": "volumesnapshot",
        "plural": "volumesnapshots",
        "scope": "Namespaced",
        "group": "snapshot.storage.k8s.io"
    },
    {
        "kind": "CSIDriver",
        "singular": "csidriver",
        "plural": "csidrivers",
        "scope": "Cluster",
        "group": "storage.k8s.io"
    },
    {
        "kind": "CSINode",
        "singular": "csinode",
        "plural": "csinodes",
        "scope": "Cluster",
        "group": "storage.k8s.io"
    },
    {
        "kind": "CSIStorageCapacity",
        "singular": "csistoragecapacitie",
        "plural": "csistoragecapacities",
        "scope": "Namespaced",
        "group": "storage.k8s.io"
    },
    {
        "kind": "StorageClass",
        "singular": "storageclasse",
        "plural": "storageclasses",
        "scope": "Cluster",
        "shortNames": ["sc"],
        "group": "storage.k8s.io"
    },
    {
        "kind": "VolumeAttachment",
        "singular": "volumeattachment",
        "plural": "volumeattachments",
        "scope": "Cluster",
        "group": "storage.k8s.io"
    },
    {
        "kind": "BrokerTemplateInstance",
        "singular": "brokertemplateinstance",
        "plural": "brokertemplateinstances",
        "scope": "Cluster",
        "group": "template.openshift.io"
    },
    {
        "kind": "Template",
        "singular": "processedtemplate",
        "plural": "processedtemplates",
        "scope": "Namespaced",
        "group": "template.openshift.io"
    },
    {
        "kind": "TemplateInstance",
        "singular": "templateinstance",
        "plural": "templateinstances",
        "scope": "Namespaced",
        "group": "template.openshift.io"
    },
    {
        "kind": "Template",
        "singular": "template",
        "plural": "templates",
        "scope": "Namespaced",
        "group": "template.openshift.io"
    },
    {
        "kind": "Profile",
        "singular": "profile",
        "plural": "profiles",
        "scope": "Namespaced",
        "group": "tuned.openshift.io"
    },
    {
        "kind": "Tuned",
        "singular": "tuned",
        "plural": "tuneds",
        "scope": "Namespaced",
        "group": "tuned.openshift.io"
    },
    {
        "kind": "Group",
        "singular": "group",
        "plural": "groups",
        "scope": "Cluster",
        "group": "user.openshift.io"
    },
    {
        "kind": "Identity",
        "singular": "identitie",
        "plural": "identities",
        "scope": "Cluster",
        "group": "user.openshift.io"
    },
    {
        "kind": "UserIdentityMapping",
        "singular": "useridentitymapping",
        "plural": "useridentitymappings",
        "scope": "Cluster",
        "group": "user.openshift.io"
    },
    {
        "kind": "User",
        "singular": "user",
        "plural": "users",
        "scope": "Cluster",
        "group": "user.openshift.io"
    },
    {
        "kind": "IPPool",
        "singular": "ippool",
        "plural": "ippools",
        "scope": "Namespaced",
        "group": "whereabouts.cni.cncf.io"
    },
    {
        "kind": "OverlappingRangeIPReservation",
        "singular": "overlappingrangeipreservation",
        "plural": "overlappingrangeipreservations",
        "scope": "Namespaced",
        "group": "whereabouts.cni.cncf.io"
    },
    {
        "kind": "CephBlockPool",
        "singular": "cephblockpool",
        "plural": "cephblockpools",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephClient",
        "singular": "cephclient",
        "plural": "cephclients",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephCluster",
        "singular": "cephcluster",
        "plural": "cephclusters",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephFilesystemMirror",
        "singular": "cephfilesystemmirror",
        "plural": "cephfilesystemmirrors",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephFilesystem",
        "singular": "cephfilesystem",
        "plural": "cephfilesystems",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephNFS",
        "singular": "cephnfse",
        "plural": "cephnfses",
        "scope": "Namespaced",
        "shortNames": ["nfs"],
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephObjectRealm",
        "singular": "cephobjectrealm",
        "plural": "cephobjectrealms",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephObjectStore",
        "singular": "cephobjectstore",
        "plural": "cephobjectstores",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephObjectStoreUser",
        "singular": "cephobjectstoreuser",
        "plural": "cephobjectstoreusers",
        "scope": "Namespaced",
        "shortNames": ["rcou", "objectuser"],
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephObjectZoneGroup",
        "singular": "cephobjectzonegroup",
        "plural": "cephobjectzonegroups",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephObjectZone",
        "singular": "cephobjectzone",
        "plural": "cephobjectzones",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },
    {
        "kind": "CephRBDMirror",
        "singular": "cephrbdmirror",
        "plural": "cephrbdmirrors",
        "scope": "Namespaced",
        "group": "ceph.rook.io"
    },

    # {
    #     "kind": "",
    #     "singular": "",
    #     "plural": "",
    #     "scope": "",
    #     "shortNames": [],
    #     "group": ""
    # },

]


# RDEFS Generated by the following script:

"""
#!/bin/bash
while read apiresline; do
    cols=$(echo ${apiresline} | tr -s ' ' | tr ' ' '\n' | wc -l)
    name=$(echo ${apiresline} | awk '{print $1}')
    if [ "${cols}" == "4" ]; then
        short=""
        api=$(echo ${apiresline} | awk '{print $2}')
        nsed=$(echo ${apiresline} | awk '{print $3}')
        kind=$(echo ${apiresline} | awk '{print $4}')
    elif [ "${cols}" == "5" ]; then
        short=$(echo ${apiresline} | awk '{print $2}')
        api=$(echo ${apiresline} | awk '{print $3}')
        nsed=$(echo ${apiresline} | awk '{print $4}')
        kind=$(echo ${apiresline} | awk '{print $5}')
    else
        echo "WARNING: Invalid line: ${apiresline}"
        continue
    fi

    sing=$(echo "${name}" | sed 's/s$//')

    if [ "${nsed}" == "true" ]; then
        scope="Namespaced"
    else
        scope="Cluster"
    fi

    if [[ "{$api}" == *"/"* ]]; then
        group=$(echo ${api} | cut -d '/' -f 1)
        apiver=$(echo ${api} | cut -d '/' -f 2)
    else
        group="core"
        apiver=${api}
    fi

    if [ -n "${short}" ]; then
        shortNames='['
        for sn in $(echo ${short} | tr ',' '\n'); do
            shortNames="${shortNames}\"${sn}\", "
        done
        shortNames=$(echo ${shortNames} | sed 's/,$/]/')
    else
        shortNames=""
    fi

if [ -n "${shortNames}" ]; then

cat <<EOF
    {
        "kind": "${kind}",
        "singular": "${sing}",
        "plural": "${name}",
        "scope": "${scope}",
        "shortNames": ${shortNames},
        "group": "${group}"
    },
EOF

else

cat <<EOF
    {
        "kind": "${kind}",
        "singular": "${sing}",
        "plural": "${name}",
        "scope": "${scope}",
        "group": "${group}"
    },
EOF

fi

done < <(oc api-resources --no-headers)
"""
