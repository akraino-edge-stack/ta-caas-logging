#! /usr/bin/python

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

import os

from cmframework.apis import cmactivator


class caasactivator(cmactivator.CMGlobalActivator):
    playbooks = dict(
        infra_chart_reconfig="/opt/openstack-ansible/playbooks/infra_chart_reconfig_fluentd.yaml"
    )

    def __init__(self):
        super(caasactivator, self).__init__()

    def get_subscription_info(self):
        return 'cloud.caas'

    def activate_set(self, props):
        self._activate()

    def activate_delete(self, props):
        self._activate()

    def activate_full(self, target):
        self._activate(target=target)

    def _activate(self, target=None):
        if 'CONFIG_PHASE' in os.environ:
            return
        self.run_playbook(self.playbooks['infra_chart_reconfig'], target)
