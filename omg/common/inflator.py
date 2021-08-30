import os
import tarfile

__supported_extensions = [
    '.tar.gz',
    '.tar.bz2',
    '.tar.xz',
    '.tgz',
    '.tbz',
    '.tbz2',
    '.txz',
]


def __get_rootdir_info(inflator):
    finfo_list = inflator.getmembers()
    # Get the root directories:
    rootdir = None
    for finfo in finfo_list:
        if finfo.isdir() and finfo.name.count('/') == 0:
            rootdir = finfo
            break
    return rootdir
    
# Left path_to_extract as an option, default to current directory.
# We need to further modify the use command to use it correctly, but
# I prefer to not apply that changes at this state. Feel free to add
# the change if you feel that could be useful.
def inflate_file(filename, path_to_extract='./'):
    print('Trying to uncompress:', filename, 'to', path_to_extract)
    if not tarfile.is_tarfile(filename):
        print('[ERROR] This is not a valid TAR file.')
        return None
    print('File looks ok!, opening now.')
    inflator = tarfile.open(filename, 'r')
    rootdir = __get_rootdir_info(inflator)
    if not rootdir:
        print(
            '[ERROR] There is not a root directory in the file, that is not good, '
            'uncompress and check the file manually'
        )
        return None
    # Check for file contents, we must have a 
    #  'must-gather.*' directory on the root of the compressed file
    if not rootdir.name.startswith('must-gather'):
        print(
            '[ERROR] Root directoty do not match "must-gather*", that is not good, '
            'uncompress and check the file manually'
        )
        return None
    # Extract all the files:
    print('Extracting files')
    inflator.extractall(path_to_extract)
    # return the name of the extracted path
    return rootdir.name