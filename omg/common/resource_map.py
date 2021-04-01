from omg.cmd.get.from_yaml import from_yaml
from omg.cmd.get.get_project import get_project

from omg.cmd.get.simple_out import simple_out
from omg.cmd.get.bc_out import bc_out
from omg.cmd.get.build_out import build_out
from omg.cmd.get.co_out import co_out
from omg.cmd.get.cm_out import cm_out
from omg.cmd.get.cj_out import cj_out
from omg.cmd.get.crd_out import crd_out
from omg.cmd.get.csr_out import csr_out
from omg.cmd.get.cv_out import cv_out
from omg.cmd.get.dc_out import dc_out
from omg.cmd.get.deployment_out import deployment_out
from omg.cmd.get.ds_out import ds_out
from omg.cmd.get.ep_out import ep_out
from omg.cmd.get.eps_out import eps_out
from omg.cmd.get.ev_out import ev_out
from omg.cmd.get.hpa_out import hpa_out
from omg.cmd.get.is_out import is_out
from omg.cmd.get.job_out import job_out
from omg.cmd.get.machine_out import machine_out
from omg.cmd.get.machineset_out import machineset_out
from omg.cmd.get.mcp_out import mcp_out
from omg.cmd.get.mc_out import mc_out
from omg.cmd.get.mwhc_out import mwhc_out
from omg.cmd.get.node_out import node_out
from omg.cmd.get.pod_out import pod_out
from omg.cmd.get.project_out import project_out
from omg.cmd.get.pv_out import pv_out
from omg.cmd.get.pvc_out import pvc_out
from omg.cmd.get.rc_out import rc_out
from omg.cmd.get.route_out import route_out
from omg.cmd.get.rs_out import rs_out
from omg.cmd.get.sc_out import sc_out
from omg.cmd.get.secret_out import secret_out
from omg.cmd.get.service_out import service_out
from omg.cmd.get.ss_out import ss_out
from omg.cmd.get.vwhc_out import vwhc_out

import os
from omg.common.config import Config


# This map and function normalizes/standarizes the different names of object/resources types
# Also returns the function that handles get,describe and output of this object type
# This is how the top level get_main function knows which objects we can handle and how.
# returns None if not an object type that we can't handle


