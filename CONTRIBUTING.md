# Setting up the Development Environment

1. Git clone the repository

```
git clone https://github.com/kxr/o-must-gather
```

2. Create and activate a separate python virtual environment for o-must-gather

```
# Create a new venv
python3 -m venv o-must-gather-venv
# Activate the venv
source o-must-gather-venv/bin/activate
```
3. Install o-must-gather in the venv

```
pip3 install -e o-must-gather/
```

If the above steps were executed successfully, you should now have:

  - Code directory `o-must-gather`(which we cloned from github)
  - Python venv directory `o-must-gather-venv` (all the dependencies/libraries are contained here)
  - `omg` executable binary in your path

Any change in the code will now be directly reflected and can be tested.
To deactivate the python venv, simply run `deactivate`.
Note that since we installed o-must-gather in a venv, `omg` binary will only be available when the venv is activated (`source o-must-gather-venv/bin/activate`).

# Architecture of o-must-gather

## Entry Point
  - `omg/cli.py`
  
  This is the the main entry point when `omg` is invoked. It sets the flags for any switches passed (e.g, -o wide or --all-namespaces), checks the commands (e.g, `get`, `log` etc.) passed and calls the respective command function. 
  
## Handling Commands
  - `omg/cmd/describe.py`
  - `omg/cmd/get_main.py`
  - `omg/cmd/log.py`
  - `omg/cmd/project.py`
  - `omg/cmd/use.py`
  - `omg/cmd/whoami.py`

These are all the files/functions responsible handling the "commands" i.e, whatever goes after `omg` e.g, `get`, `log`, `project` etc. All of them are self-contained except `get`, since it is complex. `get` is hanlded by `omg/cmd/get_main.py` and the sub-logic is in the `omg/cmd/get/*.py` files depending on the type of object(s) that is being get.


