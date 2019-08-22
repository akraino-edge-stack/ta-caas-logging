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

import json

from cmframework.apis import cmclient

from yarf.restresource import RestResource

MISSING_LOG_STORE_ENTRY_INDEX = 'Missing log store entry index parameter'
PATTERN_SHOULD_BE_ONE_OF = '{} should be one of: {}'

ID = 'id'
NAMESPACE = 'namespace'
SUPPORTED_BACKENDS = ('elasticsearch', 'remote_syslog')
SUPPORTED_STREAMS = ('stdout', 'stderr', 'both')


class CaasHandler(RestResource):
    KEY_CAAS = 'cloud.caas'

    def _get_caas_config(self):
        api = cmclient.CMClient()
        return json.loads(api.get_property(self.KEY_CAAS))

    def _update_caas_config(self, updated):
        api = cmclient.CMClient()
        api.set_property(self.KEY_CAAS, json.dumps(updated))

    @staticmethod
    def _response(return_code, data='', error_desc=''):
        return {"code": return_code, "description": error_desc, "data": data}

    def _result(self, data=None):
        return self._response(0, data=data)

    def _error(self, exc):
        error_desc = str(exc).replace('Internal error, ', '')
        return self._response(1, error_desc=error_desc)

    def _modify_caas_config(self, modifier_method):
        try:
            caas = self._get_caas_config()
            modifier_method(self, caas, self.get_args())
            self._update_caas_config(caas)
            return self._result('')
        except Exception as exc:
            return self._error(exc)