map = [

    {   'type': 'apiserver','aliases': ['apiservers'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/apiservers.yaml' },

    {   'type': 'authentication','aliases': ['authentications'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/authentications.yaml' },

    {   'type': 'build','aliases': ['builds'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': build_out,
        'yaml_loc': 'namespaces/%s/build.openshift.io/builds.yaml' },
    
    {   'type': 'buildconfig','aliases': ['buildconfigs', 'bc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': bc_out,
        'yaml_loc': 'namespaces/%s/build.openshift.io/buildconfigs.yaml' },

    {   'type': 'certificatesigningrequest','aliases': ['certificatesigningrequests', 'csr'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': csr_out,
        'yaml_loc': 'cluster-scoped-resources/certificates.k8s.io/certificatesigningrequests' },
        
    {   'type': 'clusteroperator','aliases': ['clusteroperators', 'co'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': co_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/clusteroperators.yaml' },

    {   'type': 'clusterversion','aliases': ['clusterversions'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': cv_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/clusterversions.yaml' },

    {   'type': 'configmap','aliases': ['configmaps', 'cm'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': cm_out,
        'yaml_loc': 'namespaces/%s/core/configmaps.yaml' },

    {   'type': 'console','aliases': ['consoles'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/consoles.yaml' },

    {   'type': 'cronjob','aliases': ['cronjobs'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': cj_out,
        'yaml_loc': 'namespaces/%s/batch/cronjobs.yaml' },

    {   'type': 'customresourcedefinition','aliases': ['customresourcedefinitions', 'crd', 'crds'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': crd_out,
        'yaml_loc': 'cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions' },
    
    {   'type': 'daemonset','aliases': ['daemonsets', 'ds'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ds_out,
        'yaml_loc': 'namespaces/%s/apps/daemonsets.yaml' },
        
    {   'type': 'deployment','aliases': ['deployments'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': deployment_out,
        'yaml_loc': 'namespaces/%s/apps/deployments.yaml' },

    {   'type': 'deploymentconfig','aliases': ['deploymentconfigs', 'dc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': dc_out,
        'yaml_loc': 'namespaces/%s/apps.openshift.io/deploymentconfigs.yaml' },

    {   'type': 'dns','aliases': ['dnses'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/dnses.yaml' },

    {   'type': 'endpoint','aliases': ['endpoints', 'ep'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ep_out,
        'yaml_loc': 'namespaces/%s/core/endpoints.yaml' },

    {   'type': 'endpointslice','aliases': ['endpointslices'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': eps_out,
        'yaml_loc': 'namespaces/%s/discovery.k8s.io/endpointslices.yaml' },

    {   'type': 'event','aliases': ['events', 'ev'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ev_out,
        'yaml_loc': 'namespaces/%s/core/events.yaml' },

    {   'type': 'featuregate','aliases': ['featuregates'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/featuregates.yaml' },

    {   'type': 'horizontalpodautoscaler','aliases': ['horizontalpodautoscalers', 'hpa'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': hpa_out,
        'yaml_loc': 'namespaces/%s/autoscaling/horizontalpodautoscalers.yaml' },

    {   'type': 'image','aliases': ['images'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/images.yaml' },

    {   'type': 'imagestream','aliases': ['imagestreams','is'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': is_out,
        'yaml_loc': 'namespaces/%s/image.openshift.io/imagestreams.yaml' },

    {   'type': 'infrastructure','aliases': ['infrastructures'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/infrastructures.yaml' },

    {   'type': 'ingress','aliases': ['ingresses'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/ingresses.yaml' },

    {   'type': 'job','aliases': ['jobs'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': job_out,
        'yaml_loc': 'namespaces/%s/batch/jobs.yaml' },

    {   'type': 'machine','aliases': ['machines'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': machine_out,
        'yaml_loc': 'namespaces/%s/machine.openshift.io/machines' },

    {   'type': 'machineconfig','aliases': ['machineconfigs', 'mc'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mc_out,
        'yaml_loc': 'cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs' },

    {   'type': 'machineconfigpool','aliases': ['machineconfigpools', 'mcp'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mcp_out,
        'yaml_loc': 'cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools' },

    {   'type': 'machineset','aliases': ['machinesets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': machineset_out,
        'yaml_loc': 'namespaces/%s/machine.openshift.io/machinesets' },

    {   'type': 'mutatingwebhookconfiguration','aliases': ['mutatingwebhookconfigurations'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mwhc_out,
        'yaml_loc': 'cluster-scoped-resources/admissionregistration.k8s.io/mutatingwebhookconfigurations' },
        
    {   'type': 'network','aliases': ['networks'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/networks.yaml' },

    {   'type': 'node','aliases': ['nodes'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': node_out,
        'yaml_loc': 'cluster-scoped-resources/core/nodes' },
        # When yaml_loc is a dir like in this case, we scan *.yaml files in it.

    {   'type': 'oauth','aliases': ['oauths'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/oauths.yaml' },

    {   'type': 'operatorhub','aliases': ['operatorhubs'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/operatorhubs.yaml' },
        
    {   'type': 'persistentvolume','aliases': ['persistentvolumes', 'pv'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': pv_out,
        'yaml_loc': 'cluster-scoped-resources/core/persistentvolumes' },

    {   'type': 'persistentvolumeclaim','aliases': ['persistentvolumeclaims', 'pvc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': pvc_out,
        'yaml_loc': 'namespaces/%s/core/persistentvolumeclaims.yaml' },
        
    {   'type': 'pod','aliases': ['pods', 'po'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': pod_out,
        'yaml_loc': 'namespaces/%s/core/pods.yaml' },

    {   'type': 'project','aliases': ['projects'],'need_ns': False,
        'get_func': get_project, 'getout_func': project_out,
        'yaml_loc': 'namespaces/*/*.yaml' },

    {   'type': 'proxy','aliases': ['proxies'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/proxies.yaml' },

    {   'type': 'replicaset','aliases': ['replicasets', 'rs'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': rs_out,
        'yaml_loc': 'namespaces/%s/apps/replicasets.yaml' },

    {   'type': 'replicationcontroller','aliases': ['replicationcontrollers', 'rc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': rc_out,
        'yaml_loc': 'namespaces/%s/core/replicationcontrollers.yaml' },

    {   'type': 'route','aliases': ['routes'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': route_out,
        'yaml_loc': 'namespaces/%s/route.openshift.io/routes.yaml' },

    {   'type': 'scheduler','aliases': ['schedulers'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/schedulers.yaml' },

    {   'type': 'secret','aliases': ['secrets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': secret_out,
        'yaml_loc': 'namespaces/%s/core/secrets.yaml' },

    {   'type': 'service','aliases': ['services', 'svc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': service_out,
        'yaml_loc': 'namespaces/%s/core/services.yaml' },

    {   'type': 'statefulset','aliases': ['statefulsets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ss_out,
        'yaml_loc': 'namespaces/%s/apps/statefulsets.yaml' },

    {   'type': 'storageclass','aliases': ['storageclasses', 'sc'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': sc_out,
        'yaml_loc': 'cluster-scoped-resources/storage.k8s.io/storageclasses' },

    {   'type': 'validatingwebhookconfiguration','aliases': ['validatingwebhookconfigurations'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': vwhc_out,
        'yaml_loc': 'cluster-scoped-resources/admissionregistration.k8s.io/validatingwebhookconfigurations' },

    {   'type': 'clusterroles','aliases': ['clusterroles'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/rbac.authorization.k8s.io/clusterroles' },

    {   'type': 'clusterrolebindings','aliases': ['clusterrolebindings'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/rbac.authorization.k8s.io/clusterrolebindings' },

    {   'type': 'roles','aliases': ['roles'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/rbac.authorization.k8s.io/roles' },

    {   'type': 'rolebindings','aliases': ['rolebindings'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/rbac.authorization.k8s.io/rolebindings' },

    {   'type': 'ingresscontroller','aliases': ['ingresscontrollers'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/operator.openshift.io/ingresscontrollers' },

]


def map_res(t):
    if t is not None:
        for x in map:
            # match the input with type: or alias (without case)
            if t.lower() == x['type'].lower() or t.lower() in [y.lower() for y in x['aliases'] ]:
                return x
        # If we didn't find the resource definition in the map dictionary
        # We "try" to build the definition dynamically from the crd definitions
        # Idea credit goes to bostrt: https://github.com/kxr/o-must-gather/issues/34
        # This is just fall back and expensive to compute,
        # ideally these definitions should be added to the map dict for better lookup performance
        try:
            crds = from_yaml('_all', '_all', 'cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions', False)
            for c in crds:
                singular = c['res']['spec']['names']['singular']
                plural = c['res']['spec']['names']['plural']
                if 'shortNames' in c['res']['spec']['names']:
                    short = c['res']['spec']['names']['shortNames']
                else:
                    short = []
                aliases = [plural] + short
                if t.lower() == singular or t.lower() in aliases:
                    # We found the resource type in crd
                    res_dict = {
                        'type': singular,
                        'aliases': aliases,
                        'need_ns': None,
                        'get_func': from_yaml,
                        'getout_func': simple_out,
                        'yaml_loc': None    }

                    # need_ns
                    if c['res']['spec']['scope'] == 'Namespaced':
                        res_dict['need_ns'] = True
                        yaml_pre = 'namespaces/%s/'
                    elif c['res']['spec']['scope'] == 'Cluster':
                        res_dict['need_ns'] = False
                        yaml_pre = 'cluster-scoped-resources/'
                    else:
                        # Unhandled situation
                        return None

                    # yaml_loc
                    group = c['res']['spec']['group']
                    mg_path = Config().path
                    res_dict['yaml_loc'] = os.path.join(mg_path,yaml_pre,group,plural)

                    return res_dict
        except:
            pass
            
    return None
