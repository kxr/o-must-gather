import sys

from . import cmd_get as get

# This function normalizes/standarizes the different names of object/resources types
# Also returns the function that handles get/describe of this object type
# This is how the top level omg_get function knows which objects we can handle and how
# e.g: for the input 'pods', 'pod' or 'po' it will return: 
#   { 'type':'pod', 'get_func': omg_get_pod, 'desc_func': omg_desc_pod }
# returns None if not an object type that we can handle
def check_res(t):
    map = { 'pod': { 'aliases': ['pod', 'pods', 'po'],
                     'get_func': get.simple, 'getout_func': get.pod_out,
                     'yaml_loc': '/core/pods.yaml'},

            'svc': { 'aliases': ['service', 'svc'],
                     'get_func': get.simple, 'getout_func': get.simple_out,
                     'yaml_loc': '/core/services.yaml'},

            'secrets' : { 'aliases': ['secrets'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/secrets.yaml'},

            'cm' : { 'aliases': ['configmap', 'configmaps', 'cm'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/configmaps.yaml'},

            'ep' : { 'aliases': ['endpoint', 'endpoints', 'ep'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/endpoints.yaml'},

            'ev' : { 'aliases': ['event', 'events', 'ev'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/events.yaml'},

            'pvc' : { 'aliases': ['persistentvolumeclaim', 'persistentvolumeclaims', 'pvc'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/persistentvolumeclaims.yaml'},

            'rc' : { 'aliases': ['replicationcontrollers', 'replicationcontrollers', 'rc'],
                    'get_func': get.simple, 'getout_func': get.simple_out,
                    'yaml_loc': '/core/replicationcontrollers.yaml'},
            }

    #return next(
    #    ( { 'type':x,
    #        'get_func': map[x]['get_func'],
    #        'getout_func': map[x]['getout_func'],
    #        'yaml_loc': map[x]['yaml_loc'] }
    #        for x in map.keys() if t.lower() in map[x]['aliases'] 
    #    ),None)
    for x in map.keys():
        if t.lower() in map[x]['aliases']:
            return { 'type':x,
                     'get_func': map[x]['get_func'],
                     'getout_func': map[x]['getout_func'],
                     'yaml_loc': map[x]['yaml_loc'] }
    return None