### Handling state and configuration
  - `omg/common/config.py`
  - `omg/cmd/use.py`

  `omg` stores its state in a config file saved at `~/.omgconfig`. State is basically two things, the absolute path of the must-gather that the user has selected (`omg use <path>`) and the current project that user is in. `~/.omgconfig` is simply a yaml file with these two keys. When the user calls `omg use ...`, the `omg/cmd/use.py` function checks if its a valid must-gather directory (i.e, it looks for `/namespaces` and `/cluster-scoped-resources`) and instantiates the omg/common/config.py:Config class with two properties `path` and `project`. Every other file simply imports this class and then accesses these two properties via class variables (class variables are shared by all instances of the class.). For example [`mg_path = Config().path`](https://github.com/kxr/o-must-gather/blob/c7cae6fcfa5f04e85cb8728c859d5e27ccfa9c1b/omg/cmd/get/from_yaml.py#L9)

## Get command and Resource map
- `omg/cmd/get_main.py`
- `omg/cmd/get/*.py`
- `omg/common/resource_map.py`

This is the epicenter of o-must-gather. The problem and complexity at hand is that there are many different types of objects (e.g, pods, nodes etc.) that we need to handle. These have different aliases (e.g, pod, pods, po) and are spread across different yamls in different directories, often times redundant. Some are namespace bound, some are not. The output of each type should be displayed in a unique way. Here is how I approached this problem trying to keep it plugable (i.e, new types can be easily added):

  - **Resource map**
  
    There is an array of dictionaries called [`map`](https://github.com/kxr/o-must-gather/blob/c7cae6fcfa5f04e85cb8728c859d5e27ccfa9c1b/omg/common/resource_map.py#L36-L202) defined in `omg/common/resource_map.py`. Each dictionary represents a type of object we can handle. This array is the single source of truth for what omg can and cannot handle. For example, following is the dictionary for pod:

    ```
        {   'type': 'pod',  'aliases': ['pods', 'po'],  'need_ns': True,
            'get_func': from_yaml,  'getout_func': pod_out,
            'yaml_loc': 'namespaces/%s/core/pods.yaml'                },
    ```
    We define what type of object this is, what are its aliases (i.e, other names with which the user might request this object), is it namespace bound?, What function will be used to "get" the object, what function will be used to show the output and finally the yaml location of this object.
    If the object is namespace bound (i.e, `need_ns: True`) we expect a '%s' in the `yaml_loc` string that will be replaced by whatever project the user has selected (either by `omg project <project>` or by passing -n <project>). If yaml location is not pointing to a yaml file directly but a directory, we will scan for all the *.yaml files in that directory. For example:

    ```
    {   'type': 'node', 'aliases': ['nodes'],  'need_ns': False,
            'get_func': from_yaml, 'getout_func': node_out,
            'yaml_loc': 'cluster-scoped-resources/core/nodes'    },
    ```
    Finally there is a [`map_res(t)`](https://github.com/kxr/o-must-gather/blob/c7cae6fcfa5f04e85cb8728c859d5e27ccfa9c1b/omg/common/resource_map.py#L205-L211) function that simply takes "type" as input, looks up this type in the `map` array and returns the dictionary if a match is found or returns `None` if a match is not found. We don't access the map variable directly but rather use this function to look up object types. 

  - **get_main.py**

    The `get_main()` is the top level function that handles the get command. Remember that we are trying to replicate `oc` and `get` command can get quite complicated, since a user can request in different kinds of format, for example:

      - `omg get pod` (just one object type)
      - `omg get pods,svc` (multiple object types)
      - `omg get pod httpd-8fp9c` (object type with specific object name)
      - `omg get pod/httpd-8fp9c` (object type with specific name using '/' delimeter)
      - `omg get pod/httpd-8fp9c svc/httpd` (multiple object types with names)

    The `get_main()` function has two main jobs. First, it parases the arguments and creates a python dictionary called [`objects`](https://github.com/kxr/o-must-gather/blob/c7cae6fcfa5f04e85cb8728c859d5e27ccfa9c1b/omg/cmd/get_main.py#L37) that simply holds all the objects types and names (if any) that we need to `get`. If you are troubleshooting or just curious, uncomment the [`# print(objects)`](https://github.com/kxr/o-must-gather/blob/c7cae6fcfa5f04e85cb8728c859d5e27ccfa9c1b/omg/cmd/get_main.py#L111-L112) line to print this dictionary every time we process the arguments passed after `omg get ...`.
    Secondly, once we know what to get, for each object type, we call the `map_res()` fucntion to get the respective `map` dictionary, call the `get_func` to collect the objects from the respective yamls, store all the objects in a python variable and pass it on to the `getout_func`.
    
  - **get_func and getout_func**

    The `get_func` and `getout_func` functions are kept in separate files in `omg/cmd/get/*.py`. All of them must be imporated at the top in `resource_map.py` as we need to put them in the object's `map` dictionary. 
    
    The `get_func` is almost always `from_yaml` (`omg/cmd/get/from_yaml.py`) except for "project" type. This exception is because we don't load projects from a single yaml/directory but rather from the yamls present in each directory at `<must-gather>/namespaces/`.
    
    `from_yaml()` function simply loads all the yamls and collects all the objects in an array that is returned. For object that we collect, this function also notes and returns the timestamp of the yaml that the object is being collected from. The timestamp is used to caculate the age of the object.
    
    Another thing worth mentioning is that initially a simple `yaml.safe_load(yaml_file)` function was being used to load the yaml files into python variable. However later it was observed that often times the yaml file would contain some grabage in the last few lines and would cause the whole omg operation to exception out. To overcome this problem, a special helper function `omg/common/helper.py` -> `load_yaml_file()` was written. This function first tries to load the yaml file and if it fails, it tries skipping lines from the bottom one by one, until the file is successfully loaded. A warning message is displayed showing how many lines were skipped.
    
    The `getout_func` is specialzed for each object type. We are using the `tabulate` library to output and it seems to work prefectly.
 
## Age of objects

The age/last_seen/since columns are calculated with reference to when the must-gather was generated, by checking the timestamps of the yaml files in the must-gather. This gives us the age of the objects that the cluster would have reported at the time must-gather was generated. It also gives consistent output, regardles of when we check a must-gather.

There is helper function `age()` in `omg/common/helper.py` that calculates the age of the object. It takes the object's timestamp and the object's yaml's timestamp as input and returns the age. 

## Handling New Object types (CR)

If you want to add support for handling a new object type, the steps would be as follows:

  - Add a new dictionary in `resource_map.py` -> `map` array. Set the `yaml_loc` to specify where the yaml of this object type is located in the must-gather. For `get_func`, most probably, the `from_yaml` function would work as it is working for most of the object types. For the `getout_func`, start by using the `simple_out` function and test it. `simple_out` function will simply output the name and age of the retreived objects.
  - If required, create a new output function in a separate file. You can copy an existing one and adjust accordingly. Import this function in the `resource_map.py` and set it in the `getout_func` in the object's `map` dictionary.

