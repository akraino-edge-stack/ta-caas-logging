#!/usr/bin/env python

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

# pylint: disable=line-too-long, too-few-public-methods

from copy import deepcopy

from hostcli.helper import ListerHelper, ShowOneHelper, CommandHelper

API_VERSION =       'v1'
RESOURCE_PREFIX =   'caas/%s/' % API_VERSION
ID =                'id'
NAMESPACE =         'namespace'
PLUGIN =            'plugin'
TARGETURL =         'target_url'
STREAM =            'stream'


FIELDMAP = {
    ID:         {'display': 'ID',
                 'help': 'The ID of the log entry'},
    NAMESPACE:  {'display': 'namespace',
                 'help': 'The kubernetes namespace where the log entry applies'},
    PLUGIN:     {'display': 'plugin',
                 'help': 'The fluentd plugin which is used for forwarding log entries. '
                         'Should be one of remote_syslog, elasticsearch'},
    TARGETURL:  {'display': 'target_url',
                 'help': 'The URL of the log storage where fluentd will send log entries'},
    STREAM:     {'display': 'stream',
                 'help': 'The stream which will be logged by fluentd. '
                         'Should be one of stdout, stderr, both'}
}


class CaasCliLister(ListerHelper):
    """Helper class for Lister"""
    def __init__(self, app, app_args, cmd_name=None):
        super(CaasCliLister, self).__init__(app, app_args, cmd_name)
        self.fieldmap = deepcopy(FIELDMAP)
        self.resource_prefix = RESOURCE_PREFIX


class CaasCliShowOne(ShowOneHelper):
    """Helper class for ShowOne"""
    def __init__(self, app, app_args, cmd_name=None):
        super(CaasCliShowOne, self).__init__(app, app_args, cmd_name)
        self.fieldmap = deepcopy(FIELDMAP)
        self.resource_prefix = RESOURCE_PREFIX


class CaasCliCommand(CommandHelper):
    """Helper class for Command"""
    def __init__(self, app, app_args, cmd_name=None):
        super(CaasCliCommand, self).__init__(app, app_args, cmd_name)
        self.fieldmap = deepcopy(FIELDMAP)
        self.resource_prefix = RESOURCE_PREFIX


class CreateAppLogBackend(CaasCliCommand):
    """A command for adding a new CaaS application log forwarding entry."""

    def __init__(self, app, app_args, cmd_name=None):
        super(CreateAppLogBackend, self).__init__(app, app_args, cmd_name)
        self.operation = 'post'
        self.endpoint = 'log/apps'
        self.mandatory_positional = True
        self.positional_count = 4
        self.arguments = [NAMESPACE, PLUGIN, TARGETURL, STREAM]
        self.message = 'Entry has been added.'


class ChangeAppLogBackend(CaasCliCommand):
    """A command for modifying a CaaS application log forwarding entry."""

    def __init__(self, app, app_args, cmd_name=None):
        super(ChangeAppLogBackend, self).__init__(app, app_args, cmd_name)
        self.operation = 'put'
        self.endpoint = 'log/apps'
        self.mandatory_positional = True
        self.positional_count = 1
        self.arguments = [ID, NAMESPACE, PLUGIN, TARGETURL, STREAM]
        self.message = 'Entry has been updated.'


class DeleteAppLogBackend(CaasCliCommand):
    """A command for removing a CaaS application log forwarding entry."""

    def __init__(self, app, app_args, cmd_name=None):
        super(DeleteAppLogBackend, self).__init__(app, app_args, cmd_name)
        self.operation = 'delete'
        self.endpoint = 'log/apps'
        self.mandatory_positional = True
        self.positional_count = 1
        self.arguments = [ID]
        self.message = 'Entry has been deleted.'


class ShowAppLogBackend(CaasCliShowOne):
    """A command for showing detail of a CaaS application log forwarding entry."""

    def __init__(self, app, app_args, cmd_name=None):
        super(ShowAppLogBackend, self).__init__(app, app_args, cmd_name)
        self.operation = 'get'
        self.endpoint = 'log/apps'
        self.mandatory_positional = True
        self.positional_count = 1
        self.arguments = [ID]
        self.columns = [ID, NAMESPACE, PLUGIN, TARGETURL, STREAM]
        self.default_sort = [ID, 'asc']


class ListAppLogBackend(CaasCliLister):
    """A command for listing existing CaaS application log forwarding entries."""

    def __init__(self, app, app_args, cmd_name=None):
        super(ListAppLogBackend, self).__init__(app, app_args, cmd_name)
        self.operation = 'get'
        self.endpoint = 'log/apps'
        self.no_positional = True
        self.columns = [ID, NAMESPACE, PLUGIN, TARGETURL, STREAM]
        self.default_sort = [ID, 'asc']


class ListAppLogBackendForNamespace(CaasCliLister):
    """A command for listing existing CaaS application log forwarding entries for a namespace"""

    def __init__(self, app, app_args, cmd_name=None):
        super(ListAppLogBackendForNamespace, self).__init__(app, app_args, cmd_name)
        self.operation = 'get'
        self.endpoint = 'log/apps'
        self.mandatory_positional = True
        self.positional_count = 1
        self.arguments = [NAMESPACE]
        self.columns = [ID, NAMESPACE, PLUGIN, TARGETURL, STREAM]
        self.default_sort = [ID, 'asc']
