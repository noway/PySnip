import sys
import os
import distutils
import subprocess
from setuptools import setup, find_packages, Extension
from distutils.command.build import build as _build
from distutils.core import run_setup
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules = []

names = [
    'pyspades.vxl',
    'pyspades.bytes',
    'pyspades.packet',
    'pyspades.contained',
    'pyspades.common',
    'pyspades.world',
    'pyspades.loaders',
    'pyspades.mapmaker'
]

for name in names:
    extra = {'extra_compile_args' : ['-std=c++11']} if name in ['pyspades.vxl', 'pyspades.world', 'pyspades.mapmaker'] else {}

    ext_modules.append(Extension(name, ['%s.pyx' % name.replace('.', '/')],
        language = 'c++', include_dirs=['pyspades'], **extra))

class build(_build):
    def run(self):

        previousDir = os.getcwd()
        os.chdir("enet")
        subprocess.Popen(["./prebuild.sh"]).communicate()

        os.chdir("pyenet")
        run_setup(os.path.join(os.getcwd(), "setup.py"), ['build_ext', '--inplace'])
        os.chdir(previousDir)

        _build.run(self)

setup(
    name = 'pysnip',
    packages = ['pysnip', 'pysnip.feature_server', 'pyspades', 'pyspades.enet'],
    version = '0.0.0',
    description = 'Open-source server implementation for Ace of Spades',
    author = 'Matpow2, Stackoverflow',
    author_email = 'nate.shoffner@gmail.com',
    url = 'https://github.com/NateShoffner/PySnip',
    download_url = 'https://github.com/NateShoffner/PySnip/archive/master.tar.gz',
    keywords = ['ace of spades', 'aos', 'server'],
    classifiers = [],
	setup_requires = ['cython'],
	install_requires = ['twisted'],
	extras_require = {
		'from': ['pygeoip'], 
		'statusserver': ['jinja2', 'pillow'],
		'ssh': ['pycrypto', 'pyasn1']
	},
    entry_points = {
        'console_scripts': [
        	'pysnip=pysnip.feature_server.run:main'
    	],
    },
    package_dir = {'pysnip': '', 'pyspades': 'pyspades', 'pyspades.enet': 'enet/pyenet'},
    package_data = {'pyspades.enet': ["enet.so"]},
    # ext_package = "pyspades",
    ext_modules = cythonize(ext_modules),
    cmdclass = {'build': build},

)
