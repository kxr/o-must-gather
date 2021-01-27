import os, yaml
from omg.common.config import Config
from omg.cmd.get_main import get_resources
from omg.cmd.machine_config.decode_content import decode_content


def write_unit(systemd_path, unit):
    os.makedirs(systemd_path,exist_ok=True)
    name = unit['name']
    if 'enabled' in unit:
        if unit['enabled'] is not True:
            name += '.disabled'
    if 'content' in unit:
        abs_fil = os.path.join(systemd_path, name)
        with open(abs_fil, 'w') as fh:
            print(abs_fil)
            fh.write(
                unit['contents']
            )

def extract(m):
    mg_path = Config().path
    emc_dir = 'extracted-machine-configs'
    emc_path = os.path.join(mg_path, emc_dir)
    os.makedirs(emc_path, exist_ok=True)
    
    mcs_res = get_resources('machineconfig', m, None)
    mcs = [mc['res'] for mc in mcs_res]

    for mc in mcs:
        if 'metadata' in mc and 'name' in mc['metadata']:
            mc_name = mc['metadata']['name']
        else:
            print('[WARNING] Skipping machine-config. Name not found')
            continue

        mc_path = os.path.join(emc_path, mc_name)
        os.makedirs(mc_path, exist_ok=True)

        if 'spec' in mc and 'config' in mc['spec']:
            # storage
            if 'storage' in mc['spec']['config']:
                storage_path = os.path.join(mc_path, 'storage')
                storage = mc['spec']['config']['storage']
                if 'files' in storage:
                    for fi in storage['files']:
                        path = fi['path']
                        rel_fil = path[1:]
                        rel_dir = os.path.dirname(rel_fil)
                        abs_dir = os.path.join(storage_path, rel_dir)
                        abs_fil = os.path.join(storage_path, rel_fil)
                        os.makedirs(abs_dir,exist_ok=True)
                        with open(abs_fil, 'w') as fh:
                            print(abs_fil)
                            fh.write(
                                decode_content(fi['contents']['source'])
                            )
            # TODO directories, links, disks, raid, filesystems
            # systemd
            if 'systemd' in mc['spec']['config']:
                systemd_path = os.path.join(mc_path, 'systemd')
                systemd = mc['spec']['config']['systemd']
                if 'units' in systemd:
                    for unit in systemd['units']:
                        if 'dropins' in unit:
                            systemd_path = os.path.join(mc_path, 'systemd/' + unit['name'] + '.d')
                            for unit in unit['dropins']:
                                write_unit(systemd_path, unit)
                        else:
                            write_unit(systemd_path, unit)
            # passwd
            if 'passwd' in mc['spec']['config']:
                passwd  = mc['spec']['config']['passwd']
                passwd_path = os.path.join(mc_path, 'passwd')
                if 'users' in passwd:
                    for user in passwd['users']:
                        os.makedirs(passwd_path,exist_ok=True)
                        name = user['name']
                        abs_fil = os.path.join(passwd_path, name)
                        with open(abs_fil, 'w') as fh:
                            print(abs_fil)
                            fh.write( yaml.dump(user) )
                # TODO groups
            # TODO networkd
