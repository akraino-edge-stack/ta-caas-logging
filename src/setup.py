# Copyright 2019 Nokia

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

from setuptools import setup, find_packages
setup(
    name='caas_logging',
    version='1.0',
    license='Apache-2.0',
    author='Gabor Mate',
    author_email='gabor.mate@nokia.com',
    platforms=['Any'],
    scripts=[],
    provides=[],
    namespace_packages=['caas_logging'],
    packages=find_packages(),
    include_package_data=True,
    description='CaaS Logging for Akraino REC',
    install_requires=['flask', 'flask-restful', 'hostcli'],
    entry_points={
        'hostcli.commands': [
            'caas applications log add            = caas_logging.cli.caas:CreateAppLogBackend',
            'caas applications log change         = caas_logging.cli.caas:ChangeAppLogBackend',
            'caas applications log delete         = caas_logging.cli.caas:DeleteAppLogBackend',
            'caas applications log show           = caas_logging.cli.caas:ShowAppLogBackend',
            'caas applications log list           = caas_logging.cli.caas:ListAppLogBackend',
            'caas applications log list namespace = caas_logging.cli.caas:ListAppLogBackendForNamespace',
        ],
    },
    zip_safe=False,
)
