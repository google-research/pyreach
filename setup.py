# coding=utf-8
# Copyright 2021 The PyReach Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup."""

from distutils import core
import os
from setuptools import find_packages

PYREACH_VERSION='0.0.1'

here = os.path.abspath(os.path.dirname(__file__))
try:
  README = open(os.path.join(here, 'README.md'), encoding='utf-8').read()
except IOError:
  README = ''

ur5e_so = os.path.join(here, 'pyreach', 'ikfast', 'linux_so', 'libur5e_ikfast61.so')

if not os.path.exists(ur5e_so):
  raise Exception('Please run build.sh first.')

install_requires = [
    'absl-py>=0.7.0',
    'gym>=0.17.3',
    'numpy>=1.18.5',
    'pybullet>=3.0.4',
    'matplotlib>=3.1.1',
    'opencv-python>=4.1.2.30',
    'meshcat>=0.0.18',
    'scipy>=1.4.1',
    'scikit-image>=0.17.2',
    'transforms3d>=0.3.1',
    'requests',
]


core.setup(
    name='PyReach',
    version=PYREACH_VERSION,
    description='PyReach is the Python client for the Reach system.',
    long_description='\n\n'.join([README]),
    long_description_content_type='text/markdown',
    author='Google Inc',
    author_email='robotics-reach@google.com',
    url='https://github.com/google-research/pyreach',
    packages=find_packages(),
    install_requires=install_requires,
    package_data={'pyreach.ikfast.linux_so': ['libFCR7ia_ikfast61.so', 'libFLRM200ic_ikfast61.so', 'libFLRM200id7l_ikfast61.so', 'libFLRM200id_ikfast61.so', 'libFR2000ia165f_ikfast61.so', 'libur10e_ikfast61.so', 'libur5e_ikfast61.so', 'libur5_ikfast61.so', 'libxarm6_ikfast61.so']},
    scripts=['reach', 'reach-viewer', 'reach-pendant'],
)
