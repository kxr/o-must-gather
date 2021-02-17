"""
oc like tool that works with must-gather rather than OpenShift API
"""
from setuptools import find_packages, setup
import omg

dependencies = ['tabulate', 'pyyaml', 'python-dateutil', 'cryptography>=2.5,<=3.3.2', 'click==7.1.2']

setup(
    name='o-must-gather',
    version=omg.version,
    url='https://github.com/kxr/o-must-gather',
    license='GPLv3',
    author='Khizer Naeem',
    author_email='khizernaeem@gmail.com',
    description='oc like tool that works with must-gather rather than OpenShift API',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'omg = omg.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