class AppLogStoreHandler(CaasHandler):
    KEY_NAME = 'log_forwarding'

    parser_arguments = [ID, NAMESPACE, 'plugin', 'target_url', 'stream']
    endpoints = ['log/apps']

    def post(self):
        """
        .. :quickref: CaaS - Log forwarding;Add the log forwarding configuration entry

        **Add the new containerized application log forwarding entry to configuration**:

        **Example request**:

        .. sourcecode:: http

            POST /caas/v1/log/apps HTTP/1.1
            Host: haproxyvip:61200
            Content-Type: application/json
            Accept: application/json

            {
                "namespace": "app1",
                "plugin": "elasticsearch",
                "target_url": "http://elasticsearch.elk.svc.nokia.net:9200",
                "stream": "stderr"
            }

        :<json string namespace: Apply forwarding for containers deployed in this namespace
        :<json string plugin: Plugin that handles log forwarding, one of ``elasticsearch``, ``remote_syslog``
        :<json string target_url: Log storage service URL (eg. ``protocol://ip-or-fqdn:port``)
        :<json string stream: Output stream source of gathered logs, one of ``stdout``, ``stderr``, ``both``

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 0,
                "description": ""
                "data": ""
            }

        :>json int code: The status code, 0 when OK other when error
        :>json string description: The error description, present if code is non zero
        :>json string data: Empty string in all cases
        :statuscode 200: no error
        :statuscode 401: on authentication error

        """
        def func(self, caas, args):
            entries = caas[self.KEY_NAME]
            args.pop(ID)
            if args['plugin'] not in SUPPORTED_BACKENDS:
                raise ValueError(PATTERN_SHOULD_BE_ONE_OF.format('plugin', ', '.join(SUPPORTED_BACKENDS)))
            if args['stream'] not in SUPPORTED_STREAMS:
                raise ValueError(PATTERN_SHOULD_BE_ONE_OF.format('stream', ', '.join(SUPPORTED_STREAMS)))
            if entries.count(args):
                raise ValueError('Already exists')
            entries.append(args)

        return self._modify_caas_config(func)

    def get(self):
        """
        .. :quickref: CaaS - Log forwarding;Get the existing log forwarding configuration

        **Get the existing containerized application log forwarding configuration**:

        Optionally request could filter entries by namespace.

        **Example request**:

        .. sourcecode:: http

            GET /caas/v1/apps HTTP/1.1
            Host: haproxyvip:61200
            Content-Type: application/json
            Accept: application/json

            {
                "namespace": "app1"
            }

        :<json string namespace: (optional) The IP address of the server where logs are forwarded to

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 0,
                "description": ""
                "data":
                {
                    "1":
                    {
                        "id": 1,
                        "namespace": "app1",
                        "plugin": "remote_syslog",
                        "target_url": "tcp://http://rsyslog.log.svc.nokia.net:1234",
                        "stream": "stderr"
                    }
                }
            }

        :>json int code: The status code, 0 when OK other when error
        :>json string description: The error description, present if code is non zero
        :>json string data: Contains the log forwarding configuration
        :>json string id: The identifier of the log forwarding entry
        :>json string namespace: Apply forwarding for containers deployed in this namespace
        :>json string plugin: Plugin that handles log forwarding, one of ``elasticsearch``, ``remote_syslog``
        :>json string target_url: Log storage service URL (eg. ``protocol://ip-or-fqdn:port``)
        :>json string stream: Output stream source of gathered logs, one of ``stdout``, ``stderr``, ``both``
        :statuscode 200: no error
        :statuscode 401: on authentication error

        """
        try:
            caas = self._get_caas_config()
            value = caas[self.KEY_NAME]
            args = self.get_args()
            data = {}
            for idx, v in enumerate(value, start=1):
                v[ID] = idx
                data[idx] = v
            if args[ID] is not None:
                return self._result({args[ID]: value[int(args[ID]) - 1]})
            elif args[NAMESPACE] is not None:
                return self._result({k: v for (k, v) in data.items() if v[NAMESPACE] == args[NAMESPACE]})
            else:
                return self._result(data)

        except Exception as exc:
            return self._error(exc)

    def put(self):
        """
        .. :quickref: CaaS - Log forwarding;Change the existing log forwarding entry configuration

        **Change the existing containerized application log forwarding entry configuration**:

        **Example request**:

        .. sourcecode:: http

            PUT /caas/v1/apps HTTP/1.1
            Host: haproxyvip:61200
            Content-Type: application/json
            Accept: application/json

            {
                "id": 1,
                "namespace": "app2"
            }

        :<json string id: (mandatory) The index of the entry to be modified
        :<json string namespace: (optional) Apply forwarding for containers deployed in this namespace
        :<json string plugin: (optional) Plugin that handles log forwarding, one of ``elasticsearch``, ``remote_syslog``
        :<json string target_url: (optional) Log storage service URL (eg. ``protocol://ip-or-fqdn:port``)
        :<json string stream: (optional) Output stream source of gathered logs, one of ``stdout``, ``stderr``, ``both``

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 0,
                "description": "",
                "data": ""
            }

        :>json int code: The status code, 0 when OK other when error
        :>json string description: The error description, present if code is non zero
        :>json string data: Empty string in all cases
        :statuscode 200: no error
        :statuscode 401: on authentication error

        """
        def func(self, caas, args):
            if args[ID] is None:
                raise ValueError(MISSING_LOG_STORE_ENTRY_INDEX)
            else:
                idx = int(args[ID]) - 1
                for k, v in args.items():
                    if not k == ID and v is not None:
                        caas[self.KEY_NAME][idx][k] = v

        return self._modify_caas_config(func)

    def delete(self):
        """
        .. :quickref: CaaS - Log forwarding;Delete the entry from log forwarding configuration

        **Delete the entry from containerized application log forwarding configuration**:

        **Example request**:

        .. sourcecode:: http

            DELETE /caas/v1/apps HTTP/1.1
            Host: haproxyvip:61200
            Content-Type: application/json
            Accept: application/json

            {
                "id": "1"
            }

        :<json string id: (mandatory) The index of the entry to be deleted

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 0,
                "description": ""
                "data": ""
            }

        :>json int code: The status code, 0 when OK other when error
        :>json string description: The error description, present if code is non zero
        :>json string data: Empty string in all cases
        :statuscode 200: no error
        :statuscode 401: on authentication error

        """
        def func(self, caas, args):
            if args[ID] is None:
                raise ValueError(MISSING_LOG_STORE_ENTRY_INDEX)
            else:
                caas[self.KEY_NAME].pop(int(args[ID]) - 1)

        return self._modify_caas_config(func)
