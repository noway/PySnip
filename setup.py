import sys
import os
import distutils
from setuptools import setup, find_packages, Extension
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

from distutils.command.build import build as _build


class build(_build):
    def run(self):
        print "** running enet"
        distutils.core.run_setup(os.path.join(sys.path[0], "enet/setup.py"), ['build_ext', '--inplace'])
        print "** ran enet"
        _build.run(self)
        # self.execute(_run_build_tables, (self.install_lib,),
        #              msg="Build the lexing/parsing tables")

pyspades_ext_modules = cythonize(ext_modules) 

from pprint import pprint
print "-- ext modules"
print pyspades_ext_modules
pprint(pyspades_ext_modules[0].__dict__)

setup(
    name = 'pysnip',
    packages = ['pysnip', 'pyspades', 'pyspades.enet', 'pysnip.feature_server'],
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
    package_dir = {'pysnip': '', 'pyspades': 'pyspades', 'pyspades.enet': 'enet'},
    package_data = {'pyspades.enet': ["enet.so"]},
    # ext_package = "pyspades",
    ext_modules = pyspades_ext_modules ,
    cmdclass = {'build': build},

)